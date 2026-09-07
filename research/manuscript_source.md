# Entropy-informed feedback in autism neuromodulation research: a falsifiable neural-mass benchmark

## Abstract

Person-specific closed-loop neuromodulation is a plausible research direction in autism, but neither an autism-specific entropy target nor the added value of entropy feedback has been established. We implemented an exploratory Python benchmark that separates neural dynamics, observation, feedback and independent task evaluation. Sixteen coupled excitatory–inhibitory neural masses represented each of 24 synthetic individuals, without assigning an autism diagnosis to model parameters. Separately calibrated controllers were evaluated across three random seeds, six nominal strategies and four robustness conditions, yielding 1,296 evaluation runs. Adding permutation-entropy feedback to rate feedback reduced continuous task-tracking mean squared error by 4.53 units (95% bootstrap interval across synthetic individuals, −6.54 to −2.83 for combined minus rate feedback), while increasing control energy by 0.0175 model units. Binary task accuracy remained approximately 50%, compared with 80.3% in a held-out unperturbed reference session. Increased measurement noise reversed the incremental tracking advantage, and a two-second delay made it uncertain. Calibrated fixed input had lower mean tracking error than either adaptive strategy. Bounded covariance plasticity produced weight changes whose washout followed the imposed relaxation rule. These results demonstrate conditional control performance and failure modes in a specified synthetic system, not efficacy or durable therapeutic plasticity in autistic people. The contribution is a reproducible test of whether complexity adds useful information beyond simpler feedback, accompanied by an interactive anatomical display and an explicit translational research agenda. Clinical development requires reliable individual measurements, realistic observation and actuation models, and benefits defined with autistic participants.

## 1 Introduction

The appeal of combining a bidirectional brain–computer interface with the entropic brain framework is that a system could measure changing neural dynamics, intervene when needed, and support useful learning. However, three distinct propositions are often compressed into that narrative: that a neural statistic differs in autism; that an intervention can alter that statistic; and that altering it improves an outcome valued by a particular person. Evidence for one proposition does not establish the others. We therefore treat entropy-informed feedback as an engineering hypothesis requiring an independent outcome, rather than as an established therapy.

Autism heterogeneity makes a universal connectivity correction difficult to justify. In a 32-site analysis of 1,824 people, Ilioska et al. (2026) found that extreme deviations in individual functional connections rarely overlapped between participants, although convergence increased at regional and network scales. This combination supports multiscale individual characterization without implying an absence of shared structure. A normative deviation is a statistical description; it does not, by itself, identify dysfunction, a desirable reference state or an indication for intervention. Participatory research is necessary to determine which difficulties merit support and which outcomes matter (Fletcher-Watson et al., 2019).

Neural complexity also depends on what is measured. Tenev et al. (2025) reported higher generalized EEG entropy but lower Lempel–Ziv complexity in autistic children relative to a comparison group. Fu et al. (2025) found a localized increase in sample entropy during sleep-state functional MRI, alongside directional differences in information transfer. Neither result establishes a global deficit to be corrected by increasing entropy. Estimator, temporal scale, recording modality, developmental stage and context must remain explicit.

The entropic brain theory concerns relationships between neural dynamics and conscious states (Carhart-Harris et al., 2014; Carhart-Harris, 2026). Recent work adds context to a simple disorder interpretation. Stoliker et al. (2026) found that psychedelic brain trajectories in 62 adults aligned with sensory conditions rather than becoming indiscriminately disorganized. Lyons et al. (2026) reported relationships between acute signal complexity and later wellbeing after first psilocybin use in a small exploratory adult study; these associations neither establish causal mediation nor demonstrate an autism treatment. Mechanistic whole-brain modeling links serotonergic effects to circuit and network properties rather than equating a drug with an arbitrary noise source (Herzog et al., 2023). These studies motivate measuring dynamics and context separately. They do not supply the therapeutic objective used here.

The clinical stimulation literature is mixed and protocol-specific. Two sham-controlled frontal theta-burst trials did not establish superiority on their primary autism symptom outcomes (Ni et al., 2023, 2024), consistent with uncertainty in a network meta-analysis of randomized noninvasive stimulation studies (Chen et al., 2024). A subsequent multicenter trial randomized 200 children to accelerated motor-cortex stimulation or sham and reported improved social-communication scores through one month (Tan et al., 2026). This positive trial updates an exclusively negative narrative, but it tested neither entropy targeting nor feedback control. Its protocol, population and follow-up cannot be generalized to an unspecified bidirectional device.

