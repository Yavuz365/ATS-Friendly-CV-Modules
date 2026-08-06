# Remaining 11 items — progress (2026-08-06 / 07)

Branch: `feat/start-remaining-11-items`  
Authority: Canonical Backlog only. No production-ready claims.

## Progress

| ID | Action | Status |
|----|--------|--------|
| **MAT-003** | Feature-flagged ESCO v1.2.1 adapter stub + tests. Default OFF → NOT_RUN. | Skeleton complete |
| **JOB-004** | Annotated TR/EN gold set expanded to **12 fixtures** (MUST/PREFERRED/RESPONSIBILITY/EDUCATION/EXPERIENCE/LANGUAGE + negation). Dataset-card + extractor validation tests. | Strong skeleton |
| **ING-005** | Field-level evaluation helper (`field_evaluation.py`) + unit tests. Dataset-card field-level section. Does not change ingestion. | Strong skeleton |

## Explicitly not started

- `EVAL-002`, `EVAL-003`, `EVAL-004`
- `OPS-002`, `OPS-003`, `OPS-004`
- `OUT-001`, `REL-20`

## Safety rules applied

- No change to default matching behaviour (ontology stage still skipped when flag is off).
- No personal data.
- No floating revisions.
- Existing ingestion/matching contracts left intact.
- New code is additive and tested.

## Next recommended steps

1. CI green + merge PR #15.
2. Optional: offline micro ESCO concept subset behind the same feature flag.
3. Wire field evaluator into gold corpus runner.
4. Only then touch EVAL-* cards.
