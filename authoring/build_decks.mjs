process.on('uncaughtException',e=>{console.error('DECK ERROR:',e.message);process.exitCode=1;});
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'), OUT=path.join(ROOT,'build/generated');
await fs.mkdir(OUT,{recursive:true});
const fig=path.join(ROOT,'research/figures');
const artBrain=path.join(ROOT,'assets/illustrations/exec-91f3bdac-674b-4ecd-932b-61449e80bb7e.png');
const artPerson=path.join(ROOT,'assets/illustrations/exec-7c2793a6-5b42-4c89-b62a-3715b2d8ae4c.png');
const site='https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site';
const DOI={hetero:'https://doi.org/10.1038/s44220-026-00656-y',context:'https://doi.org/10.1038/s41586-026-10910-z',entropy:'https://doi.org/10.3389/fpsyt.2025.1505297',tan:'https://doi.org/10.1136/bmj-2025-086295',ni23:'https://doi.org/10.1002/aur.2954',ni24:'https://doi.org/10.1017/S0033291724001387',oehrn:'https://doi.org/10.1038/s41591-024-03196-z',flesher:'https://doi.org/10.1126/science.abd0380',participate:'https://doi.org/10.1177/1362361318786721',wilson:'https://doi.org/10.1016/S0006-3495(72)86068-5',bandt:'https://doi.org/10.1103/PhysRevLett.88.174102',herzog:'https://doi.org/10.1038/s41598-023-32649-7'};
const research={bg:'#F5F7F8',ink:'#11283A',muted:'#526776',accent:'#008C94',rule:'#CCD8DE',dark:'#081827',light:'#E4F4F3'};
const opportunity={bg:'#15162D',ink:'#F4F2FF',muted:'#B6B5CC',accent:'#76E1CB',rule:'#3E405A',dark:'#101026',light:'#24233D'};
let number=0,theme,pres;
function shape(s,x,y,w,h,fill,geometry='rect',stroke='none',sw=0){return s.shapes.add({geometry,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}});}
function text(s,str,x,y,w,h,size=26,color=theme.ink,bold=false,align='left'){
  const a=shape(s,x,y,w,h,'none','textbox');a.text=str;
  a.text.style={typeface:'Aptos',fontSize:size,color,bold,alignment:align,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};return a;
}
function line(s,x,y,w,color=theme.rule){shape(s,x,y,w,1.4,color);}
async function picture(s,file,x,y,w,h,fit='contain'){
  const b=await fs.readFile(file);return s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt:path.basename(file).includes('exec-')?'AI-generated conceptual illustration; not patient data':'Chart generated from the accompanying synthetic benchmark',position:{left:x,top:y,width:w,height:h},fit});
}
function base(title,kicker='RESEARCH / BBCI',citation='',dark=false){
  const s=pres.slides.add();number++;s.background.fill=dark?theme.dark:theme.bg;
  const color=dark?'#F4F8FB':theme.ink;
  text(s,kicker,64,37,1000,26,17,dark?'#7BD4D7':theme.accent,true);
  text(s,title,64,91,1152,116,48,color,true);
  line(s,64,661,1152,dark?'#304456':theme.rule);
  text(s,citation||'Hopkins · Exploratory computational research · September 2026',64,677,1060,26,15,dark?'#9AAEBB':theme.muted);
  text(s,String(number).padStart(2,'0'),1160,675,56,26,17,dark?'#B8CBD6':theme.muted,false,'right');return s;
}
function notes(s,script,sources=[],extra=''){
  const sourceLines=sources.map(u=>'- '+u).join('\n');
  s.speakerNotes.textFrame.setText(script+(extra?'\n\n'+extra:'')+'\n\n[Sources]\n'+sourceLines+'\n[/Sources]');
}
function rows(s,items,{x=64,y=240,w=1152,gap=125,labelWidth=340}={}){
  items.forEach(([label,body],i)=>{let yy=y+i*gap;line(s,x,yy-15,w);if(labelWidth===0){text(s,label,x,yy,w,48,29,theme.accent,true);text(s,body,x,yy+49,w,gap-55,23,theme.ink);}else{text(s,label,x,yy,labelWidth-24,70,32,theme.accent,true);text(s,body,x+labelWidth,yy,w-labelWidth,95,27,theme.ink);}});
}
function three(s,items,{y=250}={}){
  items.forEach(([a,b],i)=>{let x=64+i*400;text(s,String(i+1).padStart(2,'0'),x,y,100,60,48,theme.accent);line(s,x,y+77,350);text(s,a,x,y+104,345,86,32,theme.ink,true);text(s,b,x,y+210,345,145,25,theme.muted);});
}
function table(s,headers,entries,widths,{y=226,rowH=57}={}){
  let x=64;headers.forEach((h,i)=>{text(s,h,x,y,widths[i]-18,40,22,theme.accent,true);x+=widths[i];});line(s,64,y+45,1152);
  entries.forEach((row,j)=>{let xx=64,yy=y+62+j*rowH;row.forEach((v,i)=>{text(s,v,xx,yy,widths[i]-18,rowH-5,23,theme.ink,i===0);xx+=widths[i];});if(j<entries.length-1)line(s,64,yy+rowH-12,1152);});
}
function flow(s,labels,subtitle){
  const pos=[[64,250],[470,250],[876,250],[876,448],[64,448]];
  for(let i=0;i<5;i++){let [x,y]=pos[i];shape(s,x,y,340,112,theme.light);text(s,labels[i][0],x+20,y+15,300,42,29,theme.ink,true);text(s,labels[i][1],x+20,y+60,300,44,22,theme.muted);}
  shape(s,417,283,40,28,theme.accent,'rightArrow');shape(s,823,283,40,28,theme.accent,'rightArrow');shape(s,1025,380,28,45,theme.accent,'downArrow');shape(s,430,485,420,28,theme.accent,'leftArrow');shape(s,215,380,28,45,theme.accent,'upArrow');
  text(s,subtitle,441,554,390,65,24,theme.accent,true,'center');
}
async function cover(title,sub,file,credit){
  const s=pres.slides.add();number++;s.background.fill=theme.dark;await picture(s,file,0,0,1280,720,'cover');
  text(s,'RYAN HOPKINS / SEPTEMBER 2026',64,51,620,30,18,'#89D8DB',true);
  text(s,title,64,173,615,285,69,'#F8FBFF',true);
  text(s,sub,64,480,520,135,27,'#C6D7E3');
  text(s,credit,64,660,1140,26,16,'#ABC0CD');return s;
}
async function exportDeck(stem){
  const dir=path.join(OUT,'previews',stem);await fs.mkdir(dir,{recursive:true});
  const scripts=[];
  for(let [i,s] of pres.slides.items.entries()){
    let name='slide-'+String(i+1).padStart(2,'0');
    const png=await pres.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(dir,name+'.png'),new Uint8Array(await png.arrayBuffer()));
    const layout=await s.export({format:'layout'});await fs.writeFile(path.join(dir,name+'.layout.json'),await layout.text());
    scripts.push({slide:i+1,notes:s.speakerNotes.textFrame.toString?.()||''});
    process.stdout.write(stem+' '+(i+1)+'/'+pres.slides.items.length+' rendered\n');
  }
  const pptx=await PresentationFile.exportPptx(pres);await pptx.save(path.join(OUT,stem+'.pptx'));
  await fs.writeFile(path.join(dir,'presentation.json'),JSON.stringify(pres.toProto()));
  console.log('Saved',stem+'.pptx');
}

