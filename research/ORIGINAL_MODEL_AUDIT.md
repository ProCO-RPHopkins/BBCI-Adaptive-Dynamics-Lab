# Audit of the starting work

Inspected source: https://github.com/ProCO-RPHopkins/BBCI-Entropic-Plasticity-Simulation, master branch, 7 September 2026. The original repository was not modified.

`bbciSim.jl` blob: `f52f9b84294b6b6bb04a56218c2a97471867c8c5`.
README blob: `734eb1edd3466fda69a68baf468fc9265112f642`.
The supplied notebook contains 24 cells and reports Julia 1.11.3.

| Starting implementation | Consequence | New implementation |
|---|---|---|
| Random walks labeled neural activity | No bounded neural population dynamics; values can become negative | Bounded excitatory/inhibitory population model |
| “Entropy” operation replaces activity with scaled random noise | Does not estimate signal entropy or implement a receptor mechanism | Explicit ordinal-pattern permutation entropy; separate current noise and sensor noise |
| Classification target is region identity | Classification does not demonstrate intent decoding or functional recovery | Separate binary input and frozen, separately calibrated task readout |
| Matrix reshape uses Julia column-major ordering | Can scramble intended observation layout | Explicit time-by-population arrays and indexed features |
| Softmax output combined with logit cross-entropy | Inconsistent probability/logit interface | Ridge readout with continuous error and sign accuracy |
| Notebook records undefined `Flux` and `y_oh` errors | Recorded workflow does not complete as presented | Executed Python notebook and reproducible scripts |
| Mixed Flux optimizer idioms, no pinned environment | Compatibility cannot be assumed across package versions | Tested dependency versions and environment manifest |
| Algebraic pull of one region toward the other | Synchronization is imposed, not evidence of synaptic learning | Explicit bounded covariance weight rule and washout check |
| No seeded held-out benchmark or meaningful ablations | Generalization and causal interpretation untested | Separate calibration, evaluation seeds, fixed/rate/entropy/combined/yoked controls |
| Strong therapeutic language in README | Model output is not clinical validation | Claims confined to synthetic engineering outcomes |

The new implementation is an independently structured benchmark. It does not claim numerical equivalence to the Julia prototype.

## Changes beyond the supplied July 26, 2026 review

- Implemented and executed the previously conceptual closed-loop experiment, including negative task results and measurement failures.
- Added the August 19, 2026 Nature context-alignment study and checked 2026 clinical and heterogeneity evidence against primary records.
- Corrected the inference that a reported low-complexity finding would make an entropy increase “directionally reversed.” Direction alone still does not identify a beneficial intervention.
- Distinguished a normative deviation from a justified target and an individual's reference state from an empirically demonstrated optimum.
- Avoided categorical claims of either reliable individual measures or unreliable group measures; reliability depends on data, scale, estimator and study design.
- Replaced proposed preregistration language with an accurate exploratory designation. Future preregistration is a recommendation, not an accomplished step.
- Preserved the distinction between a legitimate stochastic process term and an unsupported claim that injected randomness models psychedelic therapy.
- Did not claim that ABIDE provides standardized diffusion connectomes for all individuals or that an empirically fitted 68–200-region model has been completed.

## Development transparency

Pilot ranges with stronger local recurrence had poor reference decoding. The final local recurrent range was reduced to 2.5–4.5. A moderate sensor-noise pilot (SD 0.01) produced weak entropy response slopes; its aggregate summary is retained. The final SD 0.001 case is explicitly favorable and was paired with a higher-noise stress condition. Neither selection was preregistered or based on patient measurements. These choices constrain the generality of the results.