Bidirectional interfaces and adaptive stimulation provide complementary engineering precedents. Tactile feedback improved robotic-arm control in an implanted BCI study (Flesher et al., 2021), while individualized adaptive stimulation improved motor outcomes relative to optimized continuous stimulation in a four-person Parkinson’s disease feasibility trial (Oehrn et al., 2024). A small autism BCI study demonstrated feasibility of a social-attention training approach rather than definitive therapeutic efficacy (Amaral et al., 2018). None validates the proposed entropy mechanism in autism. Here, “bidirectional” refers narrowly to a modeled measurement–actuation loop; the benchmark does not implement a clinical sensory prosthesis.

The present work advances a supplied conceptual review and Julia prototype into an executable, falsifiable benchmark. We ask whether a calibrated entropy term improves an independent task readout beyond rate feedback, and whether any advantage survives delay, noise, stimulation artifact, yoked input and bounded plasticity. The model is intentionally synthetic: its purpose is to expose assumptions and counterexamples before patient fitting. It does not recreate autism, estimate an individual’s clinical state, or establish an optimal level of brain entropy.

## 2 Materials and methods

### 2.1 Study design and evidence update

The computational study was exploratory and was not preregistered. The combined-versus-rate tracking comparison was designated as the primary engineering contrast before the final benchmark execution; controller design and parameter ranges were developed through pilots. We report those choices and preserve a higher-noise pilot summary. A targeted evidence update used Consensus searches with subsequent paper-record retrieval, supplemented by primary publisher and PubMed records, through 7 September 2026. Search themes included autism neural complexity, sham-controlled stimulation, individual connectivity, adaptive BCI, entropic brain theory and neural-mass modeling. Publication metadata were checked against DOI records. This was a focused narrative update, not a systematic review, exhaustive search or meta-analysis. The evidence ledger documents source scope and unsupported extrapolations.

The original public repository was inspected at the source-file level. The audited Julia file had blob SHA f52f9b84294b6b6bb04a56218c2a97471867c8c5. Its random-walk demonstration did not implement an entropy estimator or activity-dependent synaptic weights, and its classifier distinguished region identity rather than a functional task. The notebook contained recorded undefined-variable errors. The Python implementation is a new benchmark, not a line-by-line translation or a biological validation of that prototype. The full audit is supplied with the code.

### 2.2 Synthetic individuals and neural dynamics

Each individual comprised 16 Wilson–Cowan-type excitatory and inhibitory populations (Wilson and Cowan, 1972). We selected this scale for transparent controls and interactive execution. The neural-mass approach is consistent with reusable whole-brain simulation frameworks such as neurolib, although the present implementation does not depend on that package (Cakan et al., 2023). The two hemispheres and four paired modules were illustrative labels. No participant imaging, diagnostic label, receptor map or patient-specific parameter fit was used.

@EQUATION τ_E dE_i/dt = −E_i + S(a z_i)

@EQUATION z_i = w_EE,i E_i − w_EI,i I_i + g Σ_j W_ij E_j + p − 2.5

@EQUATION        + q_i(t) + d(t) + b_i u(t) + ξ_i(t)

@EQUATION τ_I dI_i/dt = −I_i + S[a(10E_i − 2I_i − 3)],     S(x) = 1/(1 + exp(−x)).

E and I are bounded normalized population activities, not calibrated firing rates in hertz. Time constants were 40 and 80 ms. Initial activities were 0.1. The noise process ξ was an Ornstein–Uhlenbeck current with 150-ms time constant and stationary-scale parameter 0.04. Its stochastic forcing is a model component, not “entropy injection” or a pharmacological mechanism. Gain a, coupling g and baseline drive p varied between synthetic individuals; Table 1 specifies all ranges and fixed coefficients.

For each off-diagonal connection, an initial positive weight was proportional to [0.15 + 0.60 M_ij + 0.30 H_ij] times a lognormal factor with log-standard-deviation 0.30. M indicates the same paired module across either hemisphere; H indicates the same hemisphere. Rows were normalized to one and diagonal weights set to zero. A fixed broad actuator field b had values [0.35, 0.35, 0.65, 0.65, 1, 1, 0.75, 0.75] in each hemisphere. This field defines an input distribution only. It is not a modeled electric field, coil position or implant configuration.

