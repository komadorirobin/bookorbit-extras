"""Verify distributable bytes without a network, account or device."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "compatibility.json").read_text())
expected = dict(manifest["deviceSource"]["files"])
for key in ("undoOpeningV1", "tagMatchesV1"):
    entry = manifest[key]
    expected[entry["patch"]] = entry["sha256"]
for name, digest in expected.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
for name in ("LICENSE", "NOTICE", "ADDITIONAL_TERMS.md"):
    assert (root / "licenses/bookorbit" / name).stat().st_size > 100, name
assert manifest["serverPatchesAreNotCombined"] is True
assert manifest["automaticDeployment"] is False
print("PASS: four pinned artifacts, notices, independent bases and no deployment")
