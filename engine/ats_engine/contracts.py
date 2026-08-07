"""Versioned evidence-first data contracts.

The dataclasses are the Python boundary; JSON Schema files under ``schemas/v2``
are the language-neutral boundary. Unknown, missing and failed states remain
distinct and may never be promoted to PASS by a numeric fallback.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, cast

CONTRACT_VERSION = "2.0.0-alpha.2"


class DataStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    NOT_COLLECTED = "NOT_COLLECTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CONFLICTED = "CONFLICTED"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    UNVERIFIED = "UNVERIFIED"
    REJECTED = "REJECTED"


class ProcessStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW = "REVIEW"
    WARN = "WARN"
    ERROR = "ERROR"
    NOT_RUN = "NOT_RUN"


class EvaluationStatus(str, Enum):
    EVALUATED = "EVALUATED"
    NOT_EVALUATED = "NOT_EVALUATED"


class QASeverity(str, Enum):
    BLOCKING = "BLOCKING"
    REVIEW = "REVIEW"
    ADVISORY = "ADVISORY"
    INFO = "INFO"


class ConsentStatus(str, Enum):
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    NOT_COLLECTED = "NOT_COLLECTED"
    REVOKED = "REVOKED"


def to_primitive(value: Any) -> Any:
    """Convert nested dataclasses/enums into a JSON-safe structure."""
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "__dataclass_fields__"):
        return to_primitive(asdict(value))
    if isinstance(value, dict):
        return {key: to_primitive(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_primitive(item) for item in value]
    return value


@dataclass(frozen=True)
class SourceArtifact:
    id: str
    filename: str
    media_type: str
    sha256: str
    locator: str
    version: str = ""
    status: DataStatus = DataStatus.KNOWN
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class CandidateFact:
    id: str
    field: str
    value: str | None
    source_artifact_ids: list[str]
    data_status: DataStatus
    verification_status: VerificationStatus
    sensitivity: str = "PERSONAL"
    consent_status: ConsentStatus = ConsentStatus.NOT_COLLECTED
    redacted: bool = False
    retention_until: str | None = None
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    candidate_fact_id: str
    source_artifact_id: str
    locator: str
    excerpt: str = ""
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class EvidenceConflict:
    id: str
    candidate_fact_id: str
    evidence_ids: list[str]
    reason: str
    status: ProcessStatus = ProcessStatus.REVIEW
    resolution: str = ""
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class JobPostingSnapshot:
    id: str
    source_artifact_id: str
    captured_at: str
    text_sha256: str
    locale: str = "unknown"
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class JobRequirement:
    id: str
    job_posting_id: str
    text: str
    requirement_type: str
    explicit: bool
    data_status: DataStatus = DataStatus.KNOWN
    category: str = "OTHER"
    modality: str = "UNKNOWN"
    negated: bool = False
    span_start: int | None = None
    span_end: int | None = None
    review_status: ProcessStatus = ProcessStatus.REVIEW
    approval_version: str | None = None
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class RequirementEvidenceMap:
    requirement_id: str
    evidence_ids: list[str]
    verification_status: VerificationStatus
    reason: str
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class DocumentParseResult:
    artifact_id: str
    media_type: str
    text: str
    status: ProcessStatus
    warnings: list[str] = field(default_factory=list)
    page_count: int | None = None
    extraction_method: str = ""
    structural_features: dict[str, Any] = field(default_factory=dict)
    page_evidence: list[dict[str, Any]] = field(default_factory=list)
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    status: ProcessStatus
    reason: str
    action: str = ""
    diagnostics: list[str] = field(default_factory=list)
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class DiagnosticResult:
    diagnostic_id: str
    status: ProcessStatus
    message: str
    value: float | int | str | None = None
    unit: str | None = None
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class QAResult:
    """Typed QA rule outcome.

    QA-001: status/severity/blocking/message alone tell a caller *that*
    something failed but not *what specifically* triggered it (``evidence``)
    or *what to do about it* (``remediation``) without re-parsing the
    free-form ``details`` blob. Both are first-class fields so every rule's
    contract is complete on its own.
    """

    check_id: str
    status: ProcessStatus
    severity: QASeverity
    message: str
    blocking: bool = False
    details: dict[str, Any] = field(default_factory=dict)
    evidence: list[str] = field(default_factory=list)
    remediation: str = ""
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class SynthesisChange:
    """One allowlisted, evidence-bound proposed text mutation.

    SYN-002: ``evidence_ids``/``reason`` establish *why* a change is
    supported, but not *what produced the wording* — model/prompt metadata
    is required on every change so a human reviewer (or later audit) can
    tell a manually authored edit from an LLM-drafted one and which
    model/prompt version to attribute it to. ``model_id="human"`` /
    ``prompt_id="human-authored"`` are the honest values for a manually
    written change, not an invented model name.
    """

    path: str
    old_value: str
    new_value: str
    evidence_ids: list[str]
    reason: str
    model_id: str
    model_version: str
    prompt_id: str
    prompt_version: str


@dataclass(frozen=True)
class SynthesisChangeSet:
    id: str
    changes: list[SynthesisChange]
    status: ProcessStatus
    human_approved: bool = False
    parent_id: str | None = None
    decision_reason: str = ""
    applied_at: str | None = None
    rolled_back_from: str | None = None
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class DecisionReport:
    id: str
    overall_status: ProcessStatus
    evaluation_status: EvaluationStatus
    gates: list[GateResult]
    diagnostics: list[DiagnosticResult]
    errors: list[dict[str, str]] = field(default_factory=list)
    human_approved: bool = False
    contract_version: str = CONTRACT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return cast(dict[str, Any], to_primitive(self))


@dataclass(frozen=True)
class ApplicationEvent:
    id: str
    application_id: str
    event_type: str
    occurred_at: str
    payload: dict[str, Any] = field(default_factory=dict)
    data_status: DataStatus = DataStatus.KNOWN
    outcome_observed: bool | None = None
    censoring_reason: str | None = None
    source_artifact_id: str | None = None
    contract_version: str = CONTRACT_VERSION
