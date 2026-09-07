"""Verify the packaged research snapshot without installing scientific dependencies."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
failures = []
for name, expected in manifest['files'].items():
    path = ROOT / name
    if not path.is_file():
        failures.append(f'Missing: {name}')
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append(f'Changed: {name}')
if failures:
    print('\n'.join(failures))
    sys.exit(1)
print(f"Verified {len(manifest['files'])} packaged files against SHA-256 hashes.")
print('This confirms snapshot integrity; it is not a scientific or clinical validation.')
