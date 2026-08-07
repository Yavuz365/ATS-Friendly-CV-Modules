"""Versioned policy and evaluation-profile registry.

The engine has no universal ATS, interview, or hiring threshold.  Numeric
decision thresholds may only enter through an explicit, source-bound profile.
Operational integrity gates (for example a parse-safety minimum) are versioned
separately from empirical evaluation profiles.

C-009: a versioned threshold/config value is not "governed" just because it
has a version string and a source citation. Canonical acceptance also
requires, for every configured numeric value: who owns the decision to
change it (``owner``), why this specific number was chosen (``rationale``),
and when it is next due for review (``review_date``) — otherwise a stale or
arbitrary threshold can live forever with nobody accountable for revisiting
it. ``GatePolicy``/``EvaluationProfile`` enforce all three as required
fields, and ``DEFAULT_LEGACY_SCORING_POLICY`` extends that same governance to
the legacy hybrid-score weights/thresholds in ``scoring.py``, which
previously lived as a bare, unowned module-level dict.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .errors import InvalidInputError


def _unit_interval(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} sayısal olmalıdır.", field=name)
    number = float(value)
    if not math.isfinite(number) or not 0.0 <= number <= 1.0:
        raise InvalidInputError(f"{name} [0,1] aralığında sonlu olmalıdır.", field=name)
    return number


def _require_governance_fields(values: dict[str, str]) -> None:
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise InvalidInputError(
            "Politika/profil governance alanları eksik: " + ", ".join(missing),
            field="governance",
        )


@dataclass(frozen=True)
class GatePolicy:
    """Versioned operational policy; not an ATS/outcome calibration.

    ``owner``, ``rationale`` and ``review_date`` are mandatory governance
    fields (C-009): every configured gate value must have someone accountable
    for it, a documented reason it is set where it is, and a date by which it
    must be revisited — a version number and a citation alone are not enough.
    """

    id: str
    version: str
    parse_pass_min: float
    source: str
    effective_date: str
    owner: str
    rationale: str
    review_date: str
    locale: str = "und"
    domain: str = "general"

    def __post_init__(self) -> None:
        _require_governance_fields(
            {
                "id": self.id,
                "version": self.version,
                "source": self.source,
                "effective_date": self.effective_date,
                "owner": self.owner,
                "rationale": self.rationale,
                "review_date": self.review_date,
                "locale": self.locale,
                "domain": self.domain,
            }
        )
        _unit_interval("parse_pass_min", self.parse_pass_min)


@dataclass(frozen=True)
class EvaluationProfile:
    """Source-bound diagnostic comparator profile.

    ``diagnostic_stop_min`` may be used only to stop a revision experiment.  It
    never means commercial ATS pass, interview readiness, or hiring likelihood.
    ``owner``/``rationale``/``review_date`` are mandatory governance fields,
    matching :class:`GatePolicy` (C-009).
    """

    id: str
    version: str
    source: str
    effective_date: str
    locale: str
    domain: str
    comparator_version: str
    owner: str
    rationale: str
    review_date: str
    diagnostic_stop_min: float | None = None

    def __post_init__(self) -> None:
        _require_governance_fields(
            {
                "id": self.id,
                "version": self.version,
                "source": self.source,
                "effective_date": self.effective_date,
                "locale": self.locale,
                "domain": self.domain,
                "comparator_version": self.comparator_version,
                "owner": self.owner,
                "rationale": self.rationale,
                "review_date": self.review_date,
            }
        )
        if self.diagnostic_stop_min is not None:
            _unit_interval("diagnostic_stop_min", self.diagnostic_stop_min / 100.0)


@dataclass(frozen=True)
class LegacyScoringWeightsPolicy:
    """Governance wrapper around the legacy hybrid-score weights/thresholds.

    C-009 (remaining condition): "legacy scoring weights/threshold metadata
    also remains outside that complete registry" — ``scoring.DEFAULTS`` and
    ``scoring.THRESHOLDS`` were a bare module-level dict with no owner,
    rationale, version, or review date. This dataclass is that missing
    registry entry; ``scoring.py`` keeps the plain dicts for backward
    compatibility (existing call sites pass ``**DEFAULTS`` positionally) but
    this is now the governed, citable source of truth for what those numbers
    are and why they exist.
    """

    id: str
    version: str
    source: str
    effective_date: str
    owner: str
    rationale: str
    review_date: str
    weights: dict[str, float] = field(default_factory=dict)
    thresholds: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_governance_fields(
            {
                "id": self.id,
                "version": self.version,
                "source": self.source,
                "effective_date": self.effective_date,
                "owner": self.owner,
                "rationale": self.rationale,
                "review_date": self.review_date,
            }
        )
        if not self.weights:
            raise InvalidInputError("weights boş olamaz.", field="weights")


DEFAULT_GATE_POLICY = GatePolicy(
    id="evidence-first-gates",
    version="1.0.0",
    parse_pass_min=0.70,
    source="ADR-001 G0 input/integrity policy",
    effective_date="2026-08-05",
    owner="ats-engine-maintainers",
    rationale=(
        "0.70 is a conservative structural-parse-integrity floor (not an ATS/outcome "
        "threshold): below it, cv_parser.parse_safety_score() has already flagged enough "
        "missing/garbled structure that downstream matching evidence is unreliable, so G0 "
        "should block rather than silently score a document ats-engine cannot faithfully read."
    ),
    review_date="2027-02-05",
)

# C-009: the legacy alpha/beta/gamma/zeta/k1/b weights and the retained-for-compatibility
# score bands both previously lived as bare dicts in scoring.py with no owner, rationale,
# or review date. This is their governed registry entry; scoring.DEFAULTS/THRESHOLDS remain
# the values actually consumed by ats_match_score() (single source of numeric truth), this
# just makes them citable and accountable.
DEFAULT_LEGACY_SCORING_POLICY = LegacyScoringWeightsPolicy(
    id="legacy-hybrid-score-weights",
    version="1.0.0",
    source="ATS-Friendly-CV-Modules v1.5.x legacy diagnostic (legacy_adapter.legacy_diagnostic)",
    effective_date="2026-08-02",
    owner="ats-engine-maintainers",
    rationale=(
        "alpha/beta/gamma/zeta are an unvalidated, hand-tuned split favouring lexical (0.35), "
        "semantic (0.30) and coverage (0.35) signals equally, with a moderate keyword-stuffing "
        "penalty (0.20); k1/b are the standard Okapi BM25 defaults from Robertson/Zaragoza. None "
        "of these have been calibrated against a labelled outcome dataset (CCR-006/CCR-026) — the "
        "legacy score they produce is explicitly NOT_RUN for calibration purposes and must not be "
        "presented as a validated ATS/hiring probability."
    ),
    review_date="2027-02-05",
    weights={"alpha": 0.35, "beta": 0.30, "gamma": 0.35, "zeta": 0.20, "k1": 1.5, "b": 0.75},
    thresholds={"target_low": 75, "target_high": 85, "overopt": 90, "serious": 50},
)
