# Contributing Guide

## Principles (non-negotiable)
- **Honesty/Provenance:** every CV bullet must trace back to the evidence bank.
- **Coverage > density:** no keyword stuffing.
- **Score = diagnostic:** not an approximation claim about any proprietary vendor formula.
- **H1 rule:** revision loop stops at `score≥target OR closable_gap=0`; this is immutable.
- **No universal thresholds or outcome claims:** thresholds require a source/date/language/
  domain/comparator-versioned evaluation profile. See ADR-001 and `docs/limitations.md`.

## Product contract

ADR-001 was accepted on 2026-08-05. New changes must preserve the evidence-first status,
verification and G0–G4 contracts. UI/vendor automation and production claims remain out of
scope until their own evidence gates are met.

## Development Setup

```bash
# Install with dev dependencies
make dev

# Run tests (must be green before PR)
make test

# Lint & format
make lint

# Full check (lint + test)
make check
```

## Pre-commit Hooks

This repo uses pre-commit for code quality:

```bash
pip install pre-commit
pre-commit install
```

Hooks: `ruff` (lint + format), `mypy` (type check), `trailing-whitespace`, `check-json`.

## Rules

1. `make check` and `make package-check` must pass before any PR.
2. New feature = new test. Do not break audit-corrections (clamp, ParseGate, gap classification).
3. Data updates (`engine/data/*.json`) must include source documentation (Grammarly/ESCO/etc.).
4. All new modules must be exported in `__init__.py` and added to `__all__`.
5. Update `CHANGELOG.md` for every version bump.
6. README/module status must reflect actual file layout and limits.
7. New public payloads require a closed Draft 2020-12 schema and golden example.
8. Unknown/missing/error states may not be replaced by numeric fallbacks.

## Module Architecture

```
engine/ats_engine/
├── Core: text, bm25, scoring, lexicons, jd_parser, evidence_bank, synthesis, report, cli
├── Scoring: multilevel (L1/L2/L3), cv_parser (ParseGate), domain_packs
└── Quality: calibration, cliche_tone, completeness_guard, format_metadata_hygiene,
             locale_consistency, quantification_score
```

## Style Guide

- **Formatter:** ruff format (configured in `engine/pyproject.toml`)
- **Linter:** ruff check (pycodestyle, pyflakes, isort, etc.)
- **Types:** mypy strict mode
- **Naming:** snake_case for functions/variables, PascalCase for classes
- **Docstrings:** Google style
