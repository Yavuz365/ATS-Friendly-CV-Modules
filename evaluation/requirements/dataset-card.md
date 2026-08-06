# Annotated TR/EN Job Requirement Gold Set — v0.1.1

## Purpose (JOB-004)

Provide a versioned, human-reviewable set of job-posting sentences with explicit
span, category, modality and negation labels for TR and EN.

This is a **research evaluation fixture**, not a production requirement extractor
benchmark. It exists so that `job_requirements.py` and future evaluation cards
have a stable, personal-data-free reference.

## Scope (v0.1.1)

| Fixture ID | Lang | Category | Modality | Negated |
|------------|------|----------|----------|--------|
| `REQ-EN-MUST-001` | EN | SKILL | MUST | no |
| `REQ-EN-NEG-001` | EN | SKILL | MUST | **yes** |
| `REQ-EN-EDU-001` | EN | EDUCATION | MUST | no |
| `REQ-EN-EXP-001` | EN | EXPERIENCE | MUST | no |
| `REQ-EN-PREF-001` | EN | SKILL | PREFERRED | no |
| `REQ-EN-RESP-001` | EN | RESPONSIBILITY | RESPONSIBILITY | no |
| `REQ-TR-MUST-001` | TR | SKILL | MUST | no |
| `REQ-TR-PREF-001` | TR | SKILL | PREFERRED | no |
| `REQ-TR-NEG-001` | TR | LANGUAGE | MUST | **yes** |
| `REQ-TR-EDU-001` | TR | EDUCATION | MUST | no |
| `REQ-TR-EXP-001` | TR | EXPERIENCE | MUST | no |
| `REQ-TR-RESP-001` | TR | RESPONSIBILITY | RESPONSIBILITY | no |

Binary or multi-page postings are out of scope. Only sentence-level text is stored.

## Label policy

- Every item has `span_start`, `span_end`, `category`, `modality`, `negated`.
- Extractor output starts as `REVIEW`; gold labels never auto-promote to PASS.
- Negated sentences must not become positive requirements.
- No body-keyword promotion is allowed in the gold set itself.
- OR-groups (e.g. business **or** economics) stay as a single explicit sentence.

## Privacy

Fully synthetic. No real employer names, candidate data or live job URLs.

## Known limits

- Not a statistically powered sample.
- Does not measure commercial ATS parsing behaviour.
- Field-level document evaluation lives under `evaluation/gold/` (ING-005).
- Full inter-annotator agreement study is future work.