### 2.3 Task, perturbations and independent evaluation

Each 60-s run contained a balanced-in-expectation random binary input updated every 0.5 s. Input amplitude 0.6 entered four designated sensory populations. A scalar context disturbance was absent before 15 s, equaled the individual disturbance parameter during 15–30 s, changed to −0.6 times that parameter during 30–45 s, and ended at 45 s. These manipulations test distribution shift in a dynamical system. They do not operationalize sensory overload, an autistic trait or a clinical episode.

An individual ridge readout used the 12 non-input populations to estimate the input with a 150-ms lag. Features were centered and scaled using a separate unperturbed calibration session; coefficients were fitted on seconds 10–45 with penalty 10. The readout and calibration statistics were held fixed during evaluation. A fresh unperturbed seed assessed baseline generalization. The readout accesses true latent excitatory states, giving a favorable observation assumption for task decoding; the feedback controller sees only a noisy population average. This asymmetry is deliberate and limits realism.

The primary engineering outcome was mean squared error (MSE) of the continuous readout during seconds 15–45. Secondary outcomes included sign-classification accuracy, mean squared deviation from reference activity, permutation entropy, spectral entropy, control energy and post-disturbance tracking error. The linear readout is unbounded: large MSE can result from gain or offset drift despite similar sign decisions. For that reason accuracy is reported alongside MSE. Neither metric measures social communication, wellbeing or therapeutic benefit. Washout readout error used seconds 47–60 to allow a short transition interval.

### 2.4 Observation and entropy estimation

The controller observed y(t) = mean_i E_i(t) + ε(t) + A u(t) sin(2π·37t), sampled at 100 Hz. Independent Gaussian sensor noise ε had nominal standard deviation 0.001. A was zero except in the stimulation-artifact condition, where it equaled 0.20. The 37-Hz term is an illustrative measurement contaminant, not a complete stimulation artifact model or EEG forward solution. No band-pass filter, source reconstruction or artifact rejection was applied.

Normalized permutation entropy was computed from ordinal patterns of dimension three, with lag two samples and one-second non-overlapping windows (Bandt and Pompe, 2002). Stable temporal ordering resolved equal values. With six possible ordinal patterns, H = −Σ_k p_k ln(p_k)/ln(6), which ranges from zero to one. Each window contributes 96 overlapping embedded patterns. This short-window estimator has finite-sample bias and correlated observations; no claim of bias-free entropy estimation is made. An independent 35-s baseline supplied the reference mean activity and mean window entropy. References therefore reflect the individual model’s unperturbed task condition, not an empirically optimized wellbeing state.

To estimate how input changes the measured statistic, constant calibration inputs of +0.20 and −0.20 were applied in separate matched unperturbed simulations. Their mean entropy difference, divided by 0.40, defined an individual local slope s. If |s| was below 0.01, the entropy correction abstained. Otherwise the correction v = clip[(H* − H)/s, −0.35, 0.35] used the sign and scale of the measured response. This derivative is local and noisy; it does not establish global controllability or causal specificity of entropy.

### 2.5 Feedback strategies and comparators

Controllers updated once per second using the latest available one-second measurement window. Rate feedback proposed u = 4(r* − r). Entropy-only feedback proposed 0.5 times the preceding input plus 0.5v. Combined feedback proposed 4(r* − r) + 0.3v. All proposals passed through a slew limit of 0.15 per update and an absolute amplitude cap of 0.60. Proposals were zero before 10 s and from 45 s onward, with the same slew constraint retained during turn-off. These are dimensionless numerical limits and cannot be converted into a safe human stimulation dose.

The no-input comparator shared the task and random streams. The fixed-input comparator selected the lowest-MSE value among seven equally spaced candidates from −0.60 to +0.60 on an independent perturbed calibration seed. Thus fixed input had access to the disturbance distribution during calibration, whereas adaptive rules were not optimized on the evaluation outcomes. It is a useful, relatively strong open-loop comparator, but this design does not compare equally optimized controller families. A yoked comparator replayed the combined controller’s input from the next individual in a cyclic ordering, preserving aggregate input energy while removing current-person feedback. It controls aggregate exposure rather than energy matching within every individual.

