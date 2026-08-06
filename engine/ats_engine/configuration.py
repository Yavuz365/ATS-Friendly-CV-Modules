"""Versioned policy and evaluation-profile registry.

The engine has no universal ATS, interview, or hiring threshold.  Numeric
decision thresholds may only enter through an explicit, source-bound profile.
Operational integrity gates (for example a parse-safety minimum) are versioned
separately from empirical evaluation profiles.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .errors import InvalidInputError


def _unit_interval(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidInputError(f"{name} sayısal olmalıdır.", field=name)
    number = float(value)
    if not math.isfinite(number) or not 0.0 <= number <= 1.0:
        raise InvalidInputError(f"{name} [0,1] aralığında sonlu olmalıdır.", field=name)
    return number


@dataclass(frozen=True)
class GatePolicy:
    """Versioned operational policy; not an ATS/outcome calibration."""

    id: str
    version: str
    parse_pass_min: float
    source: str
    effective_date: str

    def __post_init__(self) -> None:
        if not self.id or not self.version or not self.source or not self.effective_date:
            raise InvalidInputError("Gate policy kimliği, sürümü, kaynağı ve tarihi zorunludur.")
        _unit_interval("parse_pass_min", self.parse_pass_min)


@dataclass(frozen=True)
class EvaluationProfile:
    """Source-bound diagnostic comparator profile.

    ``diagnostic_stop_min`` may be used only to stop a revision experiment.  It
    never means commercial ATS pass, interview readiness, or hiring likelihood.
    """

    id: str
    version: str
    source: str
    effective_date: str
    locale: str
    domain: str
    comparator_version: str
    diagnostic_stop_min: float | None = None

    def __post_init__(self) -> None:
        required = {
            "id": self.id,
            "version": self.version,
            "source": self.source,
            "effective_date": self.effective_date,
            "locale": self.locale,
            "domain": self.domain,
            "comparator_version": self.comparator_version,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise InvalidInputError(
                "Evaluation profile metadata eksik: " + ", ".join(missing),
                field="evaluation_profile",
            )
        if self.diagnostic_stop_min is not None:
            _unit_interval("diagnostic_stop_min", self.diagnostic_stop_min / 100.0)


DEFAULT_GATE_POLICY = GatePolicy(
    id="evidence-first-gates",
    version="1.0.0",
    parse_pass_min=0.70,
    source="ADR-001 G0 input/integrity policy",
    effective_date="2026-08-05",
)
