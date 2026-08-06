"""EVAL-003 — Evaluation cards must exist as versioned, non-empty artifacts."""

from __future__ import annotations

from pathlib import Path

_CARDS = Path(__file__).resolve().parents[2] / "evaluation" / "cards"

_REQUIRED = (
    "README.md",
    "parser-card.md",
    "requirement-card.md",
    "matching-card.md",
    "synthesis-gate-card.md",
)


def test_all_evaluation_cards_exist() -> None:
    for name in _REQUIRED:
        path = _CARDS / name
        assert path.is_file(), f"missing card: {name}"
        text = path.read_text(encoding="utf-8")
        assert len(text.strip()) > 100, f"card too short: {name}"
        assert "NOT_MEASURED" in text or name == "README.md"


def test_cards_avoid_forbidden_product_language() -> None:
    forbidden = ("interview-ready", "ats passed", "ats pass rate", "guaranteed interview")
    for name in _REQUIRED:
        if name == "README.md":
            continue
        text = (_CARDS / name).read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text, f"{name} contains forbidden phrase: {phrase}"
