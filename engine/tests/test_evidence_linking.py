"""MAT-001: requirement/evidence locator linkage + measured false-support rate."""

from __future__ import annotations

from pathlib import Path

from ats_engine.contracts import JobRequirement, VerificationStatus
from ats_engine.evidence_linking import link_requirement_evidence, measure_exact_match_false_support_rate

_GOLD_PATH = Path(__file__).resolve().parents[2] / "evaluation" / "gold" / "exact_match_support_labels.json"


def _requirement(text: str = "Incoterms zorunludur.") -> JobRequirement:
    return JobRequirement(
        id="REQ-1",
        job_posting_id="JOB-1",
        text=text,
        requirement_type="EXPLICIT_SENTENCE",
        explicit=True,
    )


def test_matched_term_produces_locator_bearing_evidence_and_map():
    cv = "Deneyimlerim arasında Incoterms 2020 kurallarına hakimiyet bulunmaktadır."
    req_map, tm, evidence = link_requirement_evidence(
        _requirement(), "incoterms", cv, source_artifact_id="SRC-1", candidate_fact_id="FACT-1"
    )
    assert tm.matched is True
    assert evidence is not None
    assert evidence.locator.startswith("char:")
    start, end = (int(x) for x in evidence.locator.removeprefix("char:").split("-"))
    assert cv[start:end].lower() == "incoterms"
    assert "incoterms" in evidence.excerpt.lower()
    assert req_map.evidence_ids == [evidence.id]
    # CCR-018/STAB-019: a lexical boundary match is a support signal, never
    # promoted to full VERIFIED on its own.
    assert req_map.verification_status is VerificationStatus.PARTIAL
    assert evidence.verification_status is VerificationStatus.PARTIAL


def test_no_match_produces_empty_evidence_map_with_honest_reason():
    req_map, tm, evidence = link_requirement_evidence(
        _requirement(),
        "sap",
        "Bu CV'de hiç ERP sistemi geçmiyor.",
        source_artifact_id="SRC-1",
        candidate_fact_id="FACT-1",
    )
    assert tm.matched is False
    assert evidence is None
    assert req_map.evidence_ids == []
    assert req_map.verification_status is VerificationStatus.UNVERIFIED
    assert "sap" in req_map.reason.lower()


def test_evidence_id_is_stable_for_same_inputs():
    cv = "Incoterms konusunda deneyimliyim."
    map1, _, ev1 = link_requirement_evidence(
        _requirement(), "incoterms", cv, source_artifact_id="SRC-1", candidate_fact_id="FACT-1"
    )
    map2, _, ev2 = link_requirement_evidence(
        _requirement(), "incoterms", cv, source_artifact_id="SRC-1", candidate_fact_id="FACT-1"
    )
    assert ev1.id == ev2.id
    assert map1.evidence_ids == map2.evidence_ids


def test_measured_false_support_rate_is_computed_from_real_gold_fixtures():
    result = measure_exact_match_false_support_rate(_GOLD_PATH)
    assert result["sample_size"] == 12
    assert result["negative_gold_count"] == 7
    assert result["positive_gold_count"] == 5
    # Real measured value on this fixture set (see dataset card) — pinned so
    # a future matcher change that silently starts ignoring negation/context
    # cases differently is caught, not silently re-measured into a new claim.
    assert result["false_support_rate"] == 1.0
    assert result["true_positive_recall"] == 1.0
    assert len(result["false_support_errors"]) == 7
    assert "not a statistically powered" in result["limitation"]
