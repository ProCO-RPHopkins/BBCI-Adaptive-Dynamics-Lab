# BBCI / entropy feedback research benchmark

A reproducible, exploratory neural-mass benchmark accompanying **Entropy-informed feedback in autism neuromodulation research: a falsifiable neural-mass benchmark**. Prepared for Ryan Hopkins, 7 September 2026.

The project tests whether an individually calibrated entropy term adds useful control information beyond rate feedback. It does **not** simulate a diagnosed autistic brain, deliver stimulation, recommend a drug or establish a therapy.

## Start here

- Interactive brain and live simulation: https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site (owner access).
- `BBCI_Research_Notebook.ipynb`: executed, self-contained model demonstration, with an embedded copy of the Python model and recorded aggregate results. Open in JupyterLab. No network connection is required after dependencies are installed.
- `bbci/model.py`: authoritative model implementation.
- `results/all_runs.csv`: all 1,296 final evaluation runs.
- `results/summary.json`: individual-level bootstrap summaries, contrasts and code hash.
- `EVIDENCE_LEDGER.md`: peer-reviewed evidence and limits of inference.
- `ORIGINAL_MODEL_AUDIT.md`: what changed from the Julia prototype and prior review.
- `SUBMISSION_NOTES.md`: journal format, author verification and remaining submission tasks.

## Reproduce

Use Python 3.12 (the tested version), preferably in a fresh virtual environment.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_experiments.py
python validate.py
python make_figures.py
jupyter lab BBCI_Research_Notebook.ipynb
```

The full experiment took approximately one minute on the preparation machine after compilation; hardware and first-run compilation affect timing. Re-running overwrites the reproducible final result files. The preserved pilot summary is separate.

## Experimental design

24 synthetic parameter sets × 3 evaluation seeds × 6 nominal strategies = 432 runs. Four separate robustness conditions each test no input, rate and combined feedback, adding 864 runs. Calibration, baseline validation, gain sweeps, phase surrogates and numerical checks are additional simulations, not part of the 1,296 count.

The same individual and seed share task/noise streams across strategies. Bootstrap intervals resample 24 individuals after averaging their seeds. They are neither patient treatment intervals nor a posterior over plausible models. The study is exploratory and was not preregistered.

The primary contrast is combined minus rate tracking MSE. In nominal conditions it is −4.533 [−6.543, −2.834]. Accuracy is approximately 50% for both; an unperturbed held-out reference is 80.27%. Sensor noise reverses the MSE contrast to +8.283 [4.604, 12.653]. Fixed input has lower mean error than either adaptive strategy but has different calibration access. Interpret these results together.

## Important implementation details

All activities, gains and input amplitudes are dimensionless. Time is in seconds. The observer is a population average with added noise; the task readout has favorable access to latent states. There is no EEG forward model, stimulation field solution, receptor model, conduction delay or patient-fitted connectome. Plasticity is bounded rate covariance with imposed relaxation, not evidence of lasting learning.

`simulate` supports `dynamic_noise=0` for the deterministic numerical check; the benchmark uses the default 0.04. The moderate-noise pilot used sensor SD 0.01; the final nominal experiment uses 0.001. This refinement was an exploratory choice to study an informative calibration regime, not a clinical sensor specification.

The browser runs a JavaScript port in a Web Worker. Reference animations are downsampled to 20 Hz, but displayed benchmark outcomes use the original 100-Hz Python evaluation. Live custom runs retain the original reference calibration when parameters change; this intentionally exposes calibration mismatch. The cortical template is visual geometry, not patient data. The Site source is maintained separately from this Python research package.

## Verification and limitations

`validate.py` performs 13 checks, including an independent ODE solver comparison. The numerical convergence test covers a short deterministic interval; `step_size_check.csv` is a separate stochastic sensitivity analysis and does not match Brownian paths across step sizes. `results/validation.json` records this distinction.

Notebook code cells were executed in-process with actual Python outputs because the preparation environment cannot open Jupyter kernel sockets; the Jupyter frontend itself was not exercised.

The notebook's aggregate results are embedded from the full benchmark. Executing the notebook reruns its single-individual demonstration, not all 1,296 evaluations; use `run_experiments.py` for that. No human clinical outcomes are generated. Public code licensing and an archival DOI should be finalized by the author before journal submission.
