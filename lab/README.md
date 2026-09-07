# BBCI · Adaptive Dynamics Lab

This directory is a source snapshot of the working lab. Serve `dist/` with any ordinary static HTTP server. It includes all local runtime assets; it has no backend, credentials, npm installation, or build requirement.

From the repository root:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory lab/dist
```

Open <http://localhost:8000>. The Web Worker runs the JavaScript port of the synthetic neural-mass model. `web_data.json` contains recorded reference runs, individual calibrations, and benchmark summaries. `brain.json` contains display geometry. The authoritative Python implementation is `../research/bbci/model.py`.

The existing Sites configuration is retained for provenance. The live Site and its access settings are managed separately; exporting this source does not redeploy the Site or change who can visit it. Static hosting elsewhere does not inherit the current hosted Site's access restrictions.
