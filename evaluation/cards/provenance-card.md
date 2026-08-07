# Provenance & Screening Log Card — v0.2.0

**Date:** 2026-08-07  
**Backlog:** EVAL-002  
**Module:** `ats_engine.provenance`  
**Tests:** `engine/tests/test_provenance.py`

## What is recorded

| Kind | Meaning |
|------|---------|
| `ARTIFACT_INGEST` | Binary/text artifact accepted by ingestion |
| `REQUIREMENT_EXTRACT` | Requirement span extraction event |
| `MATCH_STAGE` | Matcher stage outcome for a term |
| `SCREENING_DECISION` | Gate / decision outcome for a candidate-run |
| `EVALUATION_RUN` | Start/end markers for an evaluation batch |
| `NOTE` | Free-form but structured annotation |

Entries are append-only. Duplicate IDs are rejected both in memory and after a
SQLite database is closed and reopened. In SQLite mode, `list_for_run()` and
`list_all()` query persisted rows directly and return deterministic
`occurred_at, id` ordering.

Persisted enum or JSON corruption raises `ProvenanceStorageError`; it does not
silently return an empty ledger.

## Automated evidence

`engine/tests/test_provenance.py` covers:

- in-memory recording and run filtering;
- close/reopen durability for ingest, match and decision events;
- run isolation after reopen;
- duplicate-ID rejection after reopen;
- parent-ID and detail reconstruction;
- malformed JSON and unknown-enum typed failures;
- JSON-serializable export.

## What is not claimed

- Commercial ATS search ranking behaviour — `NOT_MEASURED`
- Vendor screening funnel parity — `NOT_MEASURED`
- Cross-system distributed tracing — `NOT_MEASURED`

## How to re-run

```bash
cd engine && pytest tests/test_provenance.py -v
```

## Limits

- This is a local SQLite/in-memory ledger, not a multi-node audit bus.
- Callers must explicitly record events; production paths are not monkey-patched.
- CI acceptance remains separate from repository-side implementation evidence.
