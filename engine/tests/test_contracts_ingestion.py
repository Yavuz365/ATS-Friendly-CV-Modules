from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, validate

from ats_engine import (
    ProcessStatus,
    approve_change_set,
    build_change_set,
    build_report,
    parse_document,
)
from ats_engine.errors import DocumentParseError, ErrorCode, InvalidInputError


def _docx(path: Path) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="xml" ContentType="application/xml"/>
      <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
      <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    </Types>"""
    document = """<?xml version="1.0" encoding="UTF-8"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body><w:p><w:r><w:t>Summary</w:t></w:r></w:p>
      <w:tbl><w:tr><w:tc><w:p><w:r><w:t>Table evidence</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
      <w:p><w:r><w:t>Text box content</w:t></w:r></w:p></w:body>
    </w:document>"""
    header = """<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:p><w:r><w:t>Header Name</w:t></w:r></w:p></w:hdr>"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", document)
        archive.writestr("word/header1.xml", header)


def test_docx_binary_ingestion_traverses_document_table_and_header(tmp_path):
    path = tmp_path / "cv.docx"
    _docx(path)
    result = parse_document(path)
    assert result.status is ProcessStatus.PASS
    assert "Summary" in result.text
    assert "Table evidence" in result.text
    assert "Header Name" in result.text
    assert result.extraction_method == "docx-ooxml-full-story"


def test_blank_pdf_requires_ocr_explicitly(tmp_path):
    from pypdf import PdfWriter

    path = tmp_path / "scan.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with path.open("wb") as handle:
        writer.write(handle)
    with pytest.raises(DocumentParseError) as caught:
        parse_document(path)
    assert caught.value.code is ErrorCode.SCANNED_PDF_REQUIRES_OCR


def test_lexical_provenance_never_becomes_verified_pass():
    from ats_engine.evidence_bank import parse_bank, provenance_check

    bank = parse_bank('EXP-01 | ERP | beceriler: [SAP] | kanıt: "SAP kullandım"')
    result = provenance_check(["SAP kullandım"], bank)
    assert result["pass"] is False
    assert result["table"][0]["support_type"] == "LEXICAL_SUPPORT"
    assert result["table"][0]["verification_status"] == "UNVERIFIED"


def test_safe_synthesis_requires_known_evidence_and_human_approval():
    changes = build_change_set(
        "changes-1",
        [{"path": "cv.summary", "old_value": "old", "new_value": "new", "evidence_ids": ["EV-1"]}],
        known_evidence_ids={"EV-1"},
    )
    assert changes.status is ProcessStatus.REVIEW
    assert not changes.human_approved
    approved = approve_change_set(changes)
    assert approved.status is ProcessStatus.PASS
    assert approved.human_approved


def test_safe_synthesis_rejects_protected_fact_mutation():
    with pytest.raises(InvalidInputError, match="Korunan"):
        build_change_set(
            "changes-2",
            [{"path": "candidate.metric", "new_value": "99%", "evidence_ids": ["EV-1"]}],
            known_evidence_ids={"EV-1"},
        )


def test_decision_report_schema_and_not_evaluated_state():
    report = build_report("Lojistik uzmanı aranıyor", "", use_sbert=False)
    assert report["match_score"]["score_percent"] is None
    assert report["decision_report"]["evaluation_status"] == "NOT_EVALUATED"
    assert report["decision_report"]["overall_status"] == "REVIEW"

    schema_path = Path(__file__).parents[2] / "schemas" / "v2" / "contracts.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validate(
        report["decision_report"],
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "#/$defs/decisionReport",
            "$defs": schema["$defs"],
        },
    )


def test_all_public_v2_schemas_are_draft_2020_12_and_closed():
    schema_dir = Path(__file__).parents[2] / "schemas" / "v2"
    public = [path for path in schema_dir.glob("*.schema.json") if path.name != "contracts.schema.json"]
    assert len(public) == 12
    for path in public:
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        Draft202012Validator.check_schema(schema)


def test_all_contract_golden_examples_validate():
    schema_dir = Path(__file__).parents[2] / "schemas" / "v2"
    schema = json.loads((schema_dir / "contracts.schema.json").read_text(encoding="utf-8"))
    examples = json.loads((schema_dir / "examples" / "contract-examples.json").read_text(encoding="utf-8"))
    assert set(examples) == {
        "sourceArtifact",
        "candidateFact",
        "evidence",
        "jobPostingSnapshot",
        "jobRequirement",
        "requirementEvidenceMap",
        "documentParseResult",
        "gateResult",
        "diagnosticResult",
        "synthesisChangeSet",
        "decisionReport",
        "applicationEvent",
    }
    for name, instance in examples.items():
        validate(
            instance,
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$ref": f"#/$defs/{name}",
                "$defs": schema["$defs"],
            },
        )
