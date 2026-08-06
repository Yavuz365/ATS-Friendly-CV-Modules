# Provenance & Screening Log Card — v0.1.0

**Date:** 2026-08-07  
**Backlog:** EVAL-002  
**Module:** `ats_engine.provenance`

## What is recorded

| Kind | Meaning |
|------|--------|
| `ARTIFACT_INGEST` | Binary/text artifact accepted by ingestion |
| `REQUIREMENT_EXTRACT` | Requirement span extraction event |
| `MATCH_STAGE` | Matcher stage outcome for a term |
| `SCREENING_DECISION` | Gate / decision outcome for a candidate-run |
| `EVALUATION_RUN` | Start/end markers for an evaluation batch |
| `NOTE` | Free-form but structured annotation |

Entries are **append-only**. Duplicate IDs are rejected. Optional SQLite path
makes evaluation runs durable without coupling to the full contract store.

## What is not claimed

- Commercial ATS search ranking behaviour — `NOT_MEASURED`
- Vendor screening funnel parity — `NOT_MEASURED`
- Cross-system distributed tracing — `NOT_MEASURED`

## Tests

```bash
cd engine && pytest tests/test_provenance.py -v
```

## Limits

- In-process ledger; not a multi-node audit bus.
- Callers must explicitly record events (no hidden monkey-patching of pipeline).
