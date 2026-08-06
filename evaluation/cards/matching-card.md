# Matching Cascade Evaluation Card — v0.1.0

**Date:** 2026-08-07  
**Backlog:** EVAL-003 / MAT-001..005  
**Module:** `matching.py` + `esco_adapter.py`  
**Fixtures:** unit tests + ESCO micro subset (4 concepts)

## Cascade order

1. **EXACT** — Unicode word-boundary count  
2. **SYNONYM** — reviewed locale dictionary (revision-hashed)  
3. **ONTOLOGY** — version-pinned adapter (ESCO micro; feature-flag OFF by default)  
4. **SEMANTIC** — optional revision-pinned adapter  
5. **HUMAN_REVIEW** / **NONE**

Ontology and semantic matches are **always** `review_required=True`. They never
produce a final verified PASS by themselves.

## What is measured

| Dimension | Method |
|-----------|--------|
| Boundary exact match | SAP ≠ sapphire, R ≠ risk (regression gold) |
| Synonym path | reviewed dict + deterministic revision hash |
| Ontology default | flag OFF → stage skipped (`None` adapter) |
| Ontology enabled | micro ESCO MATCH only with boundary evidence + review flag |
| No silent zero | missing adapter → NONE / NOT_RUN, not fake FAIL score |

## Current result (automated)

| Suite | Focus |
|-------|--------|
| `test_matching_cascade.py` | cascade stages, review flags |
| `test_esco_adapter.py` | default-off, micro MATCH, review_required |
| `test_regressions.py` | historical boundary / empty-req defects |

**Full ESCO dump coverage:** `NOT_MEASURED`  
**Embedding semantic quality:** `NOT_MEASURED`  
**Human agreement on ontology hits:** `NOT_MEASURED`  
**Commercial matcher parity:** `NOT_MEASURED`

## Limits

- ESCO micro subset is research-only (4 foreign-trade concepts), not official ESCO export.
- Feature flag remains OFF in default product paths.
- Fuzzy/legacy Jaccard only when no semantic adapter is configured; still review-required.

## How to re-run

```bash
cd engine && pytest tests/test_matching_cascade.py tests/test_esco_adapter.py -v
```
