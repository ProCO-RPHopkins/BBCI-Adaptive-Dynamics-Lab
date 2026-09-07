# Results files

`all_runs.csv`: one row per scenario × synthetic individual × evaluation seed × strategy. `tracking_mse` is unbounded continuous-readout mean squared error; `accuracy` is a proportion; `control_energy` is mean squared dimensionless input. Evaluation uses seconds 15–45. `washout_mse` uses seconds 47–60. Weight measures are relative Frobenius changes.

`summary.json`: means and [mean, lower, upper] percentile-bootstrap summaries. Seeds are averaged within individuals; bootstrap sample size is 24 individuals with 4,000 draws. `calibration.json` contains the independent reference and readout for each individual.

`gain_sweep.csv`: eight individuals at eleven gain levels. `phase_surrogates.csv`: eight individuals with forty phase surrogates each; these use whole-record entropy, unlike online one-second windows. `step_size_check.csv`: stochastic step sensitivity without matched paths. `validation.json`: thirteen software/numerical checks, including a distinct deterministic solver comparison.

`pilot_high_noise_summary.json`: retained exploratory pilot using sensor SD 0.01. Its results were not substituted for the final experiment, which uses SD 0.001 nominally and SD 0.05 in the noise stress condition.

`web_data.json`: 20-Hz reference animations and original 100-Hz metrics. Its study result hash identifies the same Python model. The browser port is maintained with the hosted Site.

`environment.json` records the Python preparation environment. JupyterLab is an optional frontend dependency; notebook cells were executed in-process because the preparation environment disallows kernel sockets. The notebook contains actual computed outputs.
