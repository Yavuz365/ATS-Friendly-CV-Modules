"""EVAL-003 / EVAL-002 — Evaluation cards are versioned and evidence-bound."""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_CARDS = _ROOT / "evaluation" / "cards"

_REQUIRED = (
    "README.md",
    "parser-card.md",
    "requirement-card.md",
    "matching-card.md",
    "synthesis-gate-card.md",
    "provenance-card.md",
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


def test_documented_fixture_counts_match_datasets() -> None:
    gold = json.loads((_ROOT / "evaluation" / "gold" / "manifest.json").read_text(encoding="utf-8"))
    requirements = json.loads(
        (_ROOT / "evaluation" / "requirements" / "labels.json").read_text(encoding="utf-8")
    )
    esco = json.loads(
        (_ROOT / "engine" / "ats_engine" / "data" / "esco_micro_v1_2_1.json").read_text(encoding="utf-8")
    )

    parser_card = (_CARDS / "parser-card.md").read_text(encoding="utf-8")
    requirement_card = (_CARDS / "requirement-card.md").read_text(encoding="utf-8")
    matching_card = (_CARDS / "matching-card.md").read_text(encoding="utf-8")

    assert f"Fixtures (n={len(gold['fixtures'])})" in parser_card
    assert f"gold set v{requirements['dataset_version']} ({len(requirements['labels'])} fixtures)" in requirement_card
    assert f"ESCO micro subset ({len(esco['concepts'])} concepts)" in matching_card


def test_cards_reference_existing_test_files() -> None:
    referenced = {
        "parser-card.md": ("test_gold_corpus.py", "test_field_evaluation.py"),
        "requirement-card.md": ("test_requirement_gold.py", "test_job_requirements.py"),
        "matching-card.md": ("test_matching_cascade.py", "test_esco_adapter.py"),
        "synthesis-gate-card.md": ("test_regressions.py", "test_contracts_ingestion.py"),
        "provenance-card.md": ("test_provenance.py",),
    }
    tests_dir = _ROOT / "engine" / "tests"
    for card_name, test_names in referenced.items():
        card_text = (_CARDS / card_name).read_text(encoding="utf-8")
        for test_name in test_names:
            assert (tests_dir / test_name).is_file(), f"missing referenced test: {test_name}"
            assert test_name in card_text, f"{card_name} does not mention {test_name}"
