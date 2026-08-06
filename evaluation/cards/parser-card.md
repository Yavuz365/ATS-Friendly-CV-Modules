# Parser Evaluation Card — v0.1.0

**Date:** 2026-08-07  
**Backlog:** EVAL-003 / ING-004 / ING-005  
**Engine:** `ats-engine` 2.0.0a2 (branch work)  
**Dataset:** `evaluation/gold/` binary corpus v1.0.0

## What is measured

| Dimension | Method |
|-----------|--------|
| Document-level status | `PASS` / `REVIEW` / `ERROR` vs gold `expected_status` |
| Extraction method | Must be in gold `expected_extraction_methods` |
| Required text fragments | Substring presence in extracted text |
| Structural features | `table_count`, `text_box_count`, `header_part_count`, … |
| Field-level aggregate | `field_evaluation.evaluate_fields` → `all_required_passed` |
| Scanned PDF path | ERROR + `SCANNED_PDF_REQUIRES_OCR` without OCR adapter |

## Fixtures (n=3)

| ID | Type | Expected |
|----|------|----------|
| `DOCX-COMPLEX-001` | OOXML | PASS + table/header/textbox |
| `PDF-TEXT-001` | text-layer PDF | PASS + page evidence |
| `PDF-SCAN-001` | empty text layer | ERROR / OCR required |

## Current result (automated)

Covered by `engine/tests/test_gold_corpus.py` (document + field-level).

| Fixture | Document | Field-level |
|---------|----------|-------------|
| DOCX-COMPLEX-001 | PASS expected | required fields must all pass |
| PDF-TEXT-001 | PASS expected | required fields must all pass |
| PDF-SCAN-001 | ERROR expected | error_code must match |

**Aggregate commercial metrics:** `NOT_MEASURED`  
**OCR accuracy:** `NOT_MEASURED`  
**Multi-page reading order:** `NOT_MEASURED`  
**Vendor ATS parse parity:** `NOT_MEASURED`

## Limits

- Synthetic binaries only; no personal CV data.
- Single-page PDFs in this corpus version.
- No claim about production parser robustness beyond these fixtures.

## How to re-run

```bash
cd engine && pytest tests/test_gold_corpus.py tests/test_field_evaluation.py -v
```
