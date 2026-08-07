"""JOB-004 — Extractor behaviour against the annotated requirement gold set.

Rules enforced here:
- Every gold sentence must produce exactly one REVIEW requirement.
- Category, modality and negation must match the gold label.
- Span text must equal the gold sentence.
- Body-keyword-only text must produce zero requirements (no promotion).
"""

from __future__ import annotations

import json
from pathlib import Path

from ats_engine.contracts import ProcessStatus
from ats_engine.job_requirements import extract_job_requirements

_REPO_ROOT = Path(__file__).resolve().parents[2]
_GOLD_PATH = _REPO_ROOT / "evaluation" / "requirements" / "labels.json"


def _load_gold() -> dict:
    with _GOLD_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def test_gold_file_exists_and_has_twelve_labels() -> None:
    data = _load_gold()
    assert data["dataset_id"] == "ats-requirement-gold"
    assert data["contains_personal_data"] is False
    assert len(data["labels"]) == 12


def test_each_gold_sentence_extracts_matching_requirement() -> None:
    data = _load_gold()
    for label in data["labels"]:
        job_id = f"GOLD-{label['fixture_id']}"
        result = extract_job_requirements(job_id, label["text"])

        assert result.review_required is True, label["fixture_id"]
        assert len(result.requirements) == 1, label["fixture_id"]

        req = result.requirements[0]
        assert req.review_status is ProcessStatus.REVIEW
        assert req.category == label["category"], label["fixture_id"]
        assert req.modality == label["modality"], label["fixture_id"]
        assert req.negated is label["negated"], label["fixture_id"]
        assert req.text == label["text"]
        assert label["text"][req.span_start : req.span_end] == req.text


def test_body_keywords_alone_are_never_promoted() -> None:
    """Regression: keyword soup without requirement signal → empty."""
    text = "SAP ERP Incoterms gümrük lojistik akreditif. Global pazarlarda faaliyet."
    result = extract_job_requirements("GOLD-BODY-ONLY", text)
    assert result.requirements == []
    assert result.review_required is False


def test_mixed_paragraph_preserves_all_gold_signals() -> None:
    """Concatenate several gold sentences; every signal must survive."""
    data = _load_gold()
    selected = [
        item
        for item in data["labels"]
        if item["fixture_id"]
        in {
            "REQ-EN-MUST-001",
            "REQ-EN-NEG-001",
            "REQ-TR-PREF-001",
            "REQ-TR-NEG-001",
        }
    ]
    paragraph = " ".join(item["text"] for item in selected)
    result = extract_job_requirements("GOLD-MIXED", paragraph)

    assert len(result.requirements) == len(selected)
    modalities = {r.modality for r in result.requirements}
    assert "MUST" in modalities
    assert "PREFERRED" in modalities
    assert any(r.negated for r in result.requirements)
    assert all(r.review_status is ProcessStatus.REVIEW for r in result.requirements)
