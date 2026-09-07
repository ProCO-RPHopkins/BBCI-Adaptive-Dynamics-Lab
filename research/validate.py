"""Meaningful deterministic, numerical and benchmark integrity checks."""
from pathlib import Path
import json, csv
import numpy as np
from scipy.integrate import solve_ivp
from bbci.model import Person, simulate, permutation_entropy, _rng

ROOT=Path(__file__).resolve().parent
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    assert condition,name

def main():
    x=np.random.default_rng(10).normal(size=10000)
    check('monotone_and_constant_entropy_zero',permutation_entropy(np.arange(100.))==0 and permutation_entropy(np.ones(100))==0)
    check('iid_entropy_near_one',.995<permutation_entropy(x)<=1)
    check('ordinal_entropy_monotonic_transform_invariance',abs(permutation_entropy(x)-permutation_entropy(np.exp(x)))<1e-14)
    p=Person(); c=json.loads((ROOT/'results/calibration.json').read_text())[0]
    r=simulate(p,'combined',seed=100,calibration=c)
    rr=simulate(p,'combined',seed=100,calibration=c)
    check('bitwise_seed_reproducibility',np.array_equal(r['E'],rr['E']))
    check('finite_bounded_population',np.isfinite(r['E']).all() and r['E'].min()>=0 and r['E'].max()<=1)
    check('amplitude_and_slew_limits',abs(r['u']).max()<=.600000001 and abs(np.diff(r['u'])).max()<=.150000001)
    sham=simulate(p,'sham',seed=100,calibration=c)
    check('matched_task_stream',np.array_equal(r['label'],sham['label']))
    check('zero_sham_input',np.max(abs(sham['u']))==0)
    no_entropy=dict(c,slope=0)
    a=simulate(p,'rate',calibration=no_entropy); b=simulate(p,'combined',calibration=no_entropy)
    check('weak_entropy_calibration_abstains',np.array_equal(a['E'],b['E']))
    plastic=simulate(p,'combined',calibration=c,plasticity=.15)
    ratio=plastic['drift'][-1]/plastic['drift'][4499]
    check('plasticity_washout_matches_prescribed_decay',abs(ratio-np.exp(-15/20))<1e-4)
    # Independent adaptive ODE solver checks the actual production integrator.
    # Dynamic and measurement noise are zero. First task label is constant until .5 s.
    _,z=_rng(100); label=1 if z>.5 else -1
    task=np.array([.6*label if i%8<2 else 0 for i in range(16)])
    def rhs(t,state):
        E,I=state[:16],state[16:]
        a=p.gain*(p.w_ee*E-p.w_ei*I+p.coupling*p.W@E+p.drive+task-2.5)
        b=p.gain*(10*E-2*I-3)
        return np.r_[(-E+1/(1+np.exp(-a)))/.04,(-I+1/(1+np.exp(-b)))/.08]
    target=solve_ivp(rhs,(0,.5),np.full(32,.1),rtol=1e-11,atol=1e-13).y[:16,-1]
    errors=[]
    for dt in (.002,.001,.0005):
        run=simulate(p,'sham',seed=100,duration=.5,dt=dt,stressed=False,measurement_noise=0,dynamic_noise=0)
        errors.append(float(np.max(abs(run['E'][-1]-target))))
    check('deterministic_euler_converges_to_independent_solver',errors[2]<errors[1]<errors[0] and errors[0]<.001)
    rows=list(csv.DictReader((ROOT/'results/all_runs.csv').open()))
    check('1296_unique_evaluation_rows',len(rows)==1296 and len({(x['scenario'],x['person'],x['seed'],x['arm']) for x in rows})==1296)
    energies={a:sum(float(x['control_energy']) for x in rows if x['scenario']=='nominal' and x['arm']==a) for a in ('combined','yoked')}
    check('yoked_aggregate_energy_matched',abs(energies['combined']-energies['yoked'])<1e-10)
    result={'checks':checks,'passed':len(checks),'deterministic_step_sizes':[.002,.001,.0005], 'max_E_errors_vs_solve_ivp':errors,'plasticity_decay_ratio':ratio,
      'scope':'Numerical and software verification only; no human or biological validation. Deterministic convergence is local to this autonomous 0.5-second case. Stochastic step sensitivity is separate.'}
    (ROOT/'results/validation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
