# REL-20 — Production-Readiness Gate Checklist

**Status:** Checklist only. Gate is **NOT** passed.  
**Date:** 2026-08-07  
**Product maturity:** research prototype / pre-production (ADR-000)

## Gate rule

All rows must be `PASS` with linked evidence before any production claim.
Current default for every row: `OPEN`.

| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| REL20-01 | All STAB + contract alpha release tags published | OPEN | needs real GitHub Releases |
| REL20-02 | Clean-wheel install smoke green in CI | OPEN | |
| REL20-03 | No silent fail-open on empty requirements | OPEN | regressions exist; CI proof needed |
| REL20-04 | Personal data policy + retention enforced | OPEN | storage helpers exist; audit pending |
| REL20-05 | Evaluation cards current for parser/match/gate | PARTIAL | EVAL-003 v0.1 cards |
| REL20-06 | Vendor claims not treated as engine truth | PARTIAL | EVAL-004 empty registry policy |
| REL20-07 | Ops integrations under explicit auth | OPEN | OPS-002..004 not started |
| REL20-08 | Outcome study design approved before calibration | OPEN | OUT-001 design skeleton only |
| REL20-09 | Security review (deps, secrets, public repo history) | OPEN | |
| REL20-10 | Human sign-off recorded | OPEN | |

## Explicit statement

This repository is **not** production-ready. Completing this file’s rows is a
human process; code alone cannot close REL-20.
