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
            "has_sidebar": False,
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
    assert all(verdict.passed for verdict in report.field_verdicts)


def test_missing_required_text_fails_full_text_field() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["Foreign Trade Specialist", "MISSING-FRAGMENT"],
        structural_features={"table_count": 1},
    )
    assert report.all_required_passed is False
    full_text = next(verdict for verdict in report.field_verdicts if verdict.field_name == "full_text")
    assert full_text.passed is False


def test_structural_feature_below_threshold_fails() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["Incoterms 2020"],
        structural_features={"table_count": 5},
    )
    table = next(verdict for verdict in report.field_verdicts if verdict.field_name == "table_count")
    assert report.all_required_passed is False
    assert table.passed is False


def test_missing_structural_key_is_explicit_failure() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        structural_features={"missing_feature": 1},
    )
    verdict = next(item for item in report.field_verdicts if item.field_name == "missing_feature")
    assert verdict.passed is False
    assert verdict.observed == {"state": "MISSING"}


def test_zero_and_false_are_not_treated_as_missing() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        structural_features={"has_sidebar": False, "table_count": 0},
    )
    verdicts = {item.field_name: item for item in report.field_verdicts}
    assert verdicts["has_sidebar"].passed is True
    assert verdicts["table_count"].passed is True


def test_field_order_is_stable() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        structural_features={"text_box_count": 1, "header_part_count": 1, "table_count": 1},
    )
    assert [item.field_name for item in report.field_verdicts] == [
        "document_status",
        "full_text",
        "header_part_count",
        "table_count",
        "text_box_count",
    ]


def test_summary_is_json_serializable_shape() -> None:
    report = evaluate_fields(
        "DOCX-COMPLEX-001",
        _sample_docx_result(),
        expected_status="PASS",
        required_text=["MISSING-FRAGMENT"],
        structural_features={"table_count": 1},
    )
    summary = report.summary()
    assert summary == {
        "fixture_id": "DOCX-COMPLEX-001",
        "document_status": "PASS",
        "total_fields": 3,
        "passed_fields": 2,
        "failed_fields": 1,
        "all_required_passed": False,
        "failed_field_names": ["full_text"],
    }


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
    assert [item.field_name for item in report.field_verdicts] == ["document_status", "error_code"]


def test_error_code_mismatch_fails() -> None:
    report = evaluate_fields(
        "PDF-SCAN-001",
        None,
        expected_status="ERROR",
        expected_error_code="SCANNED_PDF_REQUIRES_OCR",
        parse_error_code="SOMETHING_ELSE",
    )
    assert report.all_required_passed is False
