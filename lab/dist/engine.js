// Independent JavaScript port of bbci/model.py; dimensionless synthetic dynamics.
export const arms=['sham','fixed','rate','entropy','combined','yoked'];
export function pe(x,lag=2){let counts=new Float64Array(6),total=x.length-2*lag;if(total<1)return 0;for(let t=0;t<total;t++){let a=x[t],b=x[t+lag],c=x[t+2*lag],k;if(a<=b)k=b<=c?0:a<=c?1:4;else k=a<=c?2:b<=c?3:5;counts[k]++}let h=0;for(let z of counts)if(z){let p=z/total;h-=p*Math.log(p)}return h/Math.log(6)}
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export function simulate(p,arm='combined',options={}){
 const {gain=p.gain,disturbance=p.disturbance,seed=100,measurement_noise=.001,delay=0,artifact=0,plasticity=0,amplitude=.6,dt=.002}=options;
 const c=p.calibration,n=16,steps=Math.round(60/dt),stride=Math.round(.01/dt),window=100;
 let state=seed>>>0;const rng=()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return(state+.5)/4294967296};
 const normal=()=>Math.sqrt(-2*Math.log(rng()))*Math.cos(2*Math.PI*rng());
 let E=Array(n).fill(.1),I=Array(n).fill(.1),noise=Array(n).fill(0),avg=Array(n).fill(.1),W=p.W.map(r=>r.slice());
 let u=0,h=0,label=1,q=0;const out={E:[],observed:[],label:[],u:[],entropy_online:[],drift:[],rate:[]};
 for(let t=0;t<steps;t++){
  const sec=t*dt;if(t%Math.round(.5/dt)===0)label=rng()>.5?1:-1;
  let perturb=sec>=15&&sec<45?disturbance*(sec<30?1:-.6):0;
  for(let i=0;i<n;i++)noise[i]+=-dt/.15*noise[i]+.04*Math.sqrt(2*dt/.15)*normal();
  let en=Array(n),inn=Array(n);
  for(let i=0;i<n;i++){
   let network=0;for(let j=0;j<n;j++)network+=W[i][j]*E[j];
   const task=i%8<2?.6*label:0;
   const a=gain*(p.w_ee[i]*E[i]-p.w_ei[i]*I[i]+p.coupling*network+p.drive+task+perturb+p.field[i]*u+noise[i]-2.5);
   const b=gain*(10*E[i]-2*I[i]-3);
   en[i]=E[i]+dt/.04*(-E[i]+1/(1+Math.exp(-clamp(a,-50,50))));
   inn[i]=I[i]+dt/.08*(-I[i]+1/(1+Math.exp(-clamp(b,-50,50))));
  }E=en;I=inn;
  for(let i=0;i<n;i++)avg[i]+=dt/2*(E[i]-avg[i]);
  if(plasticity>0)for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j){let learn=sec<45?plasticity*(E[i]-avg[i])*(E[j]-avg[j]):0;W[i][j]=clamp(W[i][j]+dt*(learn-(W[i][j]-p.W[i][j])/20),.25*p.W[i][j],2*p.W[i][j]);}
  if((t+1)%stride===0){
   let m=E.reduce((a,b)=>a+b,0)/n,dw=0,denom=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++){dw+=(W[i][j]-p.W[i][j])**2;denom+=p.W[i][j]**2;}
   out.E.push(E.slice());out.observed.push(m+measurement_noise*normal()+artifact*u*Math.sin(2*Math.PI*37*sec));out.label.push(label);out.u.push(u);out.rate.push(m);out.drift.push(Math.sqrt(dw/denom));out.entropy_online.push(h);
   if((q+1)%window===0){let end=q+1-delay*window;if(end>=window){let hist=out.observed.slice(end-window,end);h=pe(hist);let rm=hist.reduce((a,b)=>a+b,0)/window,er=c.rate-rm,eh=c.entropy-h;
    let du=Math.abs(c.slope)<.01?0:clamp(eh/c.slope,-.35,.35),rate=4*er,proposal=0;
    if(arm==='fixed')proposal=c.fixed;else if(arm==='rate')proposal=rate;else if(arm==='entropy')proposal=.5*u+.5*du;else if(arm==='combined')proposal=rate+.3*du;
    if(sec<10||sec>=45)proposal=0;u=clamp(u+clamp(proposal-u,-.15,.15),-amplitude,amplitude);
   }}q++;
  }
 }return out;
}
export function metrics(r,c){const ids=c.readout_indices;let err=0,acc=0,energy=0;for(let t=1500;t<4500;t++){let pred=ids.reduce((s,i,j)=>s+(r.E[t][i]-c.center[j])/c.scale[j]*c.beta[j],0),target=r.label[t-15];err+=(pred-target)**2;acc+=(pred>0)===(target>0)?1:0;energy+=r.u[t]**2;}return{mse:err/3000,accuracy:acc/3000,energy:energy/3000}}
