# Remaining 11 items — progress (2026-08-07)

Branch: `feat/start-remaining-11-items`  
Authority: Canonical Backlog only. No production-ready claims.

## Progress

| ID | Action | Status |
|----|--------|--------|
| **MAT-003** | Feature-flagged ESCO + offline micro subset (4 concepts). Default OFF. | Strong skeleton |
| **JOB-004** | 12 annotated TR/EN requirement fixtures + tests. | Strong skeleton |
| **ING-005** | Field-level evaluator wired into gold corpus runner. | Strong skeleton |
| **EVAL-003** | Published 4 evaluation cards (parser, requirement, matching, synthesis/gate) + index + presence tests. | **Published v0.1.0** |

## Explicitly not started / still open

- `EVAL-002` (search/screening + artifact provenance logs)
- `EVAL-004` (vendor capability registry)
- `OPS-002`, `OPS-003`, `OPS-004`
- `OUT-001`, `REL-20`

## Safety rules applied

- Default matching behaviour unchanged.
- No personal data.
- Cards use `NOT_MEASURED` instead of invented commercial metrics.
- Forbidden product language checks in tests.

## Next recommended steps

1. CI green + merge PR #15.
2. EVAL-002 provenance log skeleton (if desired).
3. OPS / REL only with explicit human approval.
