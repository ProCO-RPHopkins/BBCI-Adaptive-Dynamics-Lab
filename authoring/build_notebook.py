from pathlib import Path
import json,importlib.metadata,platform
import nbformat as nbf
from nbclient import NotebookClient
from jupyter_client import KernelManager
import sys
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'research'
OUT=ROOT/'build/generated';OUT.mkdir(parents=True,exist_ok=True)
nb=nbf.v4.new_notebook();cells=[]
def md(s):cells.append(nbf.v4.new_markdown_cell(s))
def code(s,hidden=False):
    c=nbf.v4.new_code_cell(s)
    if hidden:c.metadata['jupyter']={'source_hidden':True}
    cells.append(c)
md('# Entropy-informed feedback: executable research notebook\n\nPrepared for Ryan Hopkins · 7 September 2026\n\nThis self-contained notebook reruns a synthetic individual and displays the recorded 1,296-run benchmark. The [interactive brain lab](https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site) provides a 3D browser interface.\n\n**Research scope:** no patient data, diagnosis, stimulation dose or demonstrated therapy. A lower tracking error is an engineering result, not a clinical benefit.\n\nInstall the accompanying `requirements.txt` in Python 3.12, or install NumPy, Numba, SciPy, Matplotlib, JupyterLab and ipykernel. The full benchmark is reproduced using `python run_experiments.py` in the research package.')
md('## 1. Executable model\n\nThe following collapsed cell contains the complete model. It is the package implementation with notebook compilation caching disabled. See Wilson and Cowan (1972), https://doi.org/10.1016/S0006-3495(72)86068-5, and Bandt and Pompe (2002), https://doi.org/10.1103/PhysRevLett.88.174102. All parameter choices in this benchmark are synthetic.')
code((P/'bbci/model.py').read_text().replace('@njit(cache=True)','@njit(cache=False)'),True)
md('## 2. Choose a synthetic individual and observation conditions\n\nEdit these parameters and run all subsequent cells. The reference is calibrated separately. Increasing noise, adding delay, or changing gain after calibration may undermine the feedback assumption. No parameter is a physical device dose.')
code("individual = 0\nseed = 100\nmeasurement_noise = 0.001\nextra_delay_seconds = 0\nartifact_scale = 0.0\nplasticity_rate = 0.0\nperson = Person(individual)\ncalibration = calibrate(person, seed=710 + 11*individual)\nprint({k:round(calibration[k],5) for k in ('rate','entropy','slope','fixed')})")
md('## 3. Run a six-strategy comparison\n\nThe yoked input comes from the next synthetic individual. One-person yoked energy need not equal one-person combined energy; the complete cyclic benchmark matches energy in aggregate.')
code("runs = {}\noptions = dict(measurement_noise=measurement_noise, delay=extra_delay_seconds, artifact=artifact_scale, plasticity=plasticity_rate)\nfor arm in ARMS[:-1]:\n    runs[arm] = simulate(person, arm, seed=seed, calibration=calibration, **options)\ndonor = Person((individual+1)%24)\ndonor_cal = calibrate(donor, seed=710 + 11*donor.index)\ndonor_run = simulate(donor, 'combined', seed=seed, calibration=donor_cal, **options)\nreplay = np.array([donor_run['u'][min((k+1)*100,5999)] for k in range(60)])\nruns['yoked'] = simulate(person,'yoked',seed=seed,calibration=calibration,replay=replay,**options)\nmetrics = {a:evaluate(r,calibration) for a,r in runs.items()}\nprint(f\"{'Strategy':<12} {'Tracking MSE':>13} {'Accuracy':>10} {'Energy':>10}\")\nfor a,m in metrics.items():\n    print(f\"{a:<12} {m['tracking_mse']:13.3f} {m['accuracy']:10.3%} {m['control_energy']:10.4f}\")")
md('## 4. Inspect the same run from three perspectives\n\nEntropy, neural activity and applied input answer different questions. The input phases are model perturbations, not diagnosed clinical states.')
code("import matplotlib.pyplot as plt\nplt.rcParams.update({'figure.dpi':110,'font.size':11,'axes.spines.top':False,'axes.spines.right':False})\nfig,axes=plt.subplots(3,1,figsize=(11,7),sharex=True)\ntime=np.arange(6000)/100\ncolors={'sham':'#8794a1','rate':'#386ba6','combined':'#008f94'}\nfor ax,key,label in zip(axes,['rate','entropy_online','u'],['Mean activity','Permutation entropy','Input (model units)']):\n    for a in colors: ax.plot(time,runs[a][key],label=a,color=colors[a],lw=1.5)\n    ax.axvspan(15,30,color='#d39147',alpha=.09);ax.axvspan(30,45,color='#806bb0',alpha=.09)\n    ax.set_ylabel(label);ax.grid(alpha=.12)\naxes[0].legend(ncol=3);axes[-1].set_xlabel('Time (s)');fig.tight_layout();plt.show()")
md('## 5. Recorded complete benchmark\n\nThe next cell embeds the aggregate output of the completed 1,296-run Python study, including the source hash. These results are **recorded**, not recomputed by this notebook. Recompute them using the package script. Intervals resample synthetic individuals after averaging seeds.')
summary=(P/'results/summary.json').read_text()
code('import json\nstudy = json.loads('+repr(summary)+')\nprint("Recorded evaluations:",study["n_runs"])\nprint("Model SHA-256:",study["model_sha256"])\nprint("Held-out baseline accuracy:",study["validation"]["heldout_baseline_accuracy"])',True)
code("fig,axes=plt.subplots(1,2,figsize=(11,4))\nfor ax,key,factor,label in zip(axes,['tracking_mse','accuracy'],[1,100],['Tracking MSE','Accuracy (%)']):\n    for i,a in enumerate(ARMS):\n        m,lo,hi=study['summary']['nominal_'+a][key]\n        ax.errorbar(i,m*factor,yerr=[[factor*(m-lo)],[factor*(hi-m)]],fmt='o',capsize=4,color='#008f94')\n    ax.set_xticks(range(6),ARMS,rotation=30);ax.set_ylabel(label);ax.grid(axis='y',alpha=.15)\naxes[1].axhline(50,ls=':',color='gray');fig.tight_layout();plt.show()")
md('## 6. Does the entropy term survive observation stress?\n\nNegative differences mean lower error with combined feedback; positive differences mean higher error. The clean-measurement advantage did not restore binary task accuracy. These intervals cannot be interpreted as treatment-effect uncertainty in patients.')
code("for condition in ('nominal','delay_2s','sensor_noise','stimulation_artifact','plasticity'):\n    mean,lo,hi=study['contrasts'][condition+'_combined_minus_rate']['tracking_mse']\n    print(f'{condition:24s} {mean:+.3f}  [{lo:+.3f}, {hi:+.3f}]')")
md('## 7. Plasticity is a specified rule, not a clinical finding\n\nHere the covariance term stops at 45 seconds and weights relax toward their starting values with a 20-second time constant. Remaining changes must not be described as demonstrated durable human rewiring.')
code("plastic_run = simulate(person,'combined',seed=seed,calibration=calibration,plasticity=.15)\nfig,ax=plt.subplots(figsize=(10,3));ax.plot(time,100*plastic_run['drift'],color='#806bb0');ax.axvline(45,ls=':',color='gray');ax.set(xlabel='Time (s)',ylabel='Relative weight change (%)');plt.show()\nprint('Observed washout ratio:',plastic_run['drift'][-1]/plastic_run['drift'][4499])\nprint('Prescribed approximate ratio:',np.exp(-15/20))")
md('## 8. Minimal local checks and next experiments\n\nThe full package adds 13 verification checks, including an independent ODE solver comparison. Useful next tests include equally optimized energy-matched controllers, a realistic observation model, held-out session calibration, and empirical tasks selected with autistic participants. The current simulation does not establish that entropy is a causal mediator of benefit.')
code("assert permutation_entropy(np.arange(100.)) == 0\nassert 0 <= permutation_entropy(np.random.default_rng(1).normal(size=1000)) <= 1\nassert abs(runs['combined']['u']).max() <= .600000001\nassert np.array_equal(runs['combined']['label'],runs['sham']['label'])\nprint('Local estimator, input-bound and task-stream checks passed.')")
md('## Sources and reproducibility\n\nThe accompanying `references.bib`, evidence ledger and manuscript contain the full 22-source bibliography. Key context: [Ilioska et al., 2026](https://doi.org/10.1038/s44220-026-00656-y); [Stoliker et al., 2026](https://doi.org/10.1038/s41586-026-10910-z); [Tan et al., 2026](https://doi.org/10.1136/bmj-2025-086295). None supplies an autism-specific entropy target for this model.\n\nThe benchmark was exploratory, including pilot parameter refinement. No clinical study or preregistration is claimed. An independent human author review is required before publication.')
nb.cells=cells;nb.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':platform.python_version()}}
path=OUT/'BBCI_Research_Notebook.ipynb';nbf.write(nb,path)
# Execute the real code cells in-process; this environment disallows kernel sockets.
# Capture actual stdout and Matplotlib output without fabricating notebook results.
import io,contextlib,base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
namespace={'__name__':'__main__'}
count=0
for cell in nb.cells:
    if cell.cell_type!='code':continue
    count+=1;cell.execution_count=count;cell.outputs=[]
    def capture_show(*args,**kwargs):
        for number in plt.get_fignums():
            fig=plt.figure(number);buf=io.BytesIO();fig.savefig(buf,format='png',bbox_inches='tight')
            cell.outputs.append(nbf.v4.new_output('display_data',data={'image/png':base64.b64encode(buf.getvalue()).decode(),'text/plain':'<Matplotlib figure>'}))
        plt.close('all')
    plt.show=capture_show
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):exec(compile(cell.source,f'<notebook-cell-{count}>','exec'),namespace)
    if stream.getvalue():cell.outputs.append(nbf.v4.new_output('stream',name='stdout',text=stream.getvalue()))
nb.metadata['execution_method']='Code cells executed with Python in-process and actual captured outputs; Jupyter kernel transport unavailable in the preparation environment.'

nbf.write(nb,path)
packages=['numpy','numba','scipy','matplotlib','nbformat','nbclient','ipykernel','jupyterlab']
versions={}
for p in packages:
    try:versions[p]=importlib.metadata.version(p)
    except importlib.metadata.PackageNotFoundError:pass
(OUT/'notebook-requirements.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
(OUT/'notebook-environment.json').write_text(json.dumps({'python':platform.python_version(),'platform':platform.platform(),'packages':versions},indent=2))
print('Executed',len([c for c in cells if c.cell_type=='code']),'code cells; saved portable notebook and dependency versions.')
