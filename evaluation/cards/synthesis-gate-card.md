# Safe Synthesis & Gate Evaluation Card — v0.1.0

**Date:** 2026-08-07  
**Backlog:** EVAL-003 / SYN-* / QA-* / C-008  
**Modules:** `safe_synthesis.py`, `decision.py`, `report.py`, contracts

## What is measured

| Dimension | Method |
|-----------|--------|
| Untrusted boundary | Synthesis only consumes allowlisted evidence IDs |
| Protected facts | Identity / company / title / date / degree / language / metrics not silently rewritten |
| ChangeSet shape | Allowlisted ops only; no free-form document rewrite |
| Gate outcomes | G0–G4 typed `DecisionReport`; `UNKNOWN`/`ERROR` never coerced to `PASS` |
| Empty requirements | `NOT_EVALUATED` — no fake 100% coverage |
| QA severity | Blocking vs advisory separation (style/cliché not blocking) |

## Current result (automated)

| Suite | Focus |
|-------|--------|
| `test_contracts_ingestion.py` | contract + parse wiring |
| `test_regressions.py` | empty-must, boundary, calibration, CLI honesty |
| `test_core.py` / CLI tests | report/decision smoke |

**Human approval + rollback workflow end-to-end:** partial (API present; full UX `NOT_MEASURED`)  
**Production export safety audit:** `NOT_MEASURED`  
**Live hiring decision outcomes:** `NOT_MEASURED` (OUT-001)

## Explicit non-claims

- No “ATS passed” or “interview-ready” aggregate verdict in v2 cards.
- No vendor-named auto-reject thresholds.
- Style / quantification signals remain advisory.

## Limits

- Cards track contract and regression evidence, not a large human-rated synthesis corpus.
- Gate thresholds are versioned research defaults, not calibrated on hiring outcomes.

## How to re-run

```bash
cd engine && pytest tests/test_regressions.py tests/test_contracts_ingestion.py -v
```
