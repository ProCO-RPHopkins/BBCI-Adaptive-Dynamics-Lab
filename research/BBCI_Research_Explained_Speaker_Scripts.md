## Slide 1

This presentation explains a research idea and the experiment built to challenge it. A brain–computer interface can measure activity, and a bidirectional system can also send a signal back. The question is whether information about the variety of brain activity helps that feedback support something useful. We tested a simplified computer model and updated the clinical literature through September 2026. The results are mixed in an informative way. This is a research program, and the simulation does not demonstrate a therapy for autistic people.
Visual: AI-generated conceptual brain illustration created for this presentation. It is not a scan or an empirical connectivity map.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 2

The starting point is a person’s priorities. A future intervention might be judged by a communication goal, sensory comfort or another outcome the participant chooses. Atypical brain activity is not automatically a problem to correct. Recent large-scale work also shows that heterogeneity depends on the scale at which we look. The practical implication is to measure individuals carefully and to develop the research with autistic partners. Our model uses an engineering task because it has no participants; that task must never be confused with a measure of wellbeing.
[Sources]
- https://doi.org/10.1177/1362361318786721
- https://doi.org/10.1038/s44220-026-00656-y
[/Sources]

## Slide 3

Here entropy describes the predictability of short patterns in a signal. It does not score how healthy, intelligent or useful a brain is. Different complexity measures can even move in different directions in the same research setting. Our benchmark specifies one estimator, permutation entropy, and measures an independent task outcome. Think of a microphone: adding static makes a recording less predictable, but it does not improve the message. That analogy illustrates why a controller must know whether its measurement contains useful information or contamination.
[Sources]
- https://doi.org/10.1103/PhysRevLett.88.174102
- https://doi.org/10.3389/fpsyt.2025.1505297
[/Sources]

## Slide 4

Three developments change how this research should be framed. Individual differences remain substantial, with more shared structure at some scales than others. New psychedelic research challenges the idea that a more varied signal is simply random disorder. And a recent autism stimulation trial reported a positive result for a specific protocol. These are useful developments, but they do not combine into proof of our proposed therapy. The bridge between a measured state, a feedback action and a meaningful outcome still has to be tested directly.
[Sources]
- https://doi.org/10.1038/s44220-026-00656-y
- https://doi.org/10.1038/s41586-026-10910-z
- https://doi.org/10.1136/bmj-2025-086295
[/Sources]

## Slide 5

The experiment focuses on the added value of one ingredient. Rate feedback already responds to mean activity. We then add a calibrated entropy term and ask whether the circuit preserves a separate input signal more accurately. We do not tell the model that higher entropy is better. Instead, the target comes from an individual reference session, and the entropy term uses a measured local response to input. This is an exploratory engineering comparison. Its outcome cannot establish which state would be desirable for a real person.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 6

The model contains interacting excitatory and inhibitory populations. Their activity produces a measurement, which can include noise and an input-related artifact. The feedback rule uses activity and entropy errors to propose an input. Numerical constraints limit that input before it returns to the circuit. A separate readout, trained on a different session, checks task performance. The distinction is essential: making the measured statistic match a reference is not the same as improving the task. These units are dimensionless and do not specify a human stimulation setting.
[Sources]
- https://doi.org/10.1016/S0006-3495(72)86068-5
- https://doi.org/10.1103/PhysRevLett.88.174102
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 7

The comparison needs more than a no-input control. Fixed input tests whether adaptation is necessary, although it receives a different calibration opportunity in this benchmark. Activity feedback tests a simpler adaptive explanation. Entropy alone shows what the additional term can do without rate correction. The combined strategy is the main experimental arm. Yoked replay uses another individual’s input sequence, so the complete group receives matched aggregate energy without each person’s current-state feedback. No single comparator settles every explanation; together they expose several important alternatives.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 8

The final study evaluates 24 synthetic individuals across three random seeds. Six nominal strategies produce 432 runs. Four additional stress conditions each compare three strategies, bringing the evaluation total to 1,296. Calibration and diagnostic simulations are additional. The uncertainty intervals resample synthetic individuals after averaging their seeds. They describe this chosen ensemble, not uncertainty in a human treatment effect. The project also includes reproducibility checks and a notebook, so the result can be inspected and challenged rather than accepted from a figure alone.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 9

