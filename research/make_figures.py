"""Regenerate manuscript and presentation figures from the saved raw results."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT=Path(__file__).resolve().parent
F=ROOT/'figures';F.mkdir(exist_ok=True)
D=json.loads((ROOT/'results/summary.json').read_text())
rows=list(csv.DictReader((ROOT/'results/all_runs.csv').open()))
C={'sham':'#7e8996','fixed':'#d28b37','rate':'#386ba6','entropy':'#9474b0','combined':'#078c91','yoked':'#a44966'}
names={'sham':'No input','fixed':'Fixed','rate':'Rate','entropy':'Entropy','combined':'Rate + entropy','yoked':'Yoked'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#243345','text.color':'#172a3c','axes.titleweight':'bold','savefig.facecolor':'white','lines.linewidth':2})
def save(fig,name):
    # Atomic writes prevent readers from observing partially written figure files.
    png_tmp=F/(name+'.tmp.png');fig.savefig(png_tmp,dpi=300,bbox_inches='tight')
    png_tmp.replace(F/(name+'.png'))
    with Image.open(F/(name+'.png')) as im:rgb=im.convert('RGB')
    tif_tmp=F/(name+'.tmp.tiff');rgb.save(tif_tmp,format='TIFF',compression='tiff_lzw',dpi=(300,300))
    with Image.open(tif_tmp) as im:im.load()
    tif_tmp.replace(F/(name+'.tiff'))
    pdf_tmp=F/(name+'.tmp.pdf');fig.savefig(pdf_tmp,bbox_inches='tight');pdf_tmp.replace(F/(name+'.pdf'))
    plt.close(fig)

fig,ax=plt.subplots(figsize=(7.6,4.1));ax.set_xlim(0,10);ax.set_ylim(-1,5);ax.axis('off')
def box(x,y,w,h,title,body,color='#edf4f7'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.1',facecolor=color,edgecolor='#426779',lw=2))
    ax.text(x+w/2,y+h-.25,title,ha='center',va='top',weight='bold',fontsize=11)
    ax.text(x+w/2,y+.43,body,ha='center',va='center',fontsize=9.5,linespacing=1.35)
def arrow(a,b):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,lw=2,color='#426779'))
box(.2,2.65,2.6,1.7,'Synthetic circuit','16 E/I populations\nTask + disturbance')
box(3.5,2.65,2.6,1.7,'Observation','Population average\nNoise / artifact')
box(6.8,2.65,2.7,1.7,'Feedback','Rate + calibrated\nentropy correction')
arrow((2.9,3.5),(3.4,3.5));arrow((6.2,3.5),(6.7,3.5))
arrow((8.2,2.55),(8.2,1.7));arrow((6.7,1),(2.9,1));arrow((1.5,1.65),(1.5,2.55))
box(.2,.3,2.6,1.3,'Bounded actuator','Dimensionless current')
box(6.8,.3,2.7,1.3,'Constraint','Amplitude / slew limits')
ax.text(5,-.6,'Independent task readout evaluates success.\nEntropy matching is not the outcome.',ha='center',fontsize=10,weight='bold')
save(fig,'Figure_1_Control_Architecture')

fig,axes=plt.subplots(1,2,figsize=(7.6,3.7),gridspec_kw={'width_ratios':[1.2,1]})
arms=list(names)
for ax,metric,title in zip(axes,['tracking_mse','accuracy'],['A  Continuous tracking error','B  Binary task accuracy']):
    for i,a in enumerate(arms):
        m,lo,hi=D['summary']['nominal_'+a][metric]
        factor=100 if metric=='accuracy' else 1
        ax.errorbar(m*factor,i,xerr=np.array([[m-lo],[hi-m]])*factor,fmt='o',ms=6,color=C[a],capsize=3,lw=2)
    ax.set_yticks(range(6),[names[a] for a in arms] if metric=='tracking_mse' else ['']*6)
    ax.invert_yaxis();ax.set_title(title,loc='left',fontsize=11)
    ax.set_xlabel('Mean squared error (lower is better)' if metric=='tracking_mse' else 'Correct classifications (%)')
    ax.grid(axis='x',alpha=.16)
    if metric=='accuracy':ax.axvline(50,ls=':',c='#687382',lw=2);ax.set_xlim(40,88);ax.axvspan(78.479,82.131,color='#078c91',alpha=.12);ax.text(83,2.5,'Held-out baseline',rotation=90,ha='left',va='center',fontsize=9.5)
fig.subplots_adjust(wspace=.12,bottom=.23)
fig.text(.5,.015,'24 synthetic individuals × 3 seeds; intervals resample individuals (4,000 bootstrap draws).',ha='center',fontsize=9.5)
save(fig,'Figure_2_Benchmark')

fig,ax=plt.subplots(figsize=(7.6,3.5))
scenarios={'nominal':'Clean measurement','delay_2s':'Two-second delay','sensor_noise':'Sensor noise (SD 0.05)','stimulation_artifact':'Input artifact (scale 0.20)','plasticity':'Bounded plasticity'}
for i,(key,name) in enumerate(scenarios.items()):
    m,lo,hi=D['contrasts'][key+'_combined_minus_rate']['tracking_mse']
    col='#078c91' if hi<0 else '#a44966' if lo>0 else '#6c7582'
    ax.errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt='o',color=col,capsize=4,ms=7,lw=2)
    ax.text(15.5,i,f'{m:+.2f} [{lo:+.2f}, {hi:+.2f}]',va='center',fontsize=10)
ax.axvline(0,color='#75808b',ls=':',lw=2);ax.set_yticks(range(5),scenarios.values());ax.invert_yaxis();ax.set_xlim(-8,32);ax.set_xticks([-5,0,5,10]);ax.set_xlabel('Tracking MSE: combined feedback minus rate feedback');ax.set_title('Incremental value changes with measurement conditions',loc='left',fontsize=12);ax.grid(axis='x',alpha=.15)
ax.text(.02,-.3,'Negative: lower error with entropy. Positive: higher error with entropy.\nIntervals describe this synthetic ensemble; they are not clinical confidence intervals.',transform=ax.transAxes,fontsize=10)
save(fig,'Figure_3_Robustness')

g=list(csv.DictReader((ROOT/'results/gain_sweep.csv').open()));s=list(csv.DictReader((ROOT/'results/phase_surrogates.csv').open()))
fig,axes=plt.subplots(1,2,figsize=(7.6,3.5))
for person in range(8):
    rr=[r for r in g if int(r['person'])==person]
    axes[0].plot([float(r['entropy']) for r in rr],[100*float(r['accuracy']) for r in rr],'-o',ms=3,alpha=.65,label=str(person))
    ss=[r for r in s if int(r['person'])==person]
    original=float(ss[0]['original']);v=[float(r['surrogate']) for r in ss]
    axes[1].plot([person,person],[min(v),max(v)],c='#8ea2b2',lw=2)
    axes[1].plot(person,np.mean(v),'o',c='#078c91',ms=5)
    axes[1].plot(person,original,'x',c='#a44966',ms=7,mew=2)
axes[0].set(xlabel='Mean online permutation entropy',ylabel='Task accuracy (%)',title='A  Gain sweep')
axes[0].title.set_fontsize(10);axes[0].grid(alpha=.12)
axes[1].set(xlabel='Synthetic individual',ylabel='Whole-record permutation entropy',title='B  Phase surrogates',xticks=range(8));axes[1].title.set_fontsize(10)
axes[1].plot([],[],'x',c='#a44966',label='Original record');axes[1].plot([],[],'o',c='#078c91',label='Surrogates: mean / range');axes[1].legend(fontsize=9.5,loc='lower left',frameon=False)
fig.tight_layout(w_pad=1.5);save(fig,'Figure_4_Entropy_Diagnostics')

# A large-label single-panel derivative for projection.
plt.rcParams.update({'font.size':16})
fig,ax=plt.subplots(figsize=(11,4.8))
for i,(key,name) in enumerate(list(scenarios.items())[:4]):
    m,lo,hi=D['contrasts'][key+'_combined_minus_rate']['tracking_mse'];col='#078c91' if hi<0 else '#a44966' if lo>0 else '#6c7582'
    ax.errorbar(m,i,xerr=[[m-lo],[hi-m]],fmt='o',color=col,capsize=5,ms=10,lw=3)
ax.axvline(0,ls=':',color='#8794a1',lw=2);ax.set_yticks(range(4),list(scenarios.values())[:4]);ax.invert_yaxis();ax.set_xlabel('Change in tracking error after adding entropy feedback');ax.grid(axis='x',alpha=.15);fig.tight_layout();save(fig,'Slide_Robustness')
print('Created four manuscript figures and one presentation figure, each as PNG, TIFF and PDF.')
