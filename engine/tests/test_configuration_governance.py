"""C-009: GatePolicy/EvaluationProfile/legacy-scoring governance metadata.

A versioned threshold is not accountable just because it has a version
string and a source citation — canonical acceptance also requires an owner,
a rationale, and a review date for every configured numeric value. These
tests pin that all three registries enforce and expose that metadata, and
that the previously-unowned legacy scoring weights/thresholds are now a real
governed registry entry.
"""

from __future__ import annotations

import pytest

from ats_engine.configuration import (
    DEFAULT_GATE_POLICY,
    DEFAULT_LEGACY_SCORING_POLICY,
    EvaluationProfile,
    GatePolicy,
    LegacyScoringWeightsPolicy,
)
from ats_engine.errors import InvalidInputError
from ats_engine.scoring import DEFAULTS, THRESHOLDS


def test_default_gate_policy_has_full_governance_metadata():
    assert DEFAULT_GATE_POLICY.owner
    assert DEFAULT_GATE_POLICY.rationale
    assert DEFAULT_GATE_POLICY.review_date
    assert DEFAULT_GATE_POLICY.locale
    assert DEFAULT_GATE_POLICY.domain


@pytest.mark.parametrize("missing_field", ["owner", "rationale", "review_date"])
def test_gate_policy_rejects_missing_governance_field(missing_field):
    kwargs = dict(
        id="x",
        version="1.0.0",
        parse_pass_min=0.5,
        source="s",
        effective_date="2026-01-01",
        owner="o",
        rationale="r",
        review_date="2027-01-01",
    )
    kwargs[missing_field] = ""
    with pytest.raises(InvalidInputError):
        GatePolicy(**kwargs)


@pytest.mark.parametrize("missing_field", ["owner", "rationale", "review_date"])
def test_evaluation_profile_rejects_missing_governance_field(missing_field):
    kwargs = dict(
        id="x",
        version="1.0.0",
        source="s",
        effective_date="2026-01-01",
        locale="tr",
        domain="general",
        comparator_version="v1",
        owner="o",
        rationale="r",
        review_date="2027-01-01",
    )
    kwargs[missing_field] = ""
    with pytest.raises(InvalidInputError):
        EvaluationProfile(**kwargs)


def test_legacy_scoring_policy_mirrors_actual_scoring_defaults():
    # The registry entry must describe the real numbers scoring.py uses, not
    # a stale/aspirational copy — otherwise it is a second source of truth.
    assert DEFAULT_LEGACY_SCORING_POLICY.weights == DEFAULTS
    assert DEFAULT_LEGACY_SCORING_POLICY.thresholds == THRESHOLDS
    assert DEFAULT_LEGACY_SCORING_POLICY.owner
    assert DEFAULT_LEGACY_SCORING_POLICY.rationale
    assert DEFAULT_LEGACY_SCORING_POLICY.review_date


def test_legacy_scoring_policy_requires_nonempty_weights():
    with pytest.raises(InvalidInputError):
        LegacyScoringWeightsPolicy(
            id="x",
            version="1.0.0",
            source="s",
            effective_date="2026-01-01",
            owner="o",
            rationale="r",
            review_date="2027-01-01",
            weights={},
        )