// Communication job: a general audience understands the hypothesis, the actual
// computational result and the evidence needed to move toward a useful therapy.
theme=research;pres=Presentation.create({slideSize:{width:1280,height:720}});number=0;
{
let s=await cover('A brain\nin the loop','Testing entropy-informed feedback\nfor autism neuromodulation research',artBrain,'Scientific explanation · Synthetic findings, clinical context and next steps');
notes(s,'This presentation explains a research idea and the experiment built to challenge it. A brain–computer interface can measure activity, and a bidirectional system can also send a signal back. The question is whether information about the variety of brain activity helps that feedback support something useful. We tested a simplified computer model and updated the clinical literature through September 2026. The results are mixed in an informative way. This is a research program, and the simulation does not demonstrate a therapy for autistic people.',[site],'Visual: AI-generated conceptual brain illustration created for this presentation. It is not a scan or an empirical connectivity map.');
s=base('Start with an outcome a person values','THE PURPOSE','Fletcher-Watson et al., 2019 · Ilioska et al., 2026');
three(s,[['A chosen goal','The participant helps define what support would be useful.'],['An individual context','Patterns can differ across people, settings and measurement scales.'],['A meaningful test','A signal change matters only if the agreed outcome improves.']]);
notes(s,'The starting point is a person’s priorities. A future intervention might be judged by a communication goal, sensory comfort or another outcome the participant chooses. Atypical brain activity is not automatically a problem to correct. Recent large-scale work also shows that heterogeneity depends on the scale at which we look. The practical implication is to measure individuals carefully and to develop the research with autistic partners. Our model uses an engineering task because it has no participants; that task must never be confused with a measure of wellbeing.',[DOI.participate,DOI.hetero]);
s=base('Entropy needs a separate success measure','THE CORE IDEA','Bandt & Pompe, 2002 · Tenev et al., 2025');
text(s,'How varied is\nthe signal?',64,239,500,140,53,theme.accent,true);text(s,'How useful is\nthe information?',674,239,540,140,53,theme.ink,true);line(s,64,419,1152);text(s,'A high score can reflect useful variety, measurement noise, or a mixture of both.',64,461,1060,100,32,theme.ink);text(s,'We therefore measure task performance independently of entropy.',64,583,1100,44,26,theme.muted);
notes(s,'Here entropy describes the predictability of short patterns in a signal. It does not score how healthy, intelligent or useful a brain is. Different complexity measures can even move in different directions in the same research setting. Our benchmark specifies one estimator, permutation entropy, and measures an independent task outcome. Think of a microphone: adding static makes a recording less predictable, but it does not improve the message. That analogy illustrates why a controller must know whether its measurement contains useful information or contamination.',[DOI.bandt,DOI.entropy]);
s=base('Recent evidence sharpens the question','EVIDENCE UPDATE','Ilioska et al., 2026 · Stoliker et al., 2026 · Tan et al., 2026');
rows(s,[['Individual differences','Large imaging studies support careful person-specific characterization.'],['Context matters','Psychedelic dynamics can show structured alignment with sensory context.'],['Protocol matters','A positive motor-cortex trial does not validate entropy-targeted feedback.']],{y:233,gap:130});
notes(s,'Three developments change how this research should be framed. Individual differences remain substantial, with more shared structure at some scales than others. New psychedelic research challenges the idea that a more varied signal is simply random disorder. And a recent autism stimulation trial reported a positive result for a specific protocol. These are useful developments, but they do not combine into proof of our proposed therapy. The bridge between a measured state, a feedback action and a meaningful outcome still has to be tested directly.',[DOI.hetero,DOI.context,DOI.tan]);
s=base('Ask whether entropy adds useful information','THE EXPERIMENT');
text(s,'Does adding entropy feedback\nimprove an independent task\nbeyond activity feedback alone?',64,225,1150,240,53,theme.ink,true);text(s,'This question can produce a positive result, a negative result, or a result that depends on measurement conditions.',64,527,1080,89,29,theme.muted);
notes(s,'The experiment focuses on the added value of one ingredient. Rate feedback already responds to mean activity. We then add a calibrated entropy term and ask whether the circuit preserves a separate input signal more accurately. We do not tell the model that higher entropy is better. Instead, the target comes from an individual reference session, and the entropy term uses a measured local response to input. This is an exploratory engineering comparison. Its outcome cannot establish which state would be desirable for a real person.',[site]);
s=base('The model keeps sensing and success separate','HOW THE LOOP WORKS','Wilson & Cowan, 1972 · Bandt & Pompe, 2002 · Accompanying Python model');
flow(s,[['Synthetic circuit','16 interacting populations'],['Noisy measurement','Average activity over time'],['Feedback rule','Activity + entropy errors'],['Input constraints','Bound amplitude and change'],['Applied input','Influences the circuit']],'Independent task readout\nchecks whether it helped');
notes(s,'The model contains interacting excitatory and inhibitory populations. Their activity produces a measurement, which can include noise and an input-related artifact. The feedback rule uses activity and entropy errors to propose an input. Numerical constraints limit that input before it returns to the circuit. A separate readout, trained on a different session, checks task performance. The distinction is essential: making the measured statistic match a reference is not the same as improving the task. These units are dimensionless and do not specify a human stimulation setting.',[DOI.wilson,DOI.bandt,site]);
s=base('Six strategies reveal different explanations','THE CONTROLS');
table(s,['Strategy','What it tests'],[['No input','What happens without feedback'],['Calibrated fixed input','Whether a simpler constant input is enough'],['Activity feedback','A simpler adaptive rule'],['Entropy feedback','The complexity term on its own'],['Activity + entropy','The incremental value of combining both'],['Yoked replay','Input from another individual, without live feedback']],[345,807],{y:216,rowH:59});
notes(s,'The comparison needs more than a no-input control. Fixed input tests whether adaptation is necessary, although it receives a different calibration opportunity in this benchmark. Activity feedback tests a simpler adaptive explanation. Entropy alone shows what the additional term can do without rate correction. The combined strategy is the main experimental arm. Yoked replay uses another individual’s input sequence, so the complete group receives matched aggregate energy without each person’s current-state feedback. No single comparator settles every explanation; together they expose several important alternatives.',[site]);
s=base('The benchmark is small enough to inspect','REPRODUCIBILITY');
for(let [i,n,label] of [[0,'24','synthetic individuals'],[1,'3','evaluation seeds'],[2,'6','nominal strategies']]){text(s,n,64+i*400,240,350,140,108,theme.accent,true);text(s,label,64+i*400,395,355,57,29,theme.ink);}
line(s,64,489,1152);text(s,'1,296 evaluation runs',64,524,575,74,43,theme.ink,true);text(s,'Plus calibration, held-out reference checks,\ngain sweeps and numerical verification.',674,527,525,89,25,theme.muted);
notes(s,'The final study evaluates 24 synthetic individuals across three random seeds. Six nominal strategies produce 432 runs. Four additional stress conditions each compare three strategies, bringing the evaluation total to 1,296. Calibration and diagnostic simulations are additional. The uncertainty intervals resample synthetic individuals after averaging their seeds. They describe this chosen ensemble, not uncertainty in a human treatment effect. The project also includes reproducibility checks and a notebook, so the result can be inspected and challenged rather than accepted from a figure alone.',[site]);
s=base('A tracking score improved under clean sensing','NOMINAL RESULT');
text(s,'−4.53',64,221,530,156,116,theme.accent,true);text(s,'change in tracking error\nwhen entropy was added',64,390,535,95,32,theme.ink);text(s,'95% synthetic interval: −6.54 to −2.83',64,519,570,47,24,theme.muted);
rows(s,[['81.36 → 76.83','Activity → activity + entropy'],['More input energy','0.0290 → 0.0465 model units'],['Fixed input: 69.94','Lower mean error; different calibration access']],{x:700,y:232,w:516,gap:130,labelWidth:0});
// Right-side comparison is authored as paired headline + detail rows.

notes(s,'In the deliberately clean measurement condition, adding entropy reduced the average continuous tracking error by about four and a half model units relative to activity feedback. The synthetic-ensemble interval was below zero. That improvement came with greater input energy. The fixed-input comparator had a lower mean error than either adaptive approach, although it had been calibrated on the disturbance distribution. This is evidence of conditional performance in a defined model. It is not a percentage improvement in a symptom score, and it does not establish that adaptive control is generally better.',[site]);
s=base('Task accuracy did not recover','THE CRUCIAL SECOND OUTCOME');
const bars=[['Held-out reference',80.2736,'#819BAE'],['Activity feedback',50.0417,'#386BA6'],['Activity + entropy',50.0333,'#008C94']];
bars.forEach(([label,value,col],i)=>{let y=246+i*111;text(s,label,64,y+9,320,54,29,theme.ink,true);shape(s,405,y,710,52,'#E3E9ED');shape(s,405,y,710*value/100,52,col);text(s,value.toFixed(2)+'%',1131,y+5,120,52,29,theme.ink,true);});
text(s,'The continuous score improved while useful sign discrimination remained near chance.',64,590,1152,50,29,theme.muted);
notes(s,'This is the result that prevents an overly positive interpretation. A fresh unperturbed session reached about 80 percent accuracy on the simple binary task. Under disturbance, both activity and combined feedback were close to 50 percent. The entropy term improved the continuous readout’s error without restoring useful sign decisions. A linear readout can change its offset or scale while making almost the same choices. Reporting only the favorable tracking score would therefore hide a major limitation. We need both measures to understand what the controller actually accomplished.',[site]);
s=base('Measurement noise can reverse the advantage','ROBUSTNESS');
await picture(s,path.join(fig,'Slide_Robustness.png'),64,213,1152,371);
text(s,'Left of zero: lower error with entropy. Right of zero: higher error with entropy.',64,604,1152,37,25,theme.muted);
notes(s,'The horizontal intervals show the extra effect of the entropy term under different observation conditions. Clean measurements favor the combined rule. With added sensor noise, the sign reverses and the combined rule has higher tracking error. Extra delay and an input-related artifact produce intervals that cross zero. These conditions were tested separately, so they are not a complete model of real recordings. The lesson is practical: a controller can respond to contamination in its measurement. Reliable sensing and a way to abstain when uncertain are part of the hypothesis, not optional refinements.',[site]);
s=base('Weight changes need a separate benefit test','PLASTICITY');
three(s,[['A specified rule','Weights change with activity covariance within explicit bounds.'],['A specified washout','After learning stops, changes decay with a chosen time constant.'],['A separate claim','Durable, useful learning in people would need its own evidence.']]);
notes(s,'The model includes an optional plasticity rule, which changes connection weights according to recent activity. This is more explicit than simply forcing two traces to become similar. However, the rule also contains an imposed relaxation toward the original weights. In a verification example, washout follows the expected decay almost exactly. That is a successful software check, but it is not evidence of lasting biological rewiring. A stronger learning claim would require an independent task improvement that persists beyond the imposed adaptation dynamics and is supported by an appropriate biological model.',[site]);
s=base('Explore the assumptions in the brain lab','INTERACTIVE MODEL');
await picture(s,artBrain,640,217,576,389,'cover');
rows(s,[['Rotate and inspect','Folded or inflated cortical anatomy'],['Change the experiment','Strategy, gain, delay, noise and plasticity'],['Check both outcomes','Watch entropy alongside task performance']],{x:64,y:232,w:535,gap:118,labelWidth:0});
const link=text(s,'Open the interactive research lab ↗',64,595,920,47,28,theme.accent,true);link.text.get('Open the interactive research lab ↗').link={uri:site,isExternal:true};
notes(s,'The companion lab lets you rotate a cortical surface, inspect synthetic populations and compare strategies. You can change measurement noise or feedback delay, rerun the same model and look at the task outcome as well as the animation. The anatomical surface is a real public template, but the connections and activity are simulated and are not a patient brain map. The artwork on this slide is conceptual; the live application contains the interactive cortical mesh. The Python package remains the main reproducible scientific record, with the browser serving as an exploratory view.',[site],'Slide artwork is AI-generated and is not a screenshot of the application.');
s=base('The next study should test the measurement','TRANSLATIONAL RESEARCH','Fletcher-Watson et al., 2019 · Proposed research sequence');
rows(s,[['Co-design the outcome','Choose a goal and acceptable burden with autistic partners.'],['Test repeatability','Check whether the signal predicts that goal across separate sessions.'],['Justify intervention testing','Proceed only when realistic models and simpler controls support the case.']],{y:231,gap:130});
notes(s,'The next empirical step should establish whether a candidate measurement is useful for an individual across time and context. It should be designed with autistic participants, with a prospectively agreed outcome and a clear way to stop if the measurement is uninformative. Model fitting would then need realistic sensing and actuation, along with comparisons against simpler controllers. A clinically governed intervention study would be a later, separate step. This sequence is a proposed research agenda, not an approved protocol, and the current simulation provides no device settings or treatment regimen.',[DOI.participate,site]);
s=base('Selected sources behind the story','READING');
const reading=[['Ilioska et al. (2026)','Individual connectivity · Nature Mental Health',DOI.hetero],['Stoliker et al. (2026)','Context and psychedelic dynamics · Nature',DOI.context],['Tan et al. (2026)','Motor-cortex stimulation trial · BMJ',DOI.tan],['Tenev et al. (2025)','Different complexity measures · Front. Psychiatry',DOI.entropy],['Wilson & Cowan (1972)','Population dynamics · Biophysical Journal',DOI.wilson],['Bandt & Pompe (2002)','Permutation entropy · Physical Review Letters',DOI.bandt]];
reading.forEach(([a,b,u],i)=>{let y=222+i*67;let t=text(s,a,64,y,390,48,25,theme.accent,true);t.text.get(a).link={uri:u,isExternal:true};text(s,b,476,y,730,50,24,theme.ink);});
notes(s,'These are selected entry points into the evidence and methods. The complete manuscript contains 22 references and the research package includes a BibTeX file and an evidence ledger describing what each source can and cannot support. The literature update used Consensus discovery followed by record retrieval and primary-source checking. It was a targeted narrative update, not a systematic review. The model findings are new synthetic outputs from the accompanying code and should be assessed separately from the clinical literature.',reading.map(r=>r[2]));
s=base('Useful feedback must earn its added complexity','THE TAKEAWAY','Hopkins · Exploratory benchmark · 2026',true);
text(s,'Measure a meaningful outcome.\nChallenge the controller.\nKeep the result reproducible.',64,237,1130,240,53,'#F0F6FA',true);text(s,'The current model identifies conditional gains and clear failure modes.\nThat is a starting point for better experiments.',64,531,1120,89,28,'#B7CBD8');
notes(s,'The central question was whether a more informative feedback loop could support a useful outcome. Our answer is conditional: entropy helped one score under clean observation, but did not restore the task and became counterproductive with greater measurement noise. That result improves the research question by making its assumptions visible. The way forward is to test reliable individual measurements, compare against simpler approaches and use outcomes chosen with the people the research hopes to support. The code and interactive model make those questions concrete enough to challenge.',[site]);
}
await exportDeck('BBCI_Research_Explained');

