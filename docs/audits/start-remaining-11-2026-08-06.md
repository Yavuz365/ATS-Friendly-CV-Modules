# Remaining 11 items — progress (2026-08-07)

Branch: `feat/start-remaining-11-items`  
Authority: Canonical Backlog only. No production-ready claims.

## Progress

| ID | Action | Status |
|----|--------|--------|
| **MAT-003** | Feature-flagged ESCO adapter + **offline micro concept subset** (4 foreign-trade terms, pin v1.2.1). Default OFF. Matches are always `review_required`. Tests cover OFF/ON paths. | Strong skeleton |
| **JOB-004** | 12 annotated TR/EN requirement fixtures + extractor validation tests. | Strong skeleton |
| **ING-005** | Field-level evaluator + **wired into binary gold corpus test runner**. Dataset-card field section. | Strong skeleton |

## Explicitly not started

- `EVAL-002`, `EVAL-003`, `EVAL-004`
- `OPS-002`, `OPS-003`, `OPS-004`
- `OUT-001`, `REL-20`

## Safety rules applied

- Default matching behaviour unchanged (ESCO flag OFF).
- No personal data.
- No floating revisions.
- Ingestion contracts untouched.
- All new code additive and tested.

## Next recommended steps

1. CI green + merge PR #15.
2. EVAL-003 evaluation card templates (parser / requirement / matching).
3. Only with explicit approval: OPS integrations or REL-20 gate work.
