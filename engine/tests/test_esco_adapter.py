"""MAT-003 — ESCO adapter must abstain by default and only signal review when enabled."""

from __future__ import annotations

from ats_engine.esco_adapter import (
    EscoAdapterConfig,
    build_esco_adapter,
    esco_adapter_status,
)
from ats_engine.matching import AdapterStatus, MatchStage, match_term


def test_esco_adapter_disabled_by_default_returns_none() -> None:
    adapter = build_esco_adapter()
    assert adapter is None


def test_esco_adapter_status_reports_safe_defaults() -> None:
    status = esco_adapter_status()
    assert status["enabled"] is False
    assert status["produces_verified_pass"] is False
    assert status["default_behaviour"] == "NOT_RUN / abstain"
    assert status["version"] == "1.2.1"
    assert status["concept_count"] == 0


def test_esco_enabled_loads_micro_subset_and_can_match() -> None:
    cfg = EscoAdapterConfig(enabled=True)
    adapter = build_esco_adapter(config=cfg)
    assert adapter is not None
    assert adapter.adapter_id == "esco-ontology"
    assert adapter.revision == "2025-12-esco-v1.2.1-pin"

    # Term is an ESCO micro label and appears in text with boundaries.
    result = adapter.matcher("incoterms", "Candidate applied Incoterms 2020 on exports.")
    assert result.status is AdapterStatus.MATCH
    assert result.matched_variant is not None
    assert "review" in (result.explanation or "").lower() or "human" in (result.explanation or "").lower()


def test_esco_enabled_no_match_when_label_absent_from_text() -> None:
    cfg = EscoAdapterConfig(enabled=True)
    adapter = build_esco_adapter(config=cfg)
    assert adapter is not None
    result = adapter.matcher("incoterms", "No commercial terms mentioned here.")
    assert result.status is AdapterStatus.NO_MATCH


def test_match_term_skips_ontology_when_adapter_is_none() -> None:
    tm = match_term("incoterms", "No matching text here at all.")
    assert tm.matched is False
    assert tm.stage is MatchStage.NONE


def test_match_term_ontology_stage_is_review_required_when_enabled() -> None:
    cfg = EscoAdapterConfig(enabled=True)
    adapter = build_esco_adapter(config=cfg)
    assert adapter is not None

    tm = match_term(
        "incoterms",
        "Experience with Incoterms is documented.",
        ontology_adapter=adapter,
        allow_fuzzy=False,
    )
    assert tm.matched is True
    assert tm.stage is MatchStage.ONTOLOGY
    assert tm.review_required is True
    assert tm.adapter_id == "esco-ontology"
