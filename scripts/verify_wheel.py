#!/usr/bin/env python3
"""Verify the runtime wheel and sdist manifests without importing from the source tree."""

from __future__ import annotations

import sys
import tarfile
import zipfile
from pathlib import Path

REQUIRED = {
    "ats_engine/__init__.py",
    "ats_engine/contracts.py",
    "ats_engine/configuration.py",
    "ats_engine/decision.py",
    "ats_engine/errors.py",
    "ats_engine/ingestion.py",
    "ats_engine/legacy_adapter.py",
    "ats_engine/matching.py",
    "ats_engine/safe_synthesis.py",
    "ats_engine/data/action_verbs.json",
    "ats_engine/data/skill_synonyms.json",
    "ats_engine/data/stopwords_tr_en.txt",
    "ats_engine/domain_pack_data/foreign-trade-logistics/keywords_en.json",
    "ats_engine/domain_pack_data/foreign-trade-logistics/keywords_tr.json",
}


def _check_wheel(wheel: Path) -> list[str]:
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    missing = sorted(REQUIRED - names)
    if missing:
        return [f"wheel missing: {m}" for m in missing]
    return []


def _check_sdist(sdist: Path) -> list[str]:
    with tarfile.open(sdist, "r:gz") as archive:
        names = [m.name for m in archive.getmembers()]
    errors = []
    for req in sorted(REQUIRED):
        suffix = f"/{req}"
        if not any(n.endswith(suffix) for n in names):
            errors.append(f"sdist missing: {req}")
    return errors


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("usage: verify_wheel.py <wheel.whl> [sdist.tar.gz]", file=sys.stderr)
        return 2

    errors: list[str] = []
    wheel_path: Path | None = None
    sdist_path: Path | None = None

    for arg in args:
        p = Path(arg)
        if not p.is_file():
            print(f"artifact not found: {p}", file=sys.stderr)
            return 2
        if p.suffix == ".whl":
            wheel_path = p
        elif arg.endswith(".tar.gz"):
            sdist_path = p
        else:
            print(f"unrecognised artifact: {p}", file=sys.stderr)
            return 2

    if wheel_path:
        errors.extend(_check_wheel(wheel_path))
    if sdist_path:
        errors.extend(_check_sdist(sdist_path))

    if errors:
        print("manifest errors:\n" + "\n".join(errors), file=sys.stderr)
        return 1

    parts = []
    if wheel_path:
        parts.append(f"wheel OK: {wheel_path.name}")
    if sdist_path:
        parts.append(f"sdist OK: {sdist_path.name}")
    print("; ".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
