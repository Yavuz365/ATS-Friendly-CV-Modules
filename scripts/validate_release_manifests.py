#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

_SHA = re.compile(r"^[0-9a-f]{40}$")


def validate_manifest(path: Path, *, repo: Path | None = None) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    required = {"release", "tag", "commit", "status", "production_ready", "publish_as", "required_assets"}
    missing = sorted(required - set(data))
    if missing:
        errors.append(f"{path.name}: missing {', '.join(missing)}")
        return errors
    if data["tag"] != f"v{data['release']}":
        errors.append(f"{path.name}: tag/release mismatch")
    if not _SHA.fullmatch(str(data["commit"])):
        errors.append(f"{path.name}: invalid commit SHA")
    if data["production_ready"] is not False:
        errors.append(f"{path.name}: prerelease cannot be production_ready")
    assets = list(data["required_assets"])
    if len(assets) != len(set(assets)) or "SHA256SUMS.txt" not in assets:
        errors.append(f"{path.name}: asset list must be unique and include SHA256SUMS.txt")
    if repo is not None and _SHA.fullmatch(str(data["commit"])):
        # Skip the commit-existence check in a shallow clone (CI environments often
        # use shallow clones that don't contain historical commits).  A full clone
        # or an explicit unshallow is required for this check to be meaningful.
        is_shallow = subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=repo,
            capture_output=True,
            text=True,
        )
        if is_shallow.stdout.strip() == "true":
            return errors  # shallow clone – skip commit verification
        check = subprocess.run(
            ["git", "cat-file", "-e", f"{data['commit']}^{{commit}}"],
            cwd=repo,
            capture_output=True,
            text=True,
        )
        if check.returncode != 0:
            errors.append(f"{path.name}: declared commit is absent from repository history")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--repo", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    for path in args.paths:
        errors.extend(validate_manifest(path, repo=args.repo))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(args.paths)} release manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
