"""Typed public errors for the ATS engine boundary."""

from __future__ import annotations

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


class ATSEngineError(Exception):
    """Base error with a stable code and optional field pointer."""

    def __init__(self, message: str, *, code: ErrorCode, field: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.field = field

    def to_dict(self) -> dict[str, str]:
        out = {"code": self.code.value, "message": str(self)}
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