### 2.6 Robustness, plasticity and entropy diagnostics

The control architecture is summarized in Figure 1. The nominal experiment evaluated six strategies across 24 individuals and three seeds. Four additional conditions each evaluated no input, rate feedback and combined feedback: two-second extra observation delay; sensor-noise standard deviation 0.05; artifact scale 0.20; and activity-dependent weight adaptation. These conditions were studied separately rather than as a full factorial experiment. The moderate-noise pilot used standard deviation 0.01 and yielded weak entropy calibration in much of the ensemble. The final low-noise condition deliberately tests a favorable measurement case, not expected EEG performance.

In the plasticity condition, off-diagonal weights followed a bounded covariance rule with a two-second running activity mean, coefficient η = 0.15 and relaxation time 20 s:

@EQUATION dW_ij/dt = η(E_i − Ē_i)(E_j − Ē_j) − (W_ij − W^0_ij)/20.

The covariance term ended at 45 s; relaxation continued. Weights were constrained to [0.25 W⁰, 2 W⁰], with zero diagonal and no subsequent row normalization. This phenomenological rule is neither spike-timing-dependent plasticity nor a validated molecular mechanism. Relative Frobenius weight change quantified adaptation and washout. Residual changes cannot establish durability because retention is largely specified by the imposed decay constant.

Exploratory gain sweeps covered 0.9–2.4 at 11 levels in eight individuals, without imposing an inverted-U relationship between complexity and performance. Forty Fourier phase surrogates per individual preserved the magnitude spectrum of a 30-s observed record. Original and surrogate permutation entropy were compared descriptively. Whole-record surrogate entropy and mean one-second online entropy use different windows and are not numerically interchangeable. These diagnostics examine dependence on dynamics and temporal ordering; they do not identify an autism biomarker or a universal optimal entropy.

### 2.7 Computation, uncertainty and verification

Forward Euler integration used a 2-ms step and recorded every 10 ms. A seeded 32-bit linear congruential generator with Box–Muller Gaussian conversion enabled a matched JavaScript implementation. At a fixed step size, arms shared task and stochastic streams; individual parameters used NumPy’s separately seeded generator. Parameter seeds were 4100 plus individual index, calibration seeds were 710 plus 11 times that index, and evaluation seeds were 100, 200 and 300. Supplementary code specifies all streams, including validation and diagnostic seeds.

Replicates were averaged within each synthetic individual. Mean contrasts and 95% percentile intervals used 4,000 bootstrap resamples of individuals with seed 809. These intervals describe this sampled parameter ensemble, not patients, parameter posterior uncertainty, or all plausible neural models. Secondary contrasts were exploratory and were not adjusted for multiple comparisons; no confirmatory P values are reported. Results were retained regardless of direction.

Thirteen software and numerical checks assessed reproducibility, estimator invariance, bounded states, constrained input, matched task streams, abstention, yoked energy, data integrity and plasticity decay. An independent high-accuracy adaptive ODE solver checked the production integrator during a deterministic 0.5-s interval; decreasing the Euler step from 2 to 1 to 0.5 ms reduced maximum activity error. A separate stochastic step-size sensitivity file is provided; using the same seed at different steps does not create a shared Brownian path, so that comparison is not a pathwise convergence proof. Code, raw evaluation rows, calibration records, figures and an executable notebook accompany the manuscript, consistent with reproducible computational practice (Sandve et al., 2013).

### 2.8 Interactive anatomical representation

The browser interface renders the fsaverage5 cortical template distributed through Nilearn from FreeSurfer, with folded and inflated surfaces. The 16 synthetic states color nearby vertices and the display shows illustrative network edges. Anatomical geometry, synthetic regional labels and simulated dynamics remain separate: the surface is not an autistic participant’s brain or an empirical activation map. A Web Worker executes the JavaScript port, while Python-generated benchmark data provide fixed reference results. A seed-matched example reproduced Python population trajectories to the six-decimal precision of the display data. The notebook is the reproducible analysis record; the browser is an exploratory interface, not a clinical control application.

## 3 Results

### 3.1 Calibration and nominal controller performance

