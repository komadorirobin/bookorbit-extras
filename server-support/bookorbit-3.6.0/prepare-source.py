#!/usr/bin/env python3
"""Apply verified extras to a separate, clean, exact BookOrbit 3.6.0 checkout.

No deployment, database access, package installation or container operation.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git(checkout, *args, **kwargs):
    return subprocess.run(["git", "-C", str(checkout), *args], check=True,
                          stdout=subprocess.PIPE, **kwargs).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--features", choices=("undo", "tags", "both"), default="both")
    parser.add_argument("--source-archive", type=Path,
                        help="Create full corresponding source outside the checkout (not only a diff)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    release = json.loads((root / "compatibility.json").read_text())["stableServer"]
    checkout = args.checkout.resolve(strict=True)
    if Path(git(checkout, "rev-parse", "--show-toplevel").decode().strip()).resolve() != checkout:
        parser.error("Pass the source checkout root, not a subdirectory.")
    if git(checkout, "rev-parse", "HEAD").decode().strip() != release["serverBase"]:
        parser.error("Wrong source revision. Only the pinned official 3.6.0 commit is supported.")
    if git(checkout, "status", "--porcelain").strip():
        parser.error("Use a separate clean checkout. No existing work will be overwritten.")
    names = ("undo", "tags") if args.features == "both" else (args.features,)
    payload = bytearray()
    for name in names:
        entry = release[name]
        patch = (root / entry["patch"]).read_bytes()
        if hashlib.sha256(patch).hexdigest() != entry["sha256"]:
            parser.error(f"Patch checksum mismatch: {name}")
        payload.extend(patch)
    archive = args.source_archive.resolve() if args.source_archive else None
    if archive and (archive.exists() or checkout == archive or checkout in archive.parents):
        parser.error("Choose a new source archive outside the source checkout.")
    if archive and not archive.parent.is_dir():
        parser.error("The source archive parent directory must already exist.")
    git(checkout, "apply", "--check", "--index", input=payload)
    git(checkout, "apply", "--index", input=payload)
    tree = git(checkout, "write-tree").decode().strip()
    if archive:
        with archive.open("xb") as output:
            subprocess.run(["git", "-C", str(checkout), "archive", "--format=tar.gz",
                            "--prefix=bookorbit-extras-source/", tree], check=True, stdout=output)
    print(f"Prepared BookOrbit {release['serverVersion']} with {args.features}; source tree {tree}")
    if archive:
        print(f"Full corresponding source: {archive}")
    print("No server was deployed and no database was changed. Review the version-specific README.")


if __name__ == "__main__":
    main()