// Communication job: prospective collaborators understand the potential value
// and the evidence milestones for a responsible therapeutic research program.
theme=opportunity;pres=Presentation.create({slideSize:{width:1280,height:720}});number=0;
{
let s=await cover('More choice.\nLess burden.','A research vision for\nperson-specific neural support',artPerson,'Proposed approach · Potential benefits require clinical testing');
notes(s,'This is a vision for a research program that could support greater choice and lower burden for people who want that support. It is not a presentation of a proven therapy. The proposal is to study whether carefully measured brain dynamics can help a feedback system respond to a person’s context and goals. The scientific package includes a working simulation, a critical evidence update and clear failure conditions. The opportunity is to develop and test this idea with autistic partners, computational researchers and clinical experts.',[site,DOI.participate],'Visual: AI-generated fictional adult in a calm workspace. This is an illustration, not a patient, testimonial or depiction of a tested treatment.');
s=base('A valuable therapy starts with a chosen goal','THE HUMAN PURPOSE','Fletcher-Watson et al., 2019 · Illustrative goals, not demonstrated outcomes');
three(s,[['Communication','Support a personally meaningful communication task.'],['Sensory comfort','Explore support for a difficulty the participant wants to address.'],['Autonomy','Preserve choice, consent and control over participation.']]);
notes(s,'The potential value of this work should be defined by participants. The examples here are possible research goals, not claims that the proposed approach improves them today. A communication task might matter to one person, while another may prioritize sensory comfort or something entirely different. Autonomy also determines whether a system is acceptable: people need an understandable purpose and the ability to decline or stop. Meaningful involvement should shape the study question and the evaluation criteria from the beginning.',[DOI.participate]);
s=base('Feedback could respond as context changes','THE PROPOSED APPROACH');
flow(s,[['Observe','Measure a changing signal'],['Interpret','Use a personal reference'],['Decide','Use a calibrated feedback rule'],['Constrain','Stay within tested limits'],['Respond','Check the next observation']],'A participant-valued outcome\ndetermines whether it helps');
notes(s,'The proposed approach is a loop. It observes a signal, interprets that signal relative to an individual reference and chooses a constrained response. A future clinical version would need a validated recording method, an appropriate intervention and evidence that the overall loop benefits the participant. Our current software implements only a synthetic version. It demonstrates how the parts connect and how measurement errors can change the result. A person’s goal remains outside the signal statistic and is the reason to evaluate the system at all.',[site]);
s=base('The potential benefits are testable hypotheses','POTENTIAL VALUE');
table(s,['Potential benefit','What a study would need to show'],[['More relevant support','Benefit on an agreed task across changing contexts'],['Less unnecessary input','Equal or better outcomes with an acceptable input burden'],['Useful learning','Task improvements that persist beyond immediate feedback']],[424,728],{y:251,rowH:109});
text(s,'None of these benefits has been established for this proposed autism approach.',64,602,1152,43,25,theme.muted);
notes(s,'These are the potential benefits that make the research worth testing. Personalized feedback might become more relevant to changing needs. It might also reduce unnecessary input, but that is a hypothesis: our present combined controller actually uses more energy than rate feedback. A learning claim would require useful improvements that outlast the immediate intervention, rather than merely persistent simulated weights. Each benefit therefore needs its own outcome, comparator and follow-up. The goal is to make the vision measurable before treating it as a product promise.',[site]);
s=base('Brain interfaces provide engineering precedents','WHY THE TECHNOLOGY MATTERS','Flesher et al., 2021 · Oehrn et al., 2024');
rows(s,[['Return information','Tactile feedback has improved robotic-arm control in BCI research.'],['Adapt to a state','Personalized stimulation has shown feasibility in Parkinson’s disease.'],['Test a new indication','Autism applications require their own mechanism and outcome evidence.']],{y:232,gap:130});
notes(s,'There are credible engineering precedents for closing a neural loop. Sensory feedback has improved robotic-arm control, and individualized adaptive stimulation has been tested against continuous stimulation in Parkinson’s disease. These examples show that measurement and response can be integrated in useful ways in specific settings. They do not supply evidence for an autism application or an entropy target. The opportunity is to learn from their careful calibration and comparative testing while developing independent evidence for a new research question.',[DOI.flesher,DOI.oehrn]);
s=base('Neuralink illustrates a wider research frontier','INDUSTRY CONTEXT','Neuralink official trial and program pages · Company sources, checked September 2026');
three(s,[['Digital access','Investigational neural interfaces for controlling computers.'],['Assistive devices','CONVOY explores control of an external assistive robotic device.'],['Communication','Publicly described speech-restoration research programs.']]);
text(s,'These programs do not establish an entropy-targeted autism therapy.',64,614,1152,35,24,theme.muted);
notes(s,'Neuralink is a visible example of the broader effort to connect neural signals with useful tools. Its official pages describe investigational digital control, the CONVOY assistive-device study and speech-restoration research. These are company descriptions of programs, not peer-reviewed evidence for our proposal. The relevance is the direction of engineering development and the need to define a specific use case. There is no claimed partnership or endorsement, and these programs should not be presented as proof of an autism therapy or an entropy-based mechanism.',['https://neuralink.com/trials/','https://neuralink.com/updates/convoy-study-launch/','https://neuralink.com/trials/speech-restoration/']);
s=base('Autism stimulation evidence remains specific','CLINICAL CONTEXT','Tan et al., 2026 · Ni et al., 2023, 2024');
text(s,'A positive trial',64,245,520,70,40,theme.accent,true);text(s,'A motor-cortex protocol in\n200 children reported better\nsocial-communication scores.',64,346,540,151,31,theme.ink);
text(s,'Other trials were negative',685,245,530,100,40,theme.ink,true);text(s,'Different frontal protocols\ndid not establish superiority\non their primary outcomes.',685,346,530,151,31,theme.muted);
line(s,64,542,1152);text(s,'The proposed feedback approach still needs direct clinical evidence.',64,587,1152,60,29,theme.accent,true);
notes(s,'The clinical landscape should be presented fairly. A recent motor-cortex trial reported a positive result, while two different frontal stimulation trials did not establish superiority on their primary outcomes. Population, protocol, target and follow-up matter. The positive study was not a test of entropy targeting or closed-loop control, and the proposed approach cannot borrow its benefit claim. The scientific opportunity is to identify a specific, plausible mechanism and test whether feedback adds value beyond the relevant intervention and simpler controls.',[DOI.tan,DOI.ni23,DOI.ni24]);
s=base('The simulation makes uncertainty visible','WHAT WE HAVE BUILT');
rows(s,[['Conditional improvement','A cleaner tracking score under favorable measurement conditions.'],['A meaningful limitation','Task accuracy remained near chance under disturbance.'],['A clear failure mode','More sensor noise reversed the added entropy term’s advantage.']],{y:232,gap:130});
notes(s,'The current contribution is a working model that can produce unwelcome answers. It shows a conditional improvement in continuous tracking, but no recovery of the binary task under disturbance. Greater sensor noise reverses the incremental result. That means the research team has concrete assumptions to test rather than a demonstration designed to always look successful. The model’s value is in exposing when a proposed control rule works, when it fails and what evidence would be needed to make it more realistic.',[site]);
s=base('Explore the working research model','INTERACTIVE EXPERIENCE');
await picture(s,artBrain,628,220,588,373,'cover');
text(s,'Rotate the cortex.\nChange the conditions.\nInspect the outcome.',64,253,555,232,43,theme.ink,true);
let l=text(s,'Open the brain lab ↗',64,547,550,69,33,theme.accent,true);l.text.get('Open the brain lab ↗').link={uri:site,isExternal:true};
notes(s,'The live brain lab is available through the link on this slide. It combines a cortical template with the synthetic neural model and allows changes to feedback strategy, gain, measurement noise, delay and optional plasticity. It also displays task outcomes, so a visually active brain cannot be mistaken for a successful result. The artwork here is conceptual; the application itself contains a manipulable anatomical mesh. The interface is intended for research discussion and model exploration, and it does not operate a medical device.',[site],'Visual: AI-generated conceptual brain artwork, not an application screenshot or patient scan.');
s=base('Each development stage has a decision gate','THE RESEARCH PATH');
rows(s,[['Measurement study','Can the signal reliably predict an agreed within-person outcome?'],['Realistic modeling','Does feedback beat simpler controls with credible sensing and actuation?'],['Clinical feasibility','Does a specified intervention add benefit with acceptable burden?']],{y:232,gap:130});
notes(s,'The proposed development path begins with measurement, not a treatment promise. A repeated-session study should test whether a candidate signal predicts an outcome selected with participants. Modeling should then use realistic observation and actuation and compare against optimized simpler approaches. Only a justified, clinically governed feasibility study could assess whether a specified intervention helps. Each stage can lead to revision or stopping. That is a proposed sequence, with no claim that a human protocol has been approved or that these gates have already been passed.',[site,DOI.participate]);
s=base('Collaboration is the next concrete step','A SHARED RESEARCH PROGRAM');
three(s,[['Autistic partners','Define priorities, acceptable burden and meaningful success.'],['Methods researchers','Challenge measurements, models, controls and reproducibility.'],['Clinical collaborators','Assess feasibility, study governance and participant protection.']]);
notes(s,'Advancing this program requires several kinds of expertise. Autistic partners determine which questions are worth asking and how participation should work. Methods researchers should challenge the signal interpretation, the model and the controls. Clinical collaborators are necessary to evaluate any eventual human intervention. The current manuscript and software provide a concrete starting point for that conversation. They do not replace independent scientific review, a participant study or the professional responsibilities involved in clinical research.',[DOI.participate,site]);
s=base('Evidence and materials are available to inspect','SELECTED SOURCES');
const reading=[['Participation','Fletcher-Watson et al. (2019)',DOI.participate],['Adaptive stimulation','Oehrn et al. (2024)',DOI.oehrn],['Bidirectional BCI','Flesher et al. (2021)',DOI.flesher],['Autism stimulation','Tan et al. (2026); Ni et al. (2023, 2024)',DOI.tan],['Industry programs','Neuralink official trial pages','https://neuralink.com/trials/'],['Our research','Manuscript, simulation and interactive lab',site]];
reading.forEach(([a,b,u],i)=>{let y=222+i*67;text(s,a,64,y,380,46,25,theme.accent,true);let t=text(s,b,465,y,750,51,25,theme.ink);t.text.get(b).link={uri:u,isExternal:true};});
notes(s,'The full research package contains the manuscript, references, source audit, executable Python model and recorded results. The sources listed here support distinct parts of the story and should not be combined into a claim they did not test. Peer-reviewed clinical findings are separated from company program descriptions and from our synthetic outputs. Both the positive findings and the limitations are available for review. The final invitation is to use these materials to design a stronger, participant-centered research study.',[...reading.map(r=>r[2]),DOI.ni23,DOI.ni24]);
s=base('Build support that people choose.','THE INVITATION','Proposed research program · Clinical benefits remain to be established',true);
text(s,'Start with their goals.\nTest the mechanism.\nEarn the benefit claim.',64,242,1110,251,59,'#F6F4FF',true);text(s,'A responsible path toward person-specific neural support.',64,566,1120,62,31,'#9DE3D4');
notes(s,'The vision is to develop support that people choose because it helps with something they value. The current work makes a research hypothesis concrete, with a functioning model, an updated evidence base and results that reveal both potential and failure. The next step is to test reliable measurements and plausible mechanisms with the right collaborators. A benefit claim must be earned through direct evidence on meaningful outcomes. That is the opportunity this program presents and the standard it should be held to.',[site,DOI.participate]);
}
await exportDeck('BBCI_Research_Opportunity');