The held-out unperturbed reference achieved 80.27% task accuracy (95% synthetic-ensemble interval 78.48–82.13%) and MSE 0.706 (0.663–0.748). All estimated entropy slopes were negative in the chosen operating range, spanning −0.1356 to −0.0059; two of 24 fell below the abstention threshold. Thus the model does not encode the premise that stimulation always increases entropy.

Under context disturbance, mean MSE was 124.41 without input, 69.94 with calibrated fixed input, 81.36 with rate feedback, 97.80 with entropy feedback, 76.83 with combined feedback, and 126.77 with yoked replay (Figure 2; Table 2). Combined minus rate feedback was −4.53 MSE units (−6.54 to −2.83). The corresponding difference in control energy was +0.0175 (+0.0147 to +0.0202). Combined feedback also had lower MSE than yoked replay by 49.95 units (20.14–86.17 lower), indicating dependence on current-individual state under this design. Aggregate energy was identical for combined and yoked input.

The MSE advantage did not translate into useful sign discrimination. Mean accuracy was 50.04% with rate feedback and 50.03% with combined feedback; their difference was −0.008 percentage points (−0.020 to approximately zero). The calibrated fixed comparator reached 52.58% and had the lowest mean MSE, although its calibration access differed. These findings support partial correction of a disturbed continuous readout, not restoration of the original task representation or superiority of adaptive control in general.

### 3.2 Measurement conditions changed the incremental result

With two seconds of extra observation delay, combined minus rate MSE was −0.77 (−3.00 to +1.57). With sensor-noise standard deviation 0.05, it was +8.28 (+4.60 to +12.65), reversing the nominal advantage. With stimulation artifact, the contrast was +3.52 (−0.11 to +7.56), with uncertainty spanning zero (Figure 3). The results show that nominal performance cannot be extrapolated across observation conditions. They do not identify a clinically acceptable noise threshold or quantify performance with a real recording device.

### 3.3 Plasticity and diagnostic checks

The bounded-plasticity condition retained a combined-versus-rate MSE difference of −4.60 (−6.51 to −3.01). In the validation example, weight change at the end of washout was 0.47235 times its value at 45 s, matching the prescribed exponential relaxation. This is numerical evidence that the implemented decay rule behaves as specified, not evidence of long-term learning. The exploratory gain and phase-surrogate results illustrate that entropy depends on operating point and temporal organization (Figure 4); they provide no patient-derived entropy optimum.

All 13 verification checks passed. Against the independent deterministic solver, maximum excitatory-state errors were 1.92 × 10⁻⁵, 1.01 × 10⁻⁵ and 5.14 × 10⁻⁶ at steps of 2, 1 and 0.5 ms, respectively. These checks support implementation integrity within their tested scope. They do not resolve biological validity, stochastic convergence across all regimes, or model identifiability.

## 4 Discussion

### 4.1 What the benchmark adds

The principal advance is a falsifiable separation between controlling a measured statistic and preserving independent information. In the favorable nominal condition, an entropy term improved continuous tracking beyond rate feedback, but the advantage required greater input energy and did not rescue classification accuracy. A simpler calibrated fixed input had lower mean error. These outcomes narrow the hypothesis: entropy may contain locally useful control information in a particular operating regime, yet “adaptive,” “complex” and “therapeutic” are not interchangeable descriptions.

The noise reversal is especially informative because entropy can be changed by the observation process itself. Feedback then acts on a mixture of latent dynamics, task structure and measurement contamination. A future system would need to estimate which part of a complexity change is interpretable and when its uncertainty warrants abstention. The present slope threshold offers only a minimal example. It does not address session-to-session calibration drift, nonstationarity, artifact rejection or state-estimation uncertainty. Those omissions are testable engineering gaps rather than evidence against all closed-loop approaches.

No causal benefit of entropy itself has been established. The combined controller changes input, rate and higher-order signal statistics together. Rate and entropy may reflect overlapping information; lower MSE could follow changed operating point rather than a distinct complexity mechanism. An energy-matched, optimized rate controller, phase-scrambled feedback, multiple estimators, explicit measurement models and mediation-resistant task controls are stronger next comparisons. The yoked condition addresses one alternative explanation but cannot substitute for these ablations.

### 4.2 Updating the therapeutic rationale

