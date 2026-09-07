"""Reproducible Wilson-Cowan-type neural-mass benchmark.

All current, gain, coupling and controller amplitudes are dimensionless.
Regions and connections are synthetic. No diagnostic or treatment inference.
Reference: Wilson & Cowan (1972), doi:10.1016/S0006-3495(72)86068-5.
"""
from dataclasses import dataclass
import math
import numpy as np
from numba import njit

ARMS = ('sham', 'fixed', 'rate', 'entropy', 'combined', 'yoked')

@dataclass
class Person:
    index: int = 0
    n: int = 16
    def __post_init__(self):
        r = np.random.default_rng(4100 + self.index)
        self.gain = float(r.uniform(1.25, 1.75))
        self.coupling = float(r.uniform(1.4, 2.6))
        self.drive = float(r.uniform(.55, 1.05))
        self.disturbance = float(r.choice([-1, 1]) * r.uniform(.35, .8))
        self.w_ee = r.uniform(2.5, 4.5, self.n)
        self.w_ei = r.uniform(9, 11, self.n)
        # Two hemispheres, four modules; no autism label is assigned.
        i,j = np.indices((self.n,self.n))
        w = .15 + .6*((i%8)//2 == (j%8)//2) + .3*(i//8 == j//8)
        w = w*r.lognormal(0,.3,w.shape)
        np.fill_diagonal(w,0)
        self.W = w/w.sum(axis=1,keepdims=True)
        # Broad illustrative actuator, stronger in association populations.
        self.field = np.array([.35,.35,.65,.65,1,1,.75,.75]*2)

@njit(cache=True)
def _rng(state):
    state = (1664525*state + 1013904223) & 4294967295
    return state, (state+.5)/4294967296

@njit(cache=True)
def _normal(state):
    state,u = _rng(state); state,v = _rng(state)
    return state, math.sqrt(-2*math.log(u))*math.cos(2*math.pi*v)

@njit(cache=True)
def _pe(x, lag=2):
    counts=np.zeros(6); total=len(x)-2*lag
    if total<1: return 0.
    for t in range(total):
        a,b,c=x[t],x[t+lag],x[t+2*lag]
        # Stable tie order: a precedes b precedes c.
        if a<=b:
            k=0 if b<=c else (1 if a<=c else 4)
        else:
            k=2 if a<=c else (3 if b<=c else 5)
        counts[k]+=1
    h=0.
    for k in range(6):
        if counts[k]>0:
            p=counts[k]/total; h-=p*math.log(p)
    return h/math.log(6.)

def permutation_entropy(x, lag=2):
    return float(_pe(np.asarray(x,dtype=float),lag))

@njit(cache=True)
def _run(W0,wee,wei,field,gain,coupling,drive,disturbance,seed,arm,
         dt,duration,target_r,target_h,h_slope,fixed,measurement_noise,
         artifact,delay,plasticity,replay,stressed,amplitude,freeze_after,dynamic_noise):
    n=len(wee); steps=int(round(duration/dt)); stride=int(round(.01/dt))
    nout=steps//stride; window=100; out=np.zeros((nout,n))
    observed=np.zeros(nout); labels=np.zeros(nout); us=np.zeros(nout)
    hs=np.zeros(nout); drift=np.zeros(nout); rs=np.zeros(nout)
    E=np.full(n,.1); I=np.full(n,.1); noise=np.zeros(n); avg=np.full(n,.1)
    W=W0.copy(); u=0.; h=0.; state=int(seed); m=0.; cov=np.zeros((n,n))
    ew=np.zeros(n); iw=np.zeros(n); label=1.; q=0
    cap_events=0; clip_events=0
    # Delay is an integer number of 1-second update windows.
    for t in range(steps):
        sec=t*dt
        if t % int(round(.5/dt)) == 0:
            state,z=_rng(state); label=1. if z>.5 else -1.
        perturb=0.
        if stressed and sec>=15 and sec<45:
            perturb=disturbance*(1. if sec<30 else -.6)
        for i in range(n):
            state,z=_normal(state)
            noise[i] += -dt/.15*noise[i] + dynamic_noise*math.sqrt(2*dt/.15)*z
        # Euler update, simultaneous E/I state transition.
        for i in range(n):
            network=0.
            for j in range(n): network+=W[i,j]*E[j]
            task=.6*label if i%8<2 else 0.
            a=gain*(wee[i]*E[i]-wei[i]*I[i]+coupling*network+drive+task+perturb+field[i]*u+noise[i]-2.5)
            b=gain*(10*E[i]-2*I[i]-3.)
            se=1/(1+math.exp(-max(-50.,min(50.,a))))
            si=1/(1+math.exp(-max(-50.,min(50.,b))))
            ew[i]=E[i]+dt/.04*(-E[i]+se)
            iw[i]=I[i]+dt/.08*(-I[i]+si)
        for i in range(n):
            E[i]=ew[i]; I[i]=iw[i]
            avg[i]+=dt/2*(E[i]-avg[i])
        if plasticity>0:
            for i in range(n):
                for j in range(n):
                    if i!=j:
                        learn=plasticity*(E[i]-avg[i])*(E[j]-avg[j]) if sec<freeze_after else 0.
                        change=learn-(W[i,j]-W0[i,j])/20
                        raw=W[i,j]+dt*change
                        W[i,j]=max(.25*W0[i,j],min(2*W0[i,j],raw))
        if (t+1)%stride==0:
            m=0.; dw=0.; denom=0.
            for i in range(n):
                out[q,i]=E[i]; m+=E[i]/n
                for j in range(n):
                    dw+=(W[i,j]-W0[i,j])**2; denom+=W0[i,j]**2
            # Observe population mean, not a validated EEG forward model.
            state,z=_normal(state)
            observed[q]=m+measurement_noise*z+artifact*u*math.sin(2*math.pi*37*sec)
            labels[q]=label; us[q]=u; rs[q]=m; drift[q]=math.sqrt(dw/denom)
            hs[q]=h
            if (q+1)%window==0:
                end=q+1-delay*window
                if end>=window:
                    h=_pe(observed[end-window:end],2)
                    rm=np.mean(observed[end-window:end])
                    er=target_r-rm; eh=target_h-h
                    # A calibration derivative with a dead zone, not entropy maximization.
                    du=0. if abs(h_slope)<.01 else max(-.35,min(.35,eh/h_slope))
                    rate=4*er
                    proposal=0.
                    if arm==1: proposal=fixed
                    elif arm==2: proposal=rate
                    elif arm==3: proposal=.5*u+.5*du
                    elif arm==4: proposal=rate+.3*du
                    elif arm==5:
                        idx=min(int(sec),len(replay)-1); proposal=replay[idx]
                    if sec<10 or sec>=45: proposal=0.
                    if abs(proposal)>amplitude: cap_events+=1
                    # Slew and amplitude limits are numerical constraints only.
                    delta=max(-.15,min(.15,proposal-u))
                    u=max(-amplitude,min(amplitude,u+delta))
            q+=1
    return out,observed,labels,us,hs,drift,rs,cap_events

def simulate(person=None, arm='sham', seed=100, duration=60., dt=.002,
             calibration=None, measurement_noise=.001, artifact=0., delay=0,
             plasticity=.0, replay=None, stressed=True, amplitude=.6,
             fixed_override=None, freeze_after=45., dynamic_noise=.04):
    p=person or Person()
    if dt<=0 or abs(round(.01/dt)*dt-.01)>1e-9 or dt>.01:
        raise ValueError('dt must evenly divide 0.01 and be <=0.01 s')
    c=calibration or {'rate':.2,'entropy':.8,'slope':0.,'fixed':0.}
    if delay<0 or int(delay)!=delay: raise ValueError('delay must be an integer >=0')
    vals=_run(p.W,p.w_ee,p.w_ei,p.field,p.gain,p.coupling,p.drive,p.disturbance,
       seed,ARMS.index(arm),dt,duration,c['rate'],c['entropy'],c['slope'],
       c['fixed'] if fixed_override is None else fixed_override,measurement_noise,
       artifact,int(delay),plasticity,np.zeros(61) if replay is None else replay,
       stressed,amplitude,freeze_after,dynamic_noise)
    return dict(zip(('E','observed','label','u','entropy_online','drift','rate','cap_events'),vals))

def calibrate(p, seed=710):
    # Independent reference session; no outcome labels from evaluation are used.
    baseline=simulate(p,seed=seed,stressed=False,measurement_noise=.001)
    selected=slice(1000,4500)
    rate=float(baseline['rate'][selected].mean())
    hs=[permutation_entropy(baseline['observed'][k:k+100]) for k in range(1000,4401,100)]
    entropy=float(np.mean(hs))
    c={'rate':rate,'entropy':entropy,'slope':0.,'fixed':0.}
    plus=simulate(p,'fixed',seed=seed,stressed=False,calibration=c,fixed_override=.2)
    minus=simulate(p,'fixed',seed=seed,stressed=False,calibration=c,fixed_override=-.2)
    hp=np.mean([permutation_entropy(plus['observed'][k:k+100]) for k in range(1500,4401,100)])
    hm=np.mean([permutation_entropy(minus['observed'][k:k+100]) for k in range(1500,4401,100)])
    c['slope']=float((hp-hm)/.4)
    # Ridge readout from non-input populations, delayed to reflect response latency.
    idx=np.array([i for i in range(p.n) if i%8>=2]); c['readout_indices']=idx.tolist()
    X=baseline['E'][1000:4500,idx]; y=baseline['label'][985:4485]
    center=X.mean(0); scale=X.std(0)+1e-6; Z=(X-center)/scale
    beta=np.linalg.solve(Z.T@Z+10*np.eye(len(idx)),Z.T@y)
    c.update(center=center.tolist(),scale=scale.tolist(),beta=beta.tolist())
    # Open-loop comparator tuned on independent perturbed calibration data.
    scores=[]; candidates=np.linspace(-.6,.6,7)
    for u in candidates:
        rr=simulate(p,'fixed',seed=seed+1,calibration=c,fixed_override=float(u))
        scores.append(evaluate(rr,c)['tracking_mse'])
    c['fixed']=float(candidates[int(np.argmin(scores))])
    c['baseline_accuracy']=evaluate(baseline,c)['accuracy']
    return c

def evaluate(run,c):
    e=run['E']; idx=c['readout_indices']
    z=(e[:,idx]-np.asarray(c['center']))/np.asarray(c['scale'])
    prediction=z@np.asarray(c['beta']); target=np.roll(run['label'],15)
    s=slice(1500,4500); wash=slice(4700,6000)
    err=(prediction-target)**2
    obs=run['observed'][s]
    fft=np.abs(np.fft.rfft(obs-obs.mean()))**2; fft=fft[1:]; prob=fft/(fft.sum()+1e-15)
    spectral=float(-np.sum(prob*np.log(prob+1e-15))/np.log(len(prob)))
    return {'tracking_mse':float(err[s].mean()),
      'accuracy':float(np.mean((prediction[s]>0)==(target[s]>0))),
      'rate_error':float(np.mean((run['rate'][s]-c['rate'])**2)),
      'entropy':float(np.mean([permutation_entropy(obs[k:k+100]) for k in range(0,len(obs)-99,100)])),
      'spectral_entropy':spectral,
      'saturation_fraction':float(np.mean((e[s]<.02)|(e[s]>.98))),
      'control_energy':float(np.mean(run['u'][s]**2)),
      'washout_mse':float(err[wash].mean()),
      'weight_change':float(run['drift'][4499]),
      'washout_weight_change':float(run['drift'][-1]),
      'cap_events':int(run['cap_events'])}
