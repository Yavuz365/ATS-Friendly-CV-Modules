from __future__ import annotations

import pytest

from ats_engine.matching import (
    AdapterResult,
    AdapterStatus,
    MatchStage,
    VersionedMatchAdapter,
    match_term,
    reviewed_synonym_revision,
)


def test_reviewed_locale_synonym_is_revision_bound():
    synonyms = {"gümrük": ["customs clearance", "customs operations"]}
    revision = reviewed_synonym_revision(synonyms)
    result = match_term(
        "gümrük",
        "Managed customs clearance and import documentation.",
        reviewed_synonyms=synonyms,
        synonym_revision=revision,
        allow_fuzzy=False,
    )
    assert result.matched is True
    assert result.stage is MatchStage.SYNONYM
    assert result.matched_variant == "customs clearance"
    assert result.adapter_revision == revision


def test_floating_adapter_revision_is_rejected():
    with pytest.raises(ValueError, match="floating"):
        VersionedMatchAdapter(
            adapter_id="semantic",
            version="1",
            revision="latest",
            matcher=lambda _term, _text: AdapterResult(AdapterStatus.NO_MATCH),
        )


def test_ontology_and_semantic_matches_require_human_review():
    ontology = VersionedMatchAdapter(
        adapter_id="test-ontology",
        version="1.0.0",
        revision="sha256:ontology-fixture-v1",
        locale="tr-TR",
        domain="foreign-trade",
        matcher=lambda term, _text: AdapterResult(
            AdapterStatus.MATCH if term == "akreditif" else AdapterStatus.NO_MATCH,
            matched_variant="letter of credit",
            confidence=1.0,
            explanation="Pinned ontology concept candidate.",
        ),
    )
    result = match_term("akreditif", "Managed letters of credit.", ontology_adapter=ontology)
    assert result.stage is MatchStage.ONTOLOGY
    assert result.review_required is True
    assert result.adapter_revision == "sha256:ontology-fixture-v1"

    semantic = VersionedMatchAdapter(
        adapter_id="semantic-model",
        version="2.1.0",
        revision="model-sha256:abc123",
        locale="en-US",
        domain="general",
        matcher=lambda _term, _text: AdapterResult(
            AdapterStatus.MATCH,
            matched_variant=None,
            confidence=0.82,
            explanation="Revision-pinned semantic candidate.",
        ),
    )
    semantic_result = match_term(
        "supplier negotiation",
        "Worked with vendors on commercial terms.",
        semantic_adapter=semantic,
        allow_fuzzy=False,
    )
    assert semantic_result.stage is MatchStage.SEMANTIC
    assert semantic_result.confidence == 0.82
    assert semantic_result.review_required is True


def test_adapter_error_abstains_to_human_review():
    def broken(_term: str, _text: str) -> AdapterResult:
        raise RuntimeError("model unavailable")

    adapter = VersionedMatchAdapter(
        adapter_id="semantic-model",
        version="2.1.0",
        revision="model-sha256:def456",
        matcher=broken,
    )
    result = match_term("SAP", "ERP experience", semantic_adapter=adapter)
    assert result.matched is False
    assert result.stage is MatchStage.HUMAN_REVIEW
    assert result.review_required is True
    assert "RuntimeError" in result.explanation


def test_exact_match_still_precedes_optional_adapters():
    called = False

    def adapter(_term: str, _text: str) -> AdapterResult:
        nonlocal called
        called = True
        return AdapterResult(AdapterStatus.MATCH)

    semantic = VersionedMatchAdapter(
        adapter_id="semantic-model",
        version="1.0.0",
        revision="model-sha256:exact-not-called",
        matcher=adapter,
    )
    result = match_term("SAP", "SAP MM kullanıldı", semantic_adapter=semantic)
    assert result.stage is MatchStage.EXACT
    assert called is False


# STAB-015: technical-connector boundary regressions. Plain ``\w`` boundaries let
# "c" register an EXACT hit inside "C++" because "+" is not a word character, so
# `(?!\w)` was satisfied right after the "c". These pin the canonical C/C++ gold
# case plus adjacent connector-token cases (C#) and confirm standalone "C" is
# unaffected.
def test_short_term_does_not_exact_match_inside_longer_connector_token():
    result = match_term("c", "Experienced in C++ development and embedded systems.", allow_fuzzy=False)
    assert result.matched is False, '"c" must not register an EXACT hit inside "C++"'
    assert result.stage is MatchStage.NONE


def test_short_term_does_not_exact_match_inside_hash_connector_token():
    result = match_term("c", "Backend built with C# and .NET.", allow_fuzzy=False)
    assert result.matched is False, '"c" must not register an EXACT hit inside "C#"'


def test_connector_term_still_matches_as_its_own_token():
    plus_plus = match_term("c++", "Experienced in C++ development.", allow_fuzzy=False)
    assert plus_plus.matched is True
    assert plus_plus.stage is MatchStage.EXACT

    sharp = match_term("c#", "Backend built with C# and .NET.", allow_fuzzy=False)
    assert sharp.matched is True
    assert sharp.stage is MatchStage.EXACT


def test_standalone_short_term_still_matches_when_not_part_of_a_connector_token():
    result = match_term("c", "Also comfortable writing plain C when needed.", allow_fuzzy=False)
    assert result.matched is True
    assert result.stage is MatchStage.EXACT
    assert result.count == 1