The recent literature supports a more precise rationale than either universal normalization or dismissal of stimulation research. Multiscale heterogeneity argues for individual characterization (Ilioska et al., 2026), while context-dependent psychedelic dynamics motivate distinguishing structured variability from noise (Stoliker et al., 2026). Neither observation defines a clinical target. The positive motor-cortex trial and negative frontal trials show that intervention claims must retain their population, target and outcome boundaries (Ni et al., 2023, 2024; Tan et al., 2026). The current model includes no implementation of those protocols and cannot explain their treatment effects.

Person-specific references should therefore be selected through repeated measurement and outcomes the participant values. Returning to an individual’s own baseline may be a useful engineering control, but it is not automatically desirable if that baseline is distressing or constraining. Equally, being statistically atypical is not sufficient reason to intervene. The translational objective is assistance with consented difficulties, such as a personally prioritized communication or sensory goal, while preserving autonomy and avoiding pressure to suppress harmless autistic characteristics. Meaningful participation should shape the question and stopping decisions, not merely recruitment (Fletcher-Watson et al., 2019).

### 4.3 A staged translational program

The next empirical step is a preregistered measurement study, designed with autistic adults and relevant clinical collaborators, before an efficacy trial. Candidate tasks and complexity estimators should be evaluated across repeated sessions, contexts and artifact conditions. The primary question would be whether a candidate statistic predicts a within-person, agreed functional outcome beyond simpler measures such as power, rate proxies and task history. Splitting data by session rather than adjacent windows would reduce leakage. Reliability, calibration transfer and the ability to detect uncertainty should determine whether the feedback hypothesis proceeds.

Model development should then replace the synthetic coupling, population-average observation and broad actuator with appropriate data and forward models. ABIDE resources are valuable for autism imaging research, but their available modalities must be inspected rather than assuming a ready-made individual diffusion connectome for every participant (Di Martino et al., 2014, 2017). Empirical fits would require held-out validation, sensitivity to alternative model families, identifiable parameters and comparison with simpler null models. A realistic EEG observation model and input artifact mechanism are priorities because the present result changes direction under measurement noise.

Only after these steps should a clinically governed feasibility study test whether feedback adds benefit to a specified intervention. The protocol would need a justified modality, prospectively selected outcome, credible masking, fixed and yoked comparators, blinded assessment and follow-up sufficient for the proposed duration of benefit. Success should require a participant-valued improvement beyond simpler control, acceptable burden, reproducible measurement and no unacceptable adverse effects. No stimulation dose, implant recommendation, psychedelic regimen or treatment eligibility criterion follows from this benchmark. Human study design requires appropriate expertise, ethics review and participant consent; none has been obtained or claimed here.

### 4.4 Limitations

This work is a small exploratory computational study with a deliberately favorable nominal sensor. Parameter ranges were selected during development and do not represent a measured autism distribution. Only 24 synthetic individuals and three evaluation seeds were used; bootstrap intervals do not incorporate structural model uncertainty. The fixed controller received a distinct calibration advantage, and adaptive gains were not globally optimized. The binary readout is a narrow engineering task, with unusually large errors under disturbance and privileged access to latent states. Its poor discrimination is a substantive negative result.

The estimator uses short windows, one embedding dimension and one lag. Delays, artifacts and plasticity were tested separately, with no full joint stress analysis. Coupling has no conduction delays, adaptation is phenomenological, and neither the actuator nor the observer is physiologically fitted. Real cortical geometry in the interface does not increase biological validity. The local deterministic numerical check is not a proof for the complete stochastic feedback system. Finally, the literature update was targeted and non-exhaustive. These limits preclude clinical efficacy claims, diagnostic use, assertions of durable rewiring and general conclusions that more or less entropy is beneficial.

## 5 Conclusion

Entropy-informed feedback deserves testing as an incremental source of control information, not adoption as a therapeutic objective. In this synthetic benchmark it improved one continuous measure under clean observations, failed to restore task discrimination and became disadvantageous with greater sensor noise. The accompanying code and interface make those boundaries reproducible and inspectable. Advancing the autism research program requires reliable individual measurements and prospectively defined, participant-valued outcomes before therapeutic claims can be assessed.

## Data and code availability