In the deliberately clean measurement condition, adding entropy reduced the average continuous tracking error by about four and a half model units relative to activity feedback. The synthetic-ensemble interval was below zero. That improvement came with greater input energy. The fixed-input comparator had a lower mean error than either adaptive approach, although it had been calibrated on the disturbance distribution. This is evidence of conditional performance in a defined model. It is not a percentage improvement in a symptom score, and it does not establish that adaptive control is generally better.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 10

This is the result that prevents an overly positive interpretation. A fresh unperturbed session reached about 80 percent accuracy on the simple binary task. Under disturbance, both activity and combined feedback were close to 50 percent. The entropy term improved the continuous readout’s error without restoring useful sign decisions. A linear readout can change its offset or scale while making almost the same choices. Reporting only the favorable tracking score would therefore hide a major limitation. We need both measures to understand what the controller actually accomplished.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 11

The horizontal intervals show the extra effect of the entropy term under different observation conditions. Clean measurements favor the combined rule. With added sensor noise, the sign reverses and the combined rule has higher tracking error. Extra delay and an input-related artifact produce intervals that cross zero. These conditions were tested separately, so they are not a complete model of real recordings. The lesson is practical: a controller can respond to contamination in its measurement. Reliable sensing and a way to abstain when uncertain are part of the hypothesis, not optional refinements.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 12

The model includes an optional plasticity rule, which changes connection weights according to recent activity. This is more explicit than simply forcing two traces to become similar. However, the rule also contains an imposed relaxation toward the original weights. In a verification example, washout follows the expected decay almost exactly. That is a successful software check, but it is not evidence of lasting biological rewiring. A stronger learning claim would require an independent task improvement that persists beyond the imposed adaptation dynamics and is supported by an appropriate biological model.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 13

The companion lab lets you rotate a cortical surface, inspect synthetic populations and compare strategies. You can change measurement noise or feedback delay, rerun the same model and look at the task outcome as well as the animation. The anatomical surface is a real public template, but the connections and activity are simulated and are not a patient brain map. The artwork on this slide is conceptual; the live application contains the interactive cortical mesh. The Python package remains the main reproducible scientific record, with the browser serving as an exploratory view.
Slide artwork is AI-generated and is not a screenshot of the application.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 14

The next empirical step should establish whether a candidate measurement is useful for an individual across time and context. It should be designed with autistic participants, with a prospectively agreed outcome and a clear way to stop if the measurement is uninformative. Model fitting would then need realistic sensing and actuation, along with comparisons against simpler controllers. A clinically governed intervention study would be a later, separate step. This sequence is a proposed research agenda, not an approved protocol, and the current simulation provides no device settings or treatment regimen.
[Sources]
- https://doi.org/10.1177/1362361318786721
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]

## Slide 15

These are selected entry points into the evidence and methods. The complete manuscript contains 22 references and the research package includes a BibTeX file and an evidence ledger describing what each source can and cannot support. The literature update used Consensus discovery followed by record retrieval and primary-source checking. It was a targeted narrative update, not a systematic review. The model findings are new synthetic outputs from the accompanying code and should be assessed separately from the clinical literature.
[Sources]
- https://doi.org/10.1038/s44220-026-00656-y
- https://doi.org/10.1038/s41586-026-10910-z
- https://doi.org/10.1136/bmj-2025-086295
- https://doi.org/10.3389/fpsyt.2025.1505297
- https://doi.org/10.1016/S0006-3495(72)86068-5
- https://doi.org/10.1103/PhysRevLett.88.174102
[/Sources]

## Slide 16

The central question was whether a more informative feedback loop could support a useful outcome. Our answer is conditional: entropy helped one score under clean observation, but did not restore the task and became counterproductive with greater measurement noise. That result improves the research question by making its assumptions visible. The way forward is to test reliable individual measurements, compare against simpler approaches and use outcomes chosen with the people the research hopes to support. The code and interactive model make those questions concrete enough to challenge.
[Sources]
- https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site
[/Sources]