"""Field-level evaluation against gold corpus expectations (ING-005).

This module is evaluation-only. It never mutates parse results and never
changes ingestion behaviour. It answers: for a given DocumentParseResult and
a gold fixture definition, which required fields passed?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .contracts import DocumentParseResult, ProcessStatus


@dataclass(frozen=True)
class FieldVerdict:
    field_name: str
    passed: bool
    expected: Any
    observed: Any
    detail: str = ""


@dataclass(frozen=True)
class FieldEvaluationReport:
    fixture_id: str
    document_status: ProcessStatus
    field_verdicts: list[FieldVerdict]
    all_required_passed: bool
    notes: list[str] = field(default_factory=list)


def _has_required_text(text: str, required: list[str]) -> tuple[bool, list[str]]:
    missing = [fragment for fragment in required if fragment and fragment not in text]
    return (len(missing) == 0, missing)


def evaluate_fields(
    fixture_id: str,
    parse_result: DocumentParseResult | None,
    *,
    expected_status: str,
    required_text: list[str] | None = None,
    structural_features: dict[str, Any] | None = None,
    expected_error_code: str | None = None,
    parse_error_code: str | None = None,
) -> FieldEvaluationReport:
    """Score a parse outcome against gold field expectations.

    Parameters mirror the gold manifest / labels structure so evaluation cards
    can call this without inventing a parallel schema.
    """
    required_text = required_text or []
    structural_features = structural_features or {}
    verdicts: list[FieldVerdict] = []
    notes: list[str] = []

    # --- document-level status ---
    if parse_result is None:
        # Expected error path (e.g. scanned PDF without OCR)
        status_ok = expected_status == "ERROR"
        verdicts.append(
            FieldVerdict(
                "document_status",
                status_ok,
                expected_status,
                f"ERROR:{parse_error_code or 'unknown'}",
                "Parse raised; treated as ERROR path.",
            )
        )
        if expected_error_code:
            code_ok = (parse_error_code or "") == expected_error_code
            verdicts.append(
                FieldVerdict(
                    "error_code",
                    code_ok,
                    expected_error_code,
                    parse_error_code,
                    "Expected error code match." if code_ok else "Error code mismatch.",
                )
            )
        all_passed = all(v.passed for v in verdicts)
        return FieldEvaluationReport(
            fixture_id=fixture_id,
            document_status=ProcessStatus.ERROR,
            field_verdicts=verdicts,
            all_required_passed=all_passed,
            notes=notes,
        )

    observed_status = parse_result.status.value if hasattr(parse_result.status, "value") else str(parse_result.status)
    status_ok = observed_status == expected_status
    verdicts.append(
        FieldVerdict(
            "document_status",
            status_ok,
            expected_status,
            observed_status,
            "Document-level status match." if status_ok else "Document-level status mismatch.",
        )
    )

    # --- full_text / required fragments ---
    text_ok, missing = _has_required_text(parse_result.text or "", required_text)
    verdicts.append(
        FieldVerdict(
            "full_text",
            text_ok,
            required_text,
            {"missing": missing, "text_length": len(parse_result.text or "")},
            "All required fragments present." if text_ok else f"Missing fragments: {missing}",
        )
    )

    # --- structural features ---
    observed_struct = parse_result.structural_features or {}
    for key, expected_value in structural_features.items():
        observed_value = observed_struct.get(key)
        if isinstance(expected_value, (int, float)) and isinstance(observed_value, (int, float)):
            passed = observed_value >= expected_value
            detail = f"observed={observed_value} >= expected={expected_value}" if passed else (
                f"observed={observed_value} < expected={expected_value}"
            )
        else:
            passed = observed_value == expected_value
            detail = "exact match" if passed else f"observed={observed_value!r} expected={expected_value!r}"
        verdicts.append(
            FieldVerdict(
                field_name=key,
                passed=passed,
                expected=expected_value,
                observed=observed_value,
                detail=detail,
            )
        )

    # --- page evidence for PDFs ---
    if parse_result.page_evidence:  # only when explicitly populated (non-empty)
        verdicts.append(
            FieldVerdict(
                "page_evidence",
                True,
                ">=1 page",
                len(parse_result.page_evidence),
                "Page evidence present.",
            )
        )

    all_passed = all(v.passed for v in verdicts)
    if not all_passed:
        notes.append("One or more required fields failed; document-level PASS is not sufficient.")

    return FieldEvaluationReport(
        fixture_id=fixture_id,
        document_status=parse_result.status,
        field_verdicts=verdicts,
        all_required_passed=all_passed,
        notes=notes,
    )