All data in this study were generated computationally. The accompanying BBCI_Research_Package contains model source, scripts, calibration data, all 1,296 evaluation rows, summary results, verification output, figure source and an executed notebook. The original prototype is available at https://github.com/ProCO-RPHopkins/BBCI-Entropic-Plasticity-Simulation. The new package has not been deposited in a public archival repository and has no assigned DOI; a versioned public deposit should be completed before journal submission. No external patient data were accessed.

## Ethics statement

This work used synthetic simulations and publicly distributed template anatomy. It involved no recruitment, patient records, human stimulation or animal experiments. No institutional ethics approval or human-study registration is claimed. Any future participant study is a separate project requiring appropriate review and consent.

## Author contributions

Ryan Hopkins originated the research question and supplied the prior manuscript and Julia prototype. The present draft, implementation and analysis were developed with AI assistance. Final CRediT roles, authorship eligibility, independent scientific verification and approval of the complete manuscript remain to be confirmed by the human author before submission.

## Funding

Funding information has not been supplied. A definitive funding declaration requires author confirmation before submission.

## Conflict of interest

Conflict-of-interest information has not been supplied. A definitive declaration requires author confirmation before submission.

## Acknowledgments and generative AI disclosure

OpenAI ChatGPT/Codex assisted with literature discovery, synthesis, Python and JavaScript implementation, computational analysis and manuscript drafting in September 2026. The exact underlying model version was not exposed in the working interface and must be added to the submission disclosure if available. Consensus supported scholarly discovery; publisher and DOI records supported source checking. An earlier Claude-assisted manuscript supplied by the author informed the starting question; its model version was not specified. All manuscript figures were generated from explicit code and simulation data, without generative-image processing. AI systems are not listed as authors. The human author must verify scientific claims, citations, code and declarations and accept responsibility before submission.

## Supplementary material

The research package provides the executable notebook, parameter and calibration files, complete evaluation results, exploratory diagnostics, higher-noise pilot summary, original-model audit, evidence ledger and reproducibility instructions. Presentation materials contain explanatory artwork and are distinct from the data figures in this manuscript.


## References

Amaral, C., Mouga, S., Simões, M., Pereira, H. C., Bernardino, I., Quental, H., et al. (2018). A Feasibility Clinical Trial to Improve Social Attention in Autistic Spectrum Disorder (ASD) Using a Brain Computer Interface. Front. Neurosci. 12, 477. doi: 10.3389/fnins.2018.00477

Bandt, C., Pompe, B. (2002). Permutation Entropy: A Natural Complexity Measure for Time Series. Phys. Rev. Lett. 88, 174102. doi: 10.1103/PhysRevLett.88.174102

Cakan, C., Jajcay, N., Obermayer, K. (2023). neurolib: A Simulation Framework for Whole-Brain Neural Mass Modeling. Cogn. Comput. 15, 1132-1152. doi: 10.1007/s12559-021-09931-9

Carhart-Harris, R. L., Leech, R., Hellyer, P. J., Shanahan, M., Feilding, A., Tagliazucchi, E., et al. (2014). The entropic brain: a theory of conscious states informed by neuroimaging research with psychedelic drugs. Front. Hum. Neurosci. 8, 20. doi: 10.3389/fnhum.2014.00020

Carhart-Harris, R. L. (2026). The entropic brain today. Brain, awag206 (advance online publication). doi: 10.1093/brain/awag206

Chen, Y. C. B., Lin, H. Y., Wang, L. J., Hung, K. C., Brunoni, A. R., Chou, P. H., et al. (2024). A network meta-analysis of non-invasive brain stimulation interventions for autism spectrum disorder: Evidence from randomized controlled trials. Neurosci. Biobehav. Rev. 164, 105807. doi: 10.1016/j.neubiorev.2024.105807

Di Martino, A., Yan, C. G., Li, Q., Denio, E., Castellanos, F. X., Alaerts, K., et al. (2014). The autism brain imaging data exchange: towards a large-scale evaluation of the intrinsic brain architecture in autism. Mol. Psychiatry 19, 659-667. doi: 10.1038/mp.2013.78

Di Martino, A., O’Connor, D., Chen, B., Alaerts, K., Anderson, J. S., Assaf, M., et al. (2017). Enhancing studies of the connectome in autism using the autism brain imaging data exchange II. Sci. Data 4, 170010. doi: 10.1038/sdata.2017.10

