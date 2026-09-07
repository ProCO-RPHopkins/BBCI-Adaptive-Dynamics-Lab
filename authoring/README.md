# Artifact authoring

The delivered PDF, Word file, PowerPoint files, and notebook are retained unchanged in `artifacts/` and `research/`. These scripts are portable adaptations of their preparation scripts. They locate inputs relative to this repository and write regenerated outputs under ignored `build/generated/`.

## Manuscript

`build_manuscript.py` reads `manuscript_body.md`, the 22-source `reference_metadata.json`, the study summary, and final figure PNGs. It creates the editable Word document and accompanying reference exports. Install `python-docx` in addition to the research requirements, then run from the repository root:

```bash
python authoring/build_manuscript.py
```

The delivered PDF was exported and visually inspected separately. Rebuilding the DOCX does not regenerate or revalidate that PDF. Word-to-PDF pagination depends on fonts and the rendering application; inspect any new export before sharing it.

## Notebook

```bash
python authoring/build_notebook.py
```

This executes real code cells in-process and captures stdout and Matplotlib images. It records the execution method in notebook metadata and exports the current numerical environment separately. The original environment could not launch a socket-based Jupyter kernel; it did not test the Jupyter frontend. The delivered notebook already contains computed outputs.

## Presentations

`build_decks.mjs` uses Node ES modules and `@oai/artifact-tool`. It creates editable slides, notes, and preview renders. The artifact authoring package is supplied by the preparation runtime and is not bundled or represented as a universally available npm dependency. In an environment with that package installed:

```bash
node authoring/build_decks.mjs
```

The PPTX files can be edited directly in PowerPoint or a compatible application without this authoring dependency. All 29 original slide preview images are included under `artifacts/presentations/previews/`. Regenerated decks require a fresh layout review before distribution.
