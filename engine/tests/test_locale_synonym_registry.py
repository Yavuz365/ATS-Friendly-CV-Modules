"""MAT-002: accepted, versioned, conflict-tested reviewed-synonym dataset."""

from __future__ import annotations

from pathlib import Path

import pytest

from ats_engine.locale_synonym_registry import (
    accepted_synonyms,
    audit_reviewed_synonym_conflicts,
    load_reviewed_locale_synonyms,
)
from ats_engine.matching import MatchStage, match_term, reviewed_synonym_revision

_DATASET_PATH = Path(__file__).resolve().parents[2] / "evaluation" / "gold" / "reviewed_locale_synonyms_tr_en.json"


def test_dataset_loads_and_has_both_accepted_and_abstained_sections():
    data = load_reviewed_locale_synonyms(_DATASET_PATH)
    assert len(data["accepted"]) >= 10
    assert len(data["abstained"]) >= 3
    for item in data["abstained"]:
        assert item["reason"], "every abstained pair must record why it was rejected"


def test_accepted_dataset_has_no_internal_conflicts():
    data = load_reviewed_locale_synonyms(_DATASET_PATH)
    accepted = accepted_synonyms(data)
    conflicts = audit_reviewed_synonym_conflicts(accepted)
    assert conflicts == []


def test_conflict_audit_detects_a_variant_claimed_by_two_keys():
    accepted = {"a": ["shared-term"], "b": ["shared-term"]}
    conflicts = audit_reviewed_synonym_conflicts(accepted)
    assert len(conflicts) == 1


def test_accepted_pair_drives_a_real_synonym_match():
    data = load_reviewed_locale_synonyms(_DATASET_PATH)
    accepted = accepted_synonyms(data)
    revision = reviewed_synonym_revision(accepted)
    result = match_term(
        "gümrük",
        "Managed customs clearance operations for 3 years.",
        reviewed_synonyms=accepted,
        synonym_revision=revision,
        allow_fuzzy=False,
    )
    assert result.matched is True
    assert result.stage is MatchStage.SYNONYM
    assert result.adapter_revision == revision


def test_abstained_pair_is_not_present_in_the_accepted_mapping():
    data = load_reviewed_locale_synonyms(_DATASET_PATH)
    accepted = accepted_synonyms(data)
    sap_variants = {v.lower() for v in accepted.get("sap", [])}
    assert "erp" not in sap_variants, "SAP/ERP was explicitly abstained; must not silently reappear as accepted"


@pytest.mark.parametrize("required_key", ["sap", "gümrük", "yüksek lisans"])
def test_abstained_candidate_keys_are_documented(required_key):
    data = load_reviewed_locale_synonyms(_DATASET_PATH)
    keys = {item["candidate_key"] for item in data["abstained"]}
    assert required_key in keys
