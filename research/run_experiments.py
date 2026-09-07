"""Run the complete synthetic benchmark; writes raw rows, figures and web data."""
from pathlib import Path
import json, csv, time, hashlib, sys
import numpy as np
from bbci.model import *

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)

def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def bootstrap(x,seed=809,n=4000):
    r=np.random.default_rng(seed); a=np.asarray(x)
    means=a[r.integers(0,len(a),size=(n,len(a)))].mean(1)
    return [float(np.mean(a)), *np.quantile(means,[.025,.975]).tolist()]

def main():
    start=time.time(); people=[Person(k) for k in range(24)]
    cs=[calibrate(p,seed=710+p.index*11) for p in people]
    (OUT/'calibration.json').write_text(json.dumps(cs,indent=2))
    print('Calibrated 24 synthetic individuals',flush=True)
    rows=[]; retained={}; replay={}; examples={}
    scenarios={'nominal':{},'delay_2s':{'delay':2},'sensor_noise':{'measurement_noise':.05},
      'stimulation_artifact':{'artifact':.2},'plasticity':{'plasticity':.15}}
    for scenario,opts in scenarios.items():
        for seed in (100,200,300):
            for p,c in zip(people,cs):
                for arm in ARMS[:-1]:
                    if scenario!='nominal' and arm not in ('sham','rate','combined'): continue
                    rr=simulate(p,arm,seed=seed,calibration=c,**opts)
                    metric=evaluate(rr,c)
                    rows.append(dict(scenario=scenario,person=p.index,seed=seed,arm=arm,**metric))
                    if scenario=='nominal' and arm=='combined':
                        replay[p.index,seed]=np.array([rr['u'][min((k+1)*100,5999)] for k in range(60)])
                    if scenario=='nominal' and seed==100 and p.index<4:
                        # 20-Hz animation data, original inference uses 100-Hz.
                        examples[f'{p.index}_{arm}']={k:np.round(v[::5],6).tolist() for k,v in rr.items() if isinstance(v,np.ndarray)}
        print('Completed scenario:',scenario,flush=True)
    for seed in (100,200,300):
        for p,c in zip(people,cs):
            rr=simulate(p,'yoked',seed=seed,calibration=c,replay=replay[(p.index+1)%24,seed])
            rows.append(dict(scenario='nominal',person=p.index,seed=seed,arm='yoked',**evaluate(rr,c)))
            if seed==100 and p.index<4: examples[f'{p.index}_yoked']={k:np.round(v[::5],6).tolist() for k,v in rr.items() if isinstance(v,np.ndarray)}
    write_csv('all_runs.csv',rows)
    # Aggregate replicates within individuals; confidence intervals resample people.
    means={}
    for scenario in scenarios:
        for arm in ARMS:
            sel=[r for r in rows if r['scenario']==scenario and r['arm']==arm]
            if not sel: continue
            means[scenario,arm]={k:np.array([np.mean([r[k] for r in sel if r['person']==p.index]) for p in people]) for k in ('tracking_mse','accuracy','rate_error','entropy','spectral_entropy','control_energy','washout_mse','weight_change','washout_weight_change')}
    summary={}
    for (scenario,arm),metrics in means.items():
        summary[f'{scenario}_{arm}']={k:bootstrap(v) for k,v in metrics.items()}
    contrast={}
    for scenario in scenarios:
        for pair in [('combined','rate'),('combined','sham'),('rate','sham')]:
            a,b=pair
            contrast[f'{scenario}_{a}_minus_{b}']={k:bootstrap(means[scenario,a][k]-means[scenario,b][k]) for k in ('tracking_mse','accuracy','rate_error','entropy','control_energy')}
    contrast['nominal_combined_minus_yoked']={k:bootstrap(means['nominal','combined'][k]-means['nominal','yoked'][k]) for k in ('tracking_mse','accuracy','control_energy')}
    # Fresh baseline validation, not fitted-session accuracy.
    ref=[evaluate(simulate(p,seed=900,calibration=c,stressed=False),c) for p,c in zip(people,cs)]
    validation={'heldout_baseline_accuracy':bootstrap([r['accuracy'] for r in ref]),
      'heldout_baseline_mse':bootstrap([r['tracking_mse'] for r in ref]),
      'rate_entropy_slope_range':[min(c['slope'] for c in cs),max(c['slope'] for c in cs)],
      'ambiguous_entropy_slopes':sum(abs(c['slope'])<.01 for c in cs)}
    # Step-size sensitivity uses a common seed but NOT a common stochastic path;
    # stochastic paths differ across dt, so compare aggregate outcomes, not trajectories.
    conv=[]
    for p,c in zip(people[:6],cs[:6]):
        for dt in (.004,.002,.001):
            if dt==.004: continue # outputs require a divisor of 10 ms
            rr=simulate(p,'combined',seed=900,calibration=c,dt=dt)
            conv.append(dict(person=p.index,dt=dt,**evaluate(rr,c)))
    write_csv('step_size_check.csv',conv)
    # Gain sweep tests nonmonotonicity without imposing an inverted-U curve.
    sweep=[]
    for p,c in zip(people[:8],cs[:8]):
        original=p.gain
        for gain in np.linspace(.9,2.4,11):
            p.gain=float(gain); rr=simulate(p,seed=400,calibration=c,stressed=False)
            sweep.append(dict(person=p.index,gain=float(gain),**evaluate(rr,c)))
        p.gain=original
    write_csv('gain_sweep.csv',sweep)
    # Spectral surrogate: preserves each observed record's Fourier magnitudes.
    sur=[]; rg=np.random.default_rng(809)
    for p,c in zip(people[:8],cs[:8]):
        rr=simulate(p,seed=500,calibration=c); x=rr['observed'][1500:4500]; ft=np.fft.rfft(x)
        for k in range(40):
            phase=rg.uniform(-np.pi,np.pi,len(ft)); phase[0]=0.; phase[-1]=0.
            ft_s=ft*np.exp(1j*phase); y=np.fft.irfft(ft_s,n=len(x))
            sur.append(dict(person=p.index,rep=k,original=permutation_entropy(x),surrogate=permutation_entropy(y)))
    write_csv('phase_surrogates.csv',sur)
    payload={'summary':summary,'contrasts':contrast,'validation':validation,'n_people':24,'n_seeds':3,'n_runs':len(rows),'runtime_seconds':time.time()-start,'model_sha256':hashlib.sha256((ROOT/'bbci/model.py').read_bytes()).hexdigest()}
    (OUT/'summary.json').write_text(json.dumps(payload,indent=2))
    web={'example_metrics':{f"{r['person']}_{r['arm']}": {'mse':r['tracking_mse'],'accuracy':r['accuracy'],'energy':r['control_energy']} for r in rows if r['scenario']=='nominal' and r['seed']==100 and r['person']<4}, 'people':[{**{'index':p.index,'gain':p.gain,'coupling':p.coupling,'drive':p.drive,'disturbance':p.disturbance},'W':p.W.tolist(),'w_ee':p.w_ee.tolist(),'w_ei':p.w_ei.tolist(),'field':p.field.tolist(),'calibration':c} for p,c in zip(people[:4],cs[:4])], 'examples':examples,'study':payload}
    (OUT/'web_data.json').write_text(json.dumps(web,separators=(',',':')))
    print(json.dumps({'runs':len(rows),'elapsed':time.time()-start,'validation':validation,'primary':contrast['nominal_combined_minus_rate']}),flush=True)

if __name__=='__main__': main()
