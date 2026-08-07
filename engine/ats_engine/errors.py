"""Typed public errors for the ATS engine boundary.

C-007: publishing a stable set of error *codes* is not, by itself, a stable
error taxonomy. A caller (CLI, future API) also needs to know, per code,
whether the failure is the caller's fault or the engine's fault, whether
retrying is meaningful, and what process/HTTP status it maps to — without
grepping message text. ``ERROR_TAXONOMY`` is the single source of truth for
that mapping; ``cli.py`` and any future API adapter read exit/HTTP codes from
here instead of hard-coding literals per call site.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ErrorCode(str, Enum):
    """Stable machine-readable error codes used by API and CLI adapters."""

    INVALID_INPUT = "INVALID_INPUT"
    RESOURCE_MISSING = "RESOURCE_MISSING"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    EMPTY_DOCUMENT = "EMPTY_DOCUMENT"
    SCANNED_PDF_REQUIRES_OCR = "SCANNED_PDF_REQUIRES_OCR"
    PARSE_ERROR = "PARSE_ERROR"
    QA_ERROR = "QA_ERROR"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorSeverity(str, Enum):
    """Who is responsible for resolving the error, at a glance."""

    USER_ERROR = "USER_ERROR"  # caller can fix the input/environment and retry
    REVIEW_REQUIRED = "REVIEW_REQUIRED"  # not a failure; a human decision is required
    INTERNAL_ERROR = "INTERNAL_ERROR"  # engine/programming fault, not the caller's input


@dataclass(frozen=True)
class ErrorTaxonomyEntry:
    """One row of the canonical error taxonomy for a given :class:`ErrorCode`."""

    code: ErrorCode
    severity: ErrorSeverity
    retryable: bool
    cli_exit_code: int
    http_status: int
    description: str


# CLI exit-code contract (STAB-008, kept identical here so both stay in sync):
#   0 -> success · 2 -> user/input error · 3 -> unexpected internal error · 4 -> review/blocking
ERROR_TAXONOMY: dict[ErrorCode, ErrorTaxonomyEntry] = {
    ErrorCode.INVALID_INPUT: ErrorTaxonomyEntry(
        code=ErrorCode.INVALID_INPUT,
        severity=ErrorSeverity.USER_ERROR,
        retryable=True,
        cli_exit_code=2,
        http_status=400,
        description="Malformed, out-of-range, or otherwise invalid caller-supplied input.",
    ),
    ErrorCode.RESOURCE_MISSING: ErrorTaxonomyEntry(
        code=ErrorCode.RESOURCE_MISSING,
        severity=ErrorSeverity.USER_ERROR,
        retryable=True,
        cli_exit_code=2,
        http_status=404,
        description="A referenced file, path, or resource could not be found or read.",
    ),
    ErrorCode.UNSUPPORTED_FORMAT: ErrorTaxonomyEntry(
        code=ErrorCode.UNSUPPORTED_FORMAT,
        severity=ErrorSeverity.USER_ERROR,
        retryable=False,
        cli_exit_code=2,
        http_status=415,
        description="Document media type/extension is not one of the supported formats.",
    ),
    ErrorCode.EMPTY_DOCUMENT: ErrorTaxonomyEntry(
        code=ErrorCode.EMPTY_DOCUMENT,
        severity=ErrorSeverity.USER_ERROR,
        retryable=True,
        cli_exit_code=2,
        http_status=422,
        description="Document parsed but contained no extractable content.",
    ),
    ErrorCode.SCANNED_PDF_REQUIRES_OCR: ErrorTaxonomyEntry(
        code=ErrorCode.SCANNED_PDF_REQUIRES_OCR,
        severity=ErrorSeverity.REVIEW_REQUIRED,
        retryable=True,
        cli_exit_code=4,
        http_status=422,
        description="Scanned/image-only PDF; retry with the optional OCR adapter enabled.",
    ),
    ErrorCode.PARSE_ERROR: ErrorTaxonomyEntry(
        code=ErrorCode.PARSE_ERROR,
        severity=ErrorSeverity.USER_ERROR,
        retryable=False,
        cli_exit_code=2,
        http_status=422,
        description="Document content could not be structurally parsed (corrupt/malformed file).",
    ),
    ErrorCode.QA_ERROR: ErrorTaxonomyEntry(
        code=ErrorCode.QA_ERROR,
        severity=ErrorSeverity.REVIEW_REQUIRED,
        retryable=False,
        cli_exit_code=4,
        http_status=422,
        description="A blocking QA rule failed; output requires human review before use.",
    ),
    ErrorCode.HUMAN_APPROVAL_REQUIRED: ErrorTaxonomyEntry(
        code=ErrorCode.HUMAN_APPROVAL_REQUIRED,
        severity=ErrorSeverity.REVIEW_REQUIRED,
        retryable=True,
        cli_exit_code=4,
        http_status=409,
        description="Action needs an explicit human approval/rollback decision before proceeding.",
    ),
    ErrorCode.INTERNAL_ERROR: ErrorTaxonomyEntry(
        code=ErrorCode.INTERNAL_ERROR,
        severity=ErrorSeverity.INTERNAL_ERROR,
        retryable=False,
        cli_exit_code=3,
        http_status=500,
        description="Unexpected engine/programming fault; not caused by caller input.",
    ),
}


def taxonomy_for(code: ErrorCode) -> ErrorTaxonomyEntry:
    """Return the canonical taxonomy row for ``code``.

    Falls back to the ``INTERNAL_ERROR`` row (never silently to a made-up
    "safe" default) if a code somehow isn't registered, so an unmapped code
    is loud rather than mis-classified as retryable/user-facing.
    """
    return ERROR_TAXONOMY.get(code, ERROR_TAXONOMY[ErrorCode.INTERNAL_ERROR])


class ATSEngineError(Exception):
    """Base error with a stable code, taxonomy mapping, and optional field pointer."""

    def __init__(self, message: str, *, code: ErrorCode, field: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.field = field

    @property
    def taxonomy(self) -> ErrorTaxonomyEntry:
        return taxonomy_for(self.code)

    @property
    def cli_exit_code(self) -> int:
        return self.taxonomy.cli_exit_code

    @property
    def http_status(self) -> int:
        return self.taxonomy.http_status

    @property
    def retryable(self) -> bool:
        return self.taxonomy.retryable

    def to_dict(self) -> dict[str, str | int | bool]:
        entry = self.taxonomy
        out: dict[str, str | int | bool] = {
            "code": self.code.value,
            "message": str(self),
            "severity": entry.severity.value,
            "retryable": entry.retryable,
            "cli_exit_code": entry.cli_exit_code,
            "http_status": entry.http_status,
        }
        if self.field:
            out["field"] = self.field
        return out


class InvalidInputError(ATSEngineError):
    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message, code=ErrorCode.INVALID_INPUT, field=field)


class ResourceMissingError(ATSEngineError):
    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message, code=ErrorCode.RESOURCE_MISSING, field=field)


class DocumentParseError(ATSEngineError):
    def __init__(self, message: str, *, code: ErrorCode = ErrorCode.PARSE_ERROR) -> None:
        super().__init__(message, code=code)


class InternalEngineError(ATSEngineError):
    """Wraps an unexpected engine-side fault with the stable INTERNAL_ERROR code."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code=ErrorCode.INTERNAL_ERROR)
