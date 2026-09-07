"""Render recorded synthetic dynamics on the included cortical display template."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/readme'
OUT.mkdir(parents=True, exist_ok=True)
brain = json.loads((ROOT / 'lab/dist/brain.json').read_text())
web = json.loads((ROOT / 'lab/dist/web_data.json').read_text())
run = web['examples']['0_combined']
activity = np.asarray(run['E'])
time = np.arange(len(activity)) / 20
control = np.asarray(run['u'])
bg, ink, muted, teal, amber = '#081827', '#e5eef2', '#9cb1bf', '#58d4c4', '#e5b465'
plt.rcParams.update({'font.family':'DejaVu Sans', 'text.color':ink,
    'axes.labelcolor':muted, 'xtick.color':muted, 'ytick.color':muted,
    'axes.edgecolor':'#294354', 'font.size':10})
cmap = LinearSegmentedColormap.from_list('activity', ['#274159','#237685',teal,'#f2d79c'])
# The same scale applies throughout the animation; no frame-wise normalization.
norm = Normalize(vmin=0, vmax=.4)
fig = plt.figure(figsize=(10,5.3), dpi=100, facecolor=bg)
fig.text(.055,.93,'A BRAIN IN THE LOOP',fontsize=18,weight='bold')
fig.text(.055,.88,'Recorded model output · Individual 01 · Rate + entropy',color=muted,fontsize=10)
ax = fig.add_axes([.03,.12,.43,.71],facecolor=bg)
surfaces = []
for side in ('left','right'):
    data = brain[side]
    vertices = np.asarray(data['vertices']).reshape(-1,3)
    faces = np.asarray(data['faces']).reshape(-1,3)
    triangles = vertices[faces]
    order = np.argsort(triangles[:,:,2].mean(axis=1))
    triangles = triangles[order]
    regions = np.asarray(data['regions'])[faces][order]
    normal = np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
    normal /= np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12)
    shade = .7 + .3*np.abs(normal @ np.array([.2,.3,.93]))
    collection = PolyCollection(triangles[:,:,:2],edgecolors='none',rasterized=True)
    ax.add_collection(collection)
    surfaces.append((collection,regions,shade))
ax.set(xlim=(-85,85),ylim=(-115,88),aspect='equal');ax.axis('off')
ax.text(-68,65,'L',color=muted,fontsize=10);ax.text(65,65,'R',color=muted,fontsize=10)
fig.text(.055,.105,'Template cortex / illustrative populations',fontsize=9,color=muted)
fig.text(.055,.065,'SYNTHETIC DATA · NOT A CLINICAL EFFECT',fontsize=9,color=amber)
trace = fig.add_axes([.53,.42,.42,.31],facecolor=bg)
trace.plot(time,activity.mean(axis=1),color=teal,lw=1.6)
trace.set(xlim=(0,60),ylabel='Mean activity')
inp = fig.add_axes([.53,.20,.42,.16],facecolor=bg)
inp.plot(time,control,color=amber,lw=1.6)
inp.set(xlim=(0,60),ylim=(-.65,.65),ylabel='Feedback input',xlabel='Model time (s)')
for chart in (trace,inp):
    chart.spines[['top','right']].set_visible(False)
    chart.grid(axis='y',color='#294354',alpha=.35)
    chart.set_xticks([0,15,30,45,60])
    for lo,hi,color in [(15,30,teal),(30,45,amber)]:chart.axvspan(lo,hi,color=color,alpha=.055)
    for t in [15,30,45]:chart.axvline(t,color=muted,lw=.6,alpha=.3)
cursors = [chart.axvline(0,color=ink,lw=1.1,alpha=.8) for chart in (trace,inp)]
phase = fig.text(.53,.80,'BASELINE',fontsize=12,weight='bold',color=teal)
clock = fig.text(.95,.80,'0.0 s',fontsize=12,ha='right',color=muted)
fig.text(.53,.065,'Fixed activity color scale: 0–0.4 model units',fontsize=9,color=muted)
def update(frame):
    index = min(int(frame*20),len(activity)-1)
    for collection,regions,shade in surfaces:
        colors = cmap(norm(activity[index][regions].mean(axis=1)))
        colors[:,:3] *= shade[:,None]
        collection.set_facecolors(colors)
    current=time[index]
    for cursor in cursors:cursor.set_xdata([current,current])
    phase.set_text('BASELINE' if current<15 else 'CONTEXT A' if current<30 else 'CONTEXT B' if current<45 else 'WASHOUT')
    clock.set_text(f'{current:.1f} s')
    return [phase,clock,*cursors]
animation = FuncAnimation(fig,update,frames=range(61),interval=180,blit=False)
animation.save(OUT/'dynamics.gif',writer=PillowWriter(fps=6))
update(22);fig.savefig(OUT/'dynamics-preview.png',facecolor=bg)
plt.close(fig)
print('Created dynamics.gif from the recorded 0_combined example.')
