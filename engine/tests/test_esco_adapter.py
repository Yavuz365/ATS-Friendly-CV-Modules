"""MAT-003 — ESCO adapter must abstain by default and never invent matches."""

from __future__ import annotations

from ats_engine.esco_adapter import (
    EscoAdapterConfig,
    build_esco_adapter,
    esco_adapter_status,
)
from ats_engine.matching import AdapterStatus, match_term


def test_esco_adapter_disabled_by_default_returns_none() -> None:
    adapter = build_esco_adapter()
    assert adapter is None


def test_esco_adapter_status_reports_safe_defaults() -> None:
    status = esco_adapter_status()
    assert status["enabled"] is False
    assert status["produces_verified_pass"] is False
    assert status["default_behaviour"] == "NOT_RUN / abstain"
    assert status["version"] == "1.2.1"


def test_esco_enabled_without_data_abstains() -> None:
    cfg = EscoAdapterConfig(enabled=True)
    adapter = build_esco_adapter(config=cfg)
    assert adapter is not None
    assert adapter.adapter_id == "esco-ontology"
    assert adapter.revision == "2025-12-esco-v1.2.1-pin"

    result = adapter.matcher("incoterms", "Candidate has foreign trade experience.")
    assert result.status is AdapterStatus.NOT_RUN


def test_match_term_skips_ontology_when_adapter_is_none() -> None:
    """Cascade must not fail when ontology adapter is absent (default)."""
    tm = match_term("incoterms", "No matching text here at all.")
    assert tm.matched is False
    assert tm.stage.value == "NONE"
