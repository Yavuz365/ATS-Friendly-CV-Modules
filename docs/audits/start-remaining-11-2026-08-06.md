# Remaining 11 items — progress (2026-08-07)

Branch: `feat/start-remaining-11-items`  
Authority: Canonical Backlog only. No production-ready claims.

## Progress

| ID | Action | Status |
|----|--------|--------|
| **MAT-003** | Feature-flagged ESCO + offline micro subset. Default OFF. | Strong skeleton |
| **JOB-004** | 12 annotated TR/EN requirement fixtures + tests. | Strong skeleton |
| **ING-005** | Field-level evaluator wired into gold corpus runner. | Strong skeleton |
| **EVAL-003** | 4 evaluation cards published + tests. | Published v0.1.0 |
| **EVAL-002** | Append-only provenance log (`provenance.py`) + SQLite option + card + tests. | Strong skeleton |

## Still open

- `EVAL-004` (vendor capability registry)
- `OPS-002`, `OPS-003`, `OPS-004`
- `OUT-001`, `REL-20`

## Safety rules applied

- Default matching behaviour unchanged.
- No personal data.
- No invented commercial ATS metrics.
- Provenance is explicit opt-in recording (no hidden monkey-patch).

## Next recommended steps

1. CI green + merge PR #15.
2. EVAL-004 only as a *schema* registry (no fake vendor scores).
3. OPS / REL only with explicit human approval.