Flesher, S. N., Downey, J. E., Weiss, J. M., Hughes, C. L., Herrera, A. J., Tyler-Kabara, E. C., et al. (2021). A brain-computer interface that evokes tactile sensations improves robotic arm control. Science 372, 831-836. doi: 10.1126/science.abd0380

Fletcher-Watson, S., Adams, J., Brook, K., Charman, T., Crane, L., Cusack, J., et al. (2019). Making the future together: Shaping autism research through meaningful participation. Autism 23, 943-953. doi: 10.1177/1362361318786721

Fu, S., Wang, X., Chen, Z., Huang, Z., Feng, Y., Xie, Y., et al. (2025). Abnormalities in brain complexity in children with autism spectrum disorder: a sleeping state functional MRI study. BMC Psychiatry 25, 257. doi: 10.1186/s12888-025-06689-4

Herzog, R., Mediano, P. A. M., Rosas, F. E., Lodder, P., Carhart-Harris, R., Perl, Y. S., et al. (2023). A whole-brain model of the neural entropy increase elicited by psychedelic drugs. Sci. Rep. 13, 6244. doi: 10.1038/s41598-023-32649-7

Ilioska, I., Oldehinkel, M., Llera, A., Rovný, M., Mei, T., Kia, S. M., et al. (2026). Multiscale heterogeneity of atypical functional connectivity in autism. Nat. Ment. Health 4, 1010-1020. doi: 10.1038/s44220-026-00656-y

Lyons, T., Spriggs, M., Kerkelä, L., Rosas, F. E., Roseman, L., Mediano, P. A. M., et al. (2026). Human brain changes after first psilocybin use. Nat. Commun. 17, 3977. doi: 10.1038/s41467-026-71962-3

Ni, H. C., Chen, Y. L., Chao, Y. P., Wu, C. T., Chen, R. S., Chou, T. L., et al. (2023). A lack of efficacy of continuous theta burst stimulation over the left dorsolateral prefrontal cortex in autism: A double blind randomized sham‐controlled trial. Autism Res. 16, 1247-1262. doi: 10.1002/aur.2954

Ni, H. C., Chen, Y. L., Hsieh, M. Y., Wu, C. T., Chen, R. S., Juan, C. H., et al. (2024). Improving social cognition following theta burst stimulation over the right inferior frontal gyrus in autism spectrum: an 8-week double-blind sham-controlled trial. Psychol. Med. 54, 3261-3272. doi: 10.1017/S0033291724001387

Oehrn, C. R., Cernera, S., Hammer, L. H., Shcherbakova, M., Yao, J., Hahn, A., et al. (2024). Chronic adaptive deep brain stimulation versus conventional stimulation in Parkinson’s disease: a blinded randomized feasibility trial. Nat. Med. 30, 3345-3356. doi: 10.1038/s41591-024-03196-z

Sandve, G. K., Nekrutenko, A., Taylor, J., Hovig, E. (2013). Ten Simple Rules for Reproducible Computational Research. PLoS Comput. Biol. 9, e1003285. doi: 10.1371/journal.pcbi.1003285

Stoliker, D., Novelli, L., Khajehnejad, M., Biabani, M., Greaves, M. D., Barta, T., et al. (2026). Psychedelics align brain activity with context. Nature 656, 936-947. doi: 10.1038/s41586-026-10910-z

Tan, H., Ren, T., Cao, A., Fang, S., Deng, L., Hu, B., et al. (2026). Accelerated continuous theta burst stimulation targeting left primary motor cortex for children with autism spectrum disorder: multicentre randomised sham controlled trial. BMJ 393, e086295. doi: 10.1136/bmj-2025-086295

Tenev, A., Markovska-Simoska, S., Müller, A., Mishkovski, I. (2025). Entropy, complexity, and spectral features of EEG signals in autism and typical development: a quantitative approach. Front. Psychiatry 16, 1505297. doi: 10.3389/fpsyt.2025.1505297

Wilson, H. R., Cowan, J. D. (1972). Excitatory and Inhibitory Interactions in Localized Populations of Model Neurons. Biophys. J. 12, 1-24. doi: 10.1016/S0006-3495(72)86068-5