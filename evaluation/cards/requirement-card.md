# Requirement Extraction Evaluation Card — v0.1.0

**Date:** 2026-08-07  
**Backlog:** EVAL-003 / JOB-004  
**Module:** `job_requirements.py`  
**Dataset:** `evaluation/requirements/` gold set v0.1.1 (12 fixtures)

## What is measured

| Dimension | Method |
|-----------|--------|
| Span fidelity | Extracted text equals gold sentence; span indices slice correctly |
| Category | `LANGUAGE` / `EDUCATION` / `EXPERIENCE` / `SKILL` / `RESPONSIBILITY` / … |
| Modality | `MUST` / `PREFERRED` / `RESPONSIBILITY` / `UNKNOWN` |
| Negation | Negated sentences stay visible and flagged; never positive promotion |
| No body promotion | Keyword-only paragraphs → zero requirements |
| Review status | Every extracted item starts as `REVIEW` |

## Fixtures (n=12)

6 EN + 6 TR covering MUST, PREFERRED, RESPONSIBILITY, EDUCATION, EXPERIENCE, LANGUAGE, and negation.

## Current result (automated)

Covered by `engine/tests/test_requirement_gold.py` and `test_job_requirements.py`.

| Check | Expected |
|-------|----------|
| Each gold sentence → exactly 1 requirement | yes |
| category / modality / negated match gold | yes |
| review_status is REVIEW | yes |
| body-keyword soup → empty | yes |

**Inter-annotator agreement:** `NOT_MEASURED`  
**Live job-board sample:** `NOT_MEASURED`  
**Commercial JD parser parity:** `NOT_MEASURED`

## Limits

- Sentence-level only; multi-paragraph postings not scored as a unit.
- Synthetic text; no real employer postings.
- OR-groups kept as single explicit sentences (no expansion engine yet).

## How to re-run

```bash
cd engine && pytest tests/test_requirement_gold.py tests/test_job_requirements.py -v
```
