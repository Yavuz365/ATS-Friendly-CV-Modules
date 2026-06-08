#!/usr/bin/env python3
"""
run_demo.py — ATS-Friendly-CV-Modules Engine uçtan uca demo.

Çalıştırma (engine/ dizininden):
    python examples/run_demo.py
veya paket kurulduysa:
    python -m examples.run_demo

Bu script; örnek bir iş ilanı (JD), aday framework CV'si (kanıt bankası etiketli)
ve düz bir CV alır; 7 katmanlı ayrıştırma → sentez → audit-düzeltmeli skor →
gap analizi → 6 alanlı raporu üretir ve hem JSON hem Markdown basar.
"""
from __future__ import annotations

import os
import sys

# Paket kökünü yola ekle (kurulum yapılmadan da çalışsın)
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_ROOT = os.path.dirname(HERE)
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from ats_engine import build_report, to_json, to_markdown  # noqa: E402


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main() -> int:
    jd = _read(os.path.join(HERE, "sample_jd_foreign_trade.txt"))
    framework = _read(os.path.join(HERE, "framework_cv.md"))
    cv = _read(os.path.join(HERE, "sample_cv.txt"))

    report = build_report(
        jd_text=jd,
        framework_cv_text=framework,
        cv_text=cv,
        use_sbert=False,        # demo: deterministik, SBERT'siz
        target_low=75.0,
    )

    print("=" * 72)
    print("MARKDOWN RAPOR")
    print("=" * 72)
    print(to_markdown(report))

    print("=" * 72)
    print("JSON (ilk 800 karakter)")
    print("=" * 72)
    blob = to_json(report)
    print(blob[:800] + (" ..." if len(blob) > 800 else ""))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
