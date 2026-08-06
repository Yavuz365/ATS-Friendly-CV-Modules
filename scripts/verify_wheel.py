#!/usr/bin/env python3
"""Verify the runtime wheel manifest without importing from the source tree."""

from __future__ import annotations

import sys
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_wheel.py path/to/wheel.whl", file=sys.stderr)
        return 2
    wheel = Path(sys.argv[1])
    if not wheel.is_file():
        print(f"wheel not found: {wheel}", file=sys.stderr)
        return 2
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    missing = sorted(REQUIRED - names)
    if missing:
        print("missing wheel members:\n" + "\n".join(missing), file=sys.stderr)
        return 1
    print(f"wheel manifest OK: {wheel.name} ({len(names)} members)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
