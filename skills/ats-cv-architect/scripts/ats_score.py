#!/usr/bin/env python3
"""Compatibility entry point for the canonical ats_engine CLI.

There is intentionally no standalone fallback engine: a fallback would bypass
the versioned status/error/evidence contracts and recreate implementation drift.
"""

from __future__ import annotations

import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[3] / "engine"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from ats_engine.cli import main  # noqa: E402
from ats_engine.scoring import ats_match_score  # noqa: E402,F401


if __name__ == "__main__":
    raise SystemExit(main(["score", *sys.argv[1:]]))
