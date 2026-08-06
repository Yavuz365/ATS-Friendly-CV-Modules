"""ING-005 — Field-level evaluation helper unit tests."""

from __future__ import annotations

from ats_engine.contracts import DocumentParseResult, ProcessStatus
from ats_engine.field_evaluation import evaluate_fields


def _sample_docx_result() -> DocumentParseResult:
    return DocumentParseResult(
        artifact_id="artifact-test",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        text="Foreign Trade Specialist\nIncoterms 2020\nLetter of Credit\nCandidate Header",
        status=ProcessStatus.PASS,
        extraction_method="docx-ooxml-full-story",
        structural_features={
            "table_count": 1,
            "text_box_count": 1,
            "header_part_count": 1,
            "paragraph_count": 4,
        },
    )


def test_all_required_fields_pass() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["Foreign Trade Specialist", "Incoterms 2020", "Letter of Credit"],
        structural_features={"table_count": 1, "text_box_count": 1, "header_part_count": 1},
    )
    assert report.all_required_passed is True
    assert all(v.passed for v in report.field_verdicts)


def test_missing_required_text_fails_full_text_field() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["Foreign Trade Specialist", "MISSING-FRAGMENT"],
        structural_features={"table_count": 1},
    )
    assert report.all_required_passed is False
    full_text = next(v for v in report.field_verdicts if v.field_name == "full_text")
    assert full_text.passed is False


def test_structural_feature_below_threshold_fails() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["Incoterms 2020"],
        structural_features={"table_count": 5},  # observed is 1
    )
    assert report.all_required_passed is False
    table = next(v for v in report.field_verdicts if v.field_name == "table_count")
    assert table.passed is False


def test_expected_error_path_without_parse_result() -> None:
    report = evaluate_fields(
        "PDF-SCAN-001",
        None,
        expected_status="ERROR",
        expected_error_code="SCANNED_PDF_REQUIRES_OCR",
        parse_error_code="SCANNED_PDF_REQUIRES_OCR",
    )
    assert report.all_required_passed is True
    assert report.document_status is ProcessStatus.ERROR


def test_error_code_mismatch_fails() -> None:
    report = evaluate_fields(
        "PDF-SCAN-001",
        None,
        expected_status="ERROR",
        expected_error_code="SCANNED_PDF_REQUIRES_OCR",
        parse_error_code="SOMETHING_ELSE",
    )
    assert report.all_required_passed is False
