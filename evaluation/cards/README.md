# Evaluation Cards (EVAL-003 / EVAL-002)

Versioned, evidence-bound evaluation cards for the research prototype.

These cards document **what was measured**, **on which fixtures**, **with which
limits**. They are not marketing claims and do not assert commercial ATS parity
or hiring outcomes.

| Card | Scope | Dataset / module |
|------|--------|------------------|
| [parser-card.md](parser-card.md) | Binary DOCX/PDF ingestion + field-level | `evaluation/gold/` (ING-004/005) |
| [requirement-card.md](requirement-card.md) | TR/EN requirement span/modality/negation | `evaluation/requirements/` (JOB-004) |
| [matching-card.md](matching-card.md) | Exact → synonym → ontology → semantic cascade | unit + micro ESCO (MAT-*) |
| [synthesis-gate-card.md](synthesis-gate-card.md) | Safe synthesis invariants + G0–G4 gates | contracts + regressions |
| [provenance-card.md](provenance-card.md) | Search/screening + artifact provenance log | `provenance.py` (EVAL-002) |

## Rules

- Every metric must name its fixture set and revision.
- `NOT_MEASURED` is preferred over invented numbers.
- No overall “ATS pass rate” or “interview-ready” language.
- Cards are updated only with a new card version + date.
