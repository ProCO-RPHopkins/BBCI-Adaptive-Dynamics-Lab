# Snapshot provenance

Prepared on 7 September 2026 for Ryan Hopkins. This repository assembles the completed research project; packaging did not change the model equations, recorded results, manuscript, or presentations.

## Source identities

- Original project: <https://github.com/ProCO-RPHopkins/BBCI-Entropic-Plasticity-Simulation>, `master` tree `32e8404d47a2e806e88aa8f358d67ac5dda3f7fa`. Four scientific/content files are archived under `history/julia-prototype/`; each was checked against its Git blob SHA. Editor settings are not part of the scientific archive.
- Adaptive Dynamics Lab: <https://bbci-entropic-research-lab.ryan-hopkins.chatgpt.site>, saved Site version 1. The exported tracked source is commit `435ebfc123a2cd01e42232ea9a0a1f9433c0bda9`. Every original tracked lab file is included, with a separate packaging README added.
- Research package: all 44 files from the delivered `BBCI_Research_Package.zip` are retained unchanged under `research/`. Its internal manifest and model hash remain intact.
- Manuscript and presentations: the delivered files are copied byte-for-byte. The decks retain their complete speaker notes and citations. All 29 final slide preview PNGs and both generated illustrations are also included.
- Historical paper: the user's attached earlier paper is archived unchanged with a shorter filename.

## Authoring adaptations

The manuscript, notebook, and deck authoring scripts now resolve paths relative to this repository and write regenerated output to `build/generated/`. They no longer depend on the original scratch directory or overwrite the delivered artifacts. Citation metadata is reduced to the fields needed by the manuscript builder. The full fetched publisher metadata and article abstracts are omitted; the author's evidence summaries, bibliography, and source links remain available.

The numerical model and notebook are Python. The browser's live model is a JavaScript port. Existing numerical verification and the original Python/JavaScript agreement check are recorded in the research package. Packaging checks verify file integrity, JavaScript syntax, import paths, and local documentation links; they do not constitute an independent replication or clinical validation.

## Reproduction limits

- The Python model and static lab are runnable with the documented dependencies. The static lab vendors its viewer dependencies and data.
- Presentation regeneration requires the preparation environment's `@oai/artifact-tool` package (version 2.8.52). The editable PPTX files do not require that package for use.
- The Word builder used `python-docx` 1.2.0. PDF rendering and final visual inspection are separate from DOCX generation.
- The notebook contains actual in-process Python outputs. Its Jupyter frontend was not exercised during preparation.
- Generated illustrations are retained as source assets. No claim is made that an image model will reproduce them from a prompt.

Temporary caches, dependency installations, credentials, intermediate rendering attempts, and fetched article abstracts are not project artifacts. The GitHub source export does not change the live lab's access controls or deployment.

## GitHub publication update

The user created the public repository `ProCO-RPHopkins/BBCI-Adaptive-Dynamics-Lab` and authorized adding a license and visual overview. The root README, citation repository URL, MIT software license, and CC BY 4.0 content license were added for that publication. These supersede the earlier licensing-pending statements only for the materials explicitly covered in `RIGHTS.md`.

The README gained a generated cover and an animation built from the recorded `0_combined` example. The animation samples the 20-Hz reference once per model second and plays at six frames per second. Its surface color scale is fixed at 0–0.4 throughout. `authoring/build_readme_animation.py` and `assets/readme/PROVENANCE.md` record how the visuals were prepared. The original paper, slides, research results, and lab runtime files remain byte-identical to the delivered versions.
