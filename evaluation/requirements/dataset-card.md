# Annotated TR/EN Job Requirement Gold Set — v0.1.0 (skeleton)

## Purpose (JOB-004)

Provide a small, versioned, human-reviewable set of job-posting sentences with
explicit span, category, modality and negation labels for TR and EN.

This is a **research evaluation fixture**, not a production requirement extractor
benchmark. It exists so that `job_requirements.py` and future evaluation cards
have a stable, personal-data-free reference.

## Scope (current skeleton)

| Fixture ID | Language | Focus |
|------------|----------|-------|
| `REQ-EN-MUST-001` | EN | Explicit MUST skill sentence |
| `REQ-EN-NEG-001` | EN | Negated requirement (must remain REVIEW) |
| `REQ-TR-MUST-001` | TR | Explicit zorunlu yetkinlik cümlesi |
| `REQ-TR-PREF-001` | TR | Tercih / nice-to-have cümlesi |

Binary or multi-page postings are out of scope for v0.1. Only sentence-level
text is stored.

## Label policy

- Every item has `span_start`, `span_end`, `category`, `modality`, `negated`.
- Extractor output starts as `REVIEW`; gold labels never auto-promote to PASS.
- Negated sentences must not become positive requirements.
- No body-keyword promotion is allowed in the gold set itself.

## Privacy

Fully synthetic. No real employer names, candidate data or live job URLs.

## Known limits

- Not a statistically powered sample.
- Does not measure commercial ATS parsing behaviour.
- Field-level document evaluation lives under `evaluation/gold/` (ING-005).
- Full inter-annotator agreement study is future work.
