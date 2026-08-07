"""Field-level evaluation against gold corpus expectations (ING-005).

This module is evaluation-only. It never mutates parse results or ingestion
behaviour. A document-level PASS is insufficient when required fields fail.
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

    def summary(self) -> dict[str, Any]:
        failed = [verdict.field_name for verdict in self.field_verdicts if not verdict.passed]
        return {
            "fixture_id": self.fixture_id,
            "document_status": self.document_status.value,
            "total_fields": len(self.field_verdicts),
            "passed_fields": sum(verdict.passed for verdict in self.field_verdicts),
            "failed_fields": len(failed),
            "all_required_passed": self.all_required_passed,
            "failed_field_names": failed,
        }


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
    """Score a parse outcome against deterministic gold field expectations."""
    required_text = required_text or []
    structural_features = structural_features or {}
    verdicts: list[FieldVerdict] = []
    notes: list[str] = []

    if parse_result is None:
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
        if expected_error_code is not None:
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
        all_passed = all(verdict.passed for verdict in verdicts)
        return FieldEvaluationReport(
            fixture_id=fixture_id,
            document_status=ProcessStatus.ERROR,
            field_verdicts=verdicts,
            all_required_passed=all_passed,
            notes=notes,
        )

    observed_status = parse_result.status.value
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

    observed_struct = parse_result.structural_features or {}
    for key in sorted(structural_features):
        expected_value = structural_features[key]
        if key not in observed_struct:
            verdicts.append(
                FieldVerdict(
                    field_name=key,
                    passed=False,
                    expected=expected_value,
                    observed={"state": "MISSING"},
                    detail="Required structural field is missing.",
                )
            )
            continue

        observed_value = observed_struct[key]
        if isinstance(expected_value, (int, float)) and isinstance(observed_value, (int, float)):
            passed = observed_value >= expected_value
            detail = (
                f"observed={observed_value} >= expected={expected_value}"
                if passed
                else f"observed={observed_value} < expected={expected_value}"
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

    # ING-005 fix: page_evidence is a PDF-only concept (per-page extraction
    # evidence). `DocumentParseResult.page_evidence` defaults to `[]` — never
    # `None` — for every media type, so a bare `is not None` check made this
    # field mandatory even for DOCX/TXT/MD fixtures that legitimately have no
    # notion of pages. Only require it when the document is actually a PDF.
    if parse_result.media_type == "application/pdf":
        page_count = len(parse_result.page_evidence)
        verdicts.append(
            FieldVerdict(
                "page_evidence",
                page_count > 0,
                ">=1 page",
                page_count,
                "Page evidence present." if page_count > 0 else "No page evidence.",
            )
        )

    all_passed = all(verdict.passed for verdict in verdicts)
    if not all_passed:
        notes.append("One or more required fields failed; document-level PASS is not sufficient.")

    return FieldEvaluationReport(
        fixture_id=fixture_id,
        document_status=parse_result.status,
        field_verdicts=verdicts,
        all_required_passed=all_passed,
        notes=notes,
    )
