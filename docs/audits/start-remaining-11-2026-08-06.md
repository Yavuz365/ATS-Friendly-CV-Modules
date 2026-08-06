# Remaining 11 items — safe start (2026-08-06)

Branch: `feat/start-remaining-11-items`  
Authority: Canonical Backlog only. No production-ready claims.

## What was started (non-breaking)

| ID | Action | Status |
|----|--------|--------|
| **MAT-003** | Feature-flagged ESCO v1.2.1 adapter stub (`esco_adapter.py`). Default OFF → `NOT_RUN` / abstain. Never produces verified PASS. Tests added. | Skeleton complete |
| **JOB-004** | Annotated TR/EN requirement gold set skeleton under `evaluation/requirements/` (dataset-card + 4 synthetic labels). | Skeleton complete |
| **ING-005** | Field-level evaluation section added to existing gold `dataset-card.md`. | Skeleton complete |

## Explicitly not started (still require human / external systems)

- `EVAL-002`, `EVAL-003`, `EVAL-004`
- `OPS-002`, `OPS-003`, `OPS-004`
- `OUT-001`, `REL-20`

## Safety rules applied

- No change to default matching behaviour (ontology stage still skipped when flag is off).
- No personal data introduced.
- No floating revisions allowed.
- Existing tests and contracts left intact.

## Next recommended steps

1. Merge this branch after CI green.
2. Expand JOB-004 labels with more TR/EN edge cases.
3. Wire a real (offline) ESCO concept subset only behind the feature flag + evaluation card.
4. Add field-level metric runner for ING-005.
