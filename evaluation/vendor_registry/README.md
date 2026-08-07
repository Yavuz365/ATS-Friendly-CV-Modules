# Vendor Capability Registry (EVAL-004) — v0.1.0

Source-versioned registry for **claims about** commercial / open tools.

## Hard rules

1. Every entry must cite a `source` + pinned `source_version` (never `latest`).
2. Default capability status is `NOT_MEASURED` unless we actually measured it.
3. **No fabricated numeric scores.** `scores` may exist only when `measurement_status` is `MEASURED_INTERNAL` or `MEASURED_EXTERNAL`.
4. Vendor marketing copy is stored as `CLAIMED_BY_SOURCE`, not as engine truth.
5. Empty `entries: []` is a valid honest state.

## Files

| File | Role |
|------|------|
| `schema.json` | JSON Schema Draft 2020-12 |
| `registry.json` | Live registry instance (currently empty) |

## Out of scope for v0.1

- Paying for commercial ATS tenants
- Publishing comparative leaderboards
- Treating this registry as ranking ground truth
