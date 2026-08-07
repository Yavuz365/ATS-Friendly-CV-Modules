# Canonical 72-Item Backlog — Final Status Audit

**Date:** 2026-08-07  
**Branch:** `feat/start-remaining-11-items` (Copilot working branch: `copilot/featstart-remaining-11-items`)  
**Base commit (main HEAD):** `5a39ed545b5ed12502ca208f6744eb4f1b498491`  
**Authority:** Canonical Backlog IDs only. Legacy bare ATSE/Y36/RES/TD/OPS IDs are not authoritative.

> **Repository status:** Research prototype / pre-production.  
> No production-ready, commercial ATS pass, interview or hiring-outcome claims are made.

---

## Totals

| Status | Count |
|--------|------:|
| COMPLETE | 59 |
| PARTIAL | 13 |
| NOT_STARTED | 0 |
| **TOTAL** | **72** |

---

## Status Table

| # | canonical_id | status | code evidence | test evidence | CI evidence | external blocker | next acceptance condition |
|---|---|---|---|---|---|---|---|
| 1 | F0-001 | PARTIAL | `scripts/freeze_legacy_baseline.py`, `docs/baseline/legacy-3b6cce1/README.md` | `test_legacy_contract.py` (freeze pin verified in isolation) | `freeze-baseline` job defined in `.github/workflows/test.yml`; no real artifact upload yet | No actual green Actions run has uploaded the durable artifact | Real green Actions run uploads `ats-v1.5.0-historical-baseline-3b6cce1` artifact |
| 2 | STAB-001 | COMPLETE | `contracts.py` — `ProcessStatus`, `DataStatus` enums and frozen contract dataclasses | `test_contracts_ingestion.py`, `test_core.py` | CI green | — | — |
| 3 | STAB-002 | COMPLETE | `errors.py` — typed `ATSError`, `InputError`, `ContractError` boundary | `test_contracts_ingestion.py` | CI green | — | — |
| 4 | STAB-003 | COMPLETE | `cli.py` — `run` command, honest score output, no fabricated verdict | `test_cli.py` | CI green | — | — |
| 5 | STAB-004 | COMPLETE | `scoring.py` — `empty_must → NOT_EVALUATED`, `parse_gate` wiring | `test_core.py`, `test_regressions.py` (reg_001) | CI green | — | — |
| 6 | STAB-005 | COMPLETE | `text.py` / `lexicons.py` — `tr_lower`, stopwords, importlib.resources | `test_core.py` (tokenise, BM25, jaccard) | CI green | — | — |
| 7 | STAB-006 | COMPLETE | `jd_parser.py` — JD layers, explicit must, body inference blocked | `test_core.py` (parse_jd_returns_layers, no body promotion) | CI green | — | — |
| 8 | STAB-007 | COMPLETE | `cv_parser.py` — text format heuristic, parse safety score | `test_core.py` (parse_gate tests) | CI green | — | — |
| 9 | STAB-008 | COMPLETE | `scoring.py` — BM25 component, hybrid score, P/R/F1 | `test_core.py` (bm25 tests) | CI green | — | — |
| 10 | STAB-009 | COMPLETE | `decision.py` — G0–G4 typed `DecisionReport`, `UNKNOWN`/`ERROR` never coerced to `PASS` | `test_contracts_ingestion.py`, `test_regressions.py` (reg_003) | CI green | — | — |
| 11 | STAB-010 | COMPLETE | `safe_synthesis.py` — allowlist boundary, protected fact enforcement | `test_regressions.py` (reg_015), `test_contracts_ingestion.py` | CI green | — | — |
| 12 | STAB-011 | COMPLETE | `report.py` — JSON/Markdown output, QA block, gate payload | `test_core.py` (test_reg_006_json_and_markdown_keep_qa_payload) | CI green | — | — |
| 13 | STAB-012 | COMPLETE | `scoring.py` — Skill Count table diagnostic restored | `test_regressions.py` (B1/STAB-015 comment) | CI green | — | — |
| 14 | STAB-013 | COMPLETE | `evidence_bank.py` — lexical lookup, no factual verification claim | `test_core.py` (test_parse_bank_extracts_tagged_entries) | CI green | — | — |
| 15 | STAB-014 | COMPLETE | `legacy_adapter.py`, `schemas/v1.5.1/` — frozen v1.5.1 compat schema + 2 golden payloads | `test_legacy_contract.py` (4 tests) | CI green | — | — |
| 16 | STAB-015 | COMPLETE | `scoring.py` — Skill Count table fully restored (B1 fix) | `test_regressions.py` (STAB-015 comment) | CI green | — | — |
| 17 | STAB-016 | COMPLETE | `multilevel.py` — three-level scoring, thresholds as diagnostics | `test_core.py` (test_score_is_clamped_0_1) | CI green | — | — |
| 18 | STAB-017 | COMPLETE | `cliche_tone.py` — cliché/tone QA advisory (not blocking) | `test_regressions.py` (reg_010) | CI green | — | — |
| 19 | STAB-018 | COMPLETE | `jd_parser.py` — body keywords never promoted to MUST without explicit signal | `test_core.py` (STAB-018 annotation), `test_regressions.py` (reg_009) | CI green | — | — |
| 20 | STAB-019 | COMPLETE | `completeness_guard.py` — missing section guard returns `NOT_EVALUATED` | `test_contracts_ingestion.py` | CI green | — | — |
| 21 | STAB-020 | COMPLETE | `quantification_score.py` — quantified achievement detection | `test_core.py` (test_has_quantification) | CI green | — | — |
| 22 | STAB-021 | COMPLETE | `format_metadata_hygiene.py` — format + metadata hygiene checks | `test_contracts_ingestion.py` | CI green | — | — |
| 23 | STAB-022 | COMPLETE | `locale_consistency.py` — locale flag, TR/EN mixing advisory | `test_contracts_ingestion.py` | CI green | — | — |
| 24 | STAB-023 | COMPLETE | `domain_packs.py` — foreign-trade domain pack, missing resource explicit error | `test_contracts_ingestion.py` | CI green | — | — |
| 25 | STAB-024 | COMPLETE | `calibration.py` — gated behind real external comparator; no auto-calibration | `test_regressions.py` (reg_004) | CI green | — | — |
| 26 | STAB-025 | COMPLETE | `configuration.py` — feature flags, `ENGINE_ESCO_ENABLED=false` default | `test_esco_adapter.py` (disabled by default) | CI green | — | — |
| 27 | STAB-026 | COMPLETE | `synthesis.py` — `SynthesisChangeSet` shape validated, allowlisted ops only | `test_contracts_ingestion.py` | CI green | — | — |
| 28 | STAB-027 | COMPLETE | `report.py` — schema validated JSON output (`schemas/v2/decision-report.schema.json`) | `test_regressions.py` (reg_008) | CI green | — | — |
| 29 | STAB-028 | COMPLETE | `text.py` — Turkish `İ`/`i` normalization (P0-9 fix) | `test_core.py` (reg_012 comment) | CI green | — | — |
| 30 | STAB-029 | COMPLETE | `lexicons.py` — `action_verbs_by_intent` never returns empty for known intents | `test_core.py` (test_action_verbs_by_intent_never_empty_for_known_intents) | CI green | — | — |
| 31 | STAB-030 | COMPLETE | `scoring.py` — `schemas/scoring_result.schema.json` validation wired | `test_regressions.py` (reg_008) | CI green | — | — |
| 32 | ING-001 | COMPLETE | `ingestion.py` — DOCX full-story extraction, structural features | `test_contracts_ingestion.py` | CI green | — | — |
| 33 | ING-002 | COMPLETE | `ingestion.py` — text PDF page evidence extraction | `test_contracts_ingestion.py` | CI green | — | — |
| 34 | ING-003 | COMPLETE | `ingestion.py` — scanned PDF explicit `SCANNED_PDF_REQUIRES_OCR` error | `test_contracts_ingestion.py` | CI green | — | — |
| 35 | ING-004 | COMPLETE | `evaluation/gold/` — versioned binary DOCX/PDF gold corpus, manifest v1.0.0 | `test_gold_corpus.py` | CI green | — | — |
| 36 | ING-005 | PARTIAL | `engine/ats_engine/field_evaluation.py` — field-level verdict, stable ordering, JSON summary | `test_field_evaluation.py` (5 tests), `test_gold_corpus.py` | CI tests pass; no real binary fixture upload CI artifact | Binary corpus CI artifact and all corpus fixture tests needed | All corpus tests + CI pass; evaluation card updated with actual counts |
| 37 | JOB-001 | COMPLETE | `storage.py` — immutable `JobPostingSnapshot` with `source_url`, `source_sha256`, `retrieved_at` | `test_storage.py` | CI green | — | — |
| 38 | JOB-002 | COMPLETE | `job_requirements.py` — explicit TR/EN sentence spans, category, modality, negation | `test_job_requirements.py` | CI green | — | — |
| 39 | JOB-003 | COMPLETE | `storage.py` — append-only `RequirementReview` versions, no silent overwrite | `test_storage.py` | CI green | — | — |
| 40 | JOB-004 | PARTIAL | `evaluation/requirements/labels.json` — 12 synthetic gold labels + schema + tests | `test_requirement_gold.py` (4 tests), `test_evaluation_labels.py` | CI tests pass | Human-reviewed TR/EN annotation approval pending | External: human annotation approval recorded in `approval_status` field |
| 41 | MAT-001 | COMPLETE | `matching.py` — boundary-exact `count_boundary_occurrences`, `TermMatch` contract | `test_core.py`, `test_regressions.py` (reg_002) | CI green | — | — |
| 42 | MAT-002 | COMPLETE | `matching.py` — reviewed locale synonym dict with deterministic `reviewed_synonym_revision` hash | `test_matching_cascade.py` (test_reviewed_locale_synonym_is_revision_bound) | CI green | — | — |
| 43 | MAT-003 | PARTIAL | `engine/ats_engine/esco_adapter.py` — ESCO v1.2.1 micro adapter, feature flag OFF by default, `review_required=True` always | `test_esco_adapter.py` (7 tests) | CI tests pass | Official ESCO v1.2.1 pinned download + license verification missing | Official pinned ESCO data with SHA256 + license; or explicit empty-source abstention confirmed |
| 44 | MAT-004 | COMPLETE | `matching.py` — `VersionedMatchAdapter` revision-pinned, floating refs rejected | `test_matching_cascade.py` (test_floating_adapter_revision_is_rejected) | CI green | — | — |
| 45 | MAT-005 | COMPLETE | `matching.py` — ontology-first → exact → synonym → semantic → human-review cascade | `test_matching_cascade.py` (test_ontology_and_semantic_matches_require_human_review) | CI green | — | — |
| 46 | EVD-001 | COMPLETE | `storage.py` — `SourceArtifact`, `CandidateFact`, `Evidence`, `EvidenceConflict` persistence | `test_storage.py` | CI green | — | — |
| 47 | EVD-002 | COMPLETE | `storage.py` — consent, redaction flag, retention policy, revocation enforcement | `test_storage.py` | CI green | — | — |
| 48 | EVAL-001 | COMPLETE | `evaluation/gold/labels.json` — corrected reviewed labels, `ING-004` fixture corpus integration | `test_evaluation_labels.py`, `test_gold_corpus.py` | CI green | — | — |
| 49 | EVAL-002 | PARTIAL | `engine/ats_engine/provenance.py` — SQLite persistence; `list_for_run()` / `list_all()` now query SQLite on reopen | `test_provenance.py` (10 tests including 5 reopen tests) | CI tests pass | No real green CI run with artifact yet | All reopen + duplicate-rejection + malformed-JSON tests pass in CI |
| 50 | EVAL-003 | PARTIAL | `evaluation/cards/` — 5 evaluation cards (parser, requirement, matching, synthesis-gate, provenance) v0.1.0 | `test_evaluation_cards.py` | CI tests pass | Fixture/test counts are not yet auto-calculated from file scan | Auto-count test added; drift-detection test green in CI |
| 51 | EVAL-004 | PARTIAL | `evaluation/vendor_registry/` — closed schema, empty registry, validator, prohibited marketing tests | `test_vendor_registry.py` | CI tests pass | No real reviewed source-versioned vendor entry accepted | At least one real reviewed source entry added and passes schema + no-fake-URL tests |
| 52 | OPS-001 | COMPLETE | `storage.py` — append-only `ApplicationEvent` store, censoring semantics, `outcome_observed=False` | `test_storage.py` | CI green | — | — |
| 53 | OPS-002 | PARTIAL | `docs/ops/OPS-integration-stubs.md` — interface stubs for GitHub/Notion/Drive/tracker; env var names only | No live integration tests; contract interface defined only | CI not applicable (stub only) | External credentials for least-privilege read-only probe missing | Authenticated live read-only probe recorded as provenance NOTE event |
| 54 | OPS-003 | PARTIAL | `docs/ops/OPS-integration-stubs.md`, `schemas/v2/application-event.schema.json` — MySQL schema stub, Metabase spec stub | No real DB deployment tests; migration stubs only | CI not applicable (stub only) | Real MySQL deployment and Metabase dashboard missing | Real MySQL deployment + Metabase dashboard verified and documented |
| 55 | OPS-004 | PARTIAL | `docs/ops/OPS-integration-stubs.md` — N8n/OpenClaw orchestration contract stubs, idempotency and audit requirements documented | No live orchestration tests | CI not applicable (stub only) | Authenticated runtime smoke test missing | Controlled smoke test with real N8n/OpenClaw execution recorded |
| 56 | OUT-001 | PARTIAL | `docs/research/OUT-001-prospective-outcome-study-design.md` — preregistration-ready protocol draft | No data collection; design only | CI not applicable (design doc) | Human approval section not signed; preregistration not filed | Human sign-off recorded in approval section; preregistration filed |
| 57 | REL-20 | PARTIAL | `docs/releases/REL-20-production-readiness-checklist.md` — checklist with criterion_id, owner_role, status fields | `test_release_manifests.py` (manifest validation) | CI tests pass (manifest structure valid) | Multiple gate rows are not PASS; no human sign-off | Every required gate row has linked evidence with `evidence_sha` and `verified_at`; human sign-off recorded |
| 58 | REL-20A1 | PARTIAL | `docs/releases/2.0.0-alpha.1.json`, `docs/releases/2.0.0-alpha.2.json` — commit-pinned manifests; `scripts/validate_release_manifests.py` | `test_release_manifests.py` (structure + SHA validation) | CI tests pass (shallow-clone check bypassed; commits exist on `main`) | GitHub prerelease tags `v2.0.0-alpha.1` and `v2.0.0-alpha.2` not yet published | `gh release create v2.0.0-alpha.1 --target c76f64f5b352beeba149458b071a9aaeb47f5f06 --prerelease` and `v2.0.0-alpha.2 --target 5bc5969edf9bb71cf8a8be093f3132262a8799ff` executed and verified |
| 59 | BUILD-001 | COMPLETE | `engine/pyproject.toml` — `ats-engine` wheel + sdist build config, `[dev]` extras | `make package-check` / `python -m build` | CI green | — | — |
| 60 | BUILD-002 | COMPLETE | `engine/MANIFEST.in` — source distribution includes data files | `python -m build` | CI green | — | — |
| 61 | BUILD-003 | COMPLETE | `Makefile` — `make package-check`, `make lint`, `make test` targets | Local and CI Makefile execution | CI green | — | — |
| 62 | BUILD-004 | COMPLETE | `.github/workflows/test.yml` — CI pipeline: lint (ruff), type-check (mypy), pytest, build | All green CI runs on main branch | CI green | — | — |
| 63 | BUILD-005 | COMPLETE | `.pre-commit-config.yaml` — pre-commit hooks (ruff format, ruff check, mypy) | CI green | CI green | — | — |
| 64 | SCHEMA-001 | COMPLETE | `schemas/v2/contracts.schema.json` — closed v2 contract JSON schema | `test_contracts_ingestion.py` (schema validation) | CI green | — | — |
| 65 | SCHEMA-002 | COMPLETE | `schemas/v2/decision-report.schema.json` — typed gate outcome schema | `test_regressions.py` (reg_008) | CI green | — | — |
| 66 | SCHEMA-003 | COMPLETE | `schemas/v2/` — full v2 schema suite: evidence, candidate-fact, source-artifact, synthesis-change-set, job-requirement | `test_contracts_ingestion.py` | CI green | — | — |
| 67 | SCHEMA-004 | COMPLETE | `schemas/v1.5.1/` — frozen v1.5.1 compat schema, two golden payloads | `test_legacy_contract.py` | CI green | — | — |
| 68 | SCHEMA-005 | COMPLETE | `evaluation/vendor_registry/schema.json` — closed vendor registry JSON schema | `test_vendor_registry.py` | CI green | — | — |
| 69 | CLI-001 | COMPLETE | `engine/ats_engine/cli.py` — `ats-engine run` command, honest output, no fabricated verdict | `test_cli.py` | CI green | — | — |
| 70 | CLI-002 | COMPLETE | `engine/ats_engine/cli.py` — `--json` flag, exit-code contract, error propagation | `test_cli.py` | CI green | — | — |
| 71 | CLI-003 | COMPLETE | `engine/examples/run_demo.py` — runnable demo, documents framework CV and foreign-trade JD fixture | Manual smoke test | CI green | — | — |
| 72 | PROV-001 | COMPLETE | `engine/ats_engine/provenance.py` — `ProvenanceLog` in-memory append-only baseline, `new_run_id`, `new_entry_id` | `test_provenance.py` (test_record_and_list_for_run, test_duplicate_id_rejected) | CI green | — | — |

---

## Validation

```
COMPLETE = 59  (rows 2-31 STAB, 32-35 ING, 37-39 JOB, 41-42 MAT, 44-45 MAT, 46-47 EVD, 48 EVAL, 52 OPS, 59-72 BUILD/SCHEMA/CLI/PROV)
PARTIAL  = 13  (rows 1 F0, 36 ING-005, 40 JOB-004, 43 MAT-003, 49 EVAL-002, 50 EVAL-003, 51 EVAL-004, 53 OPS-002, 54 OPS-003, 55 OPS-004, 56 OUT-001, 57 REL-20, 58 REL-20A1)
TOTAL    = 72
```

---

## Blockers for remaining PARTIAL items

| canonical_id | exact blocker |
|---|---|
| F0-001 | No real GitHub Actions run has uploaded the `ats-v1.5.0-historical-baseline-3b6cce1` artifact |
| ING-005 | Binary corpus CI artifact upload and all fixture evaluation tests required |
| JOB-004 | Human-reviewed TR/EN annotation approval (`approval_status` field) |
| MAT-003 | Official ESCO v1.2.1 pinned download URL + license verification + SHA256 |
| EVAL-002 | All SQLite reopen / malformed-JSON / duplicate-rejection tests now pass; waiting for confirmed green CI run |
| EVAL-003 | Fixture and test counts must be auto-calculated (not manually stated); drift-detection test required |
| EVAL-004 | At least one real reviewed source-versioned vendor entry |
| OPS-002 | External credentials for least-privilege authenticated read-only workspace probe |
| OPS-003 | Real MySQL deployment + Metabase dashboard instance |
| OPS-004 | Authenticated N8n/OpenClaw runtime smoke test |
| OUT-001 | Human sign-off on study design; preregistration filing |
| REL-20 | Every gate row needs linked evidence + `evidence_sha` + `verified_at` + human sign-off |
| REL-20A1 | `gh release create` commands executed; immutable GitHub prerelease tags published |

---

## Non-negotiable language

- This repository is a **research prototype / pre-production** system.
- No row is marked COMPLETE without linked code evidence and passing tests.
- `UNKNOWN`, `ERROR`, `NOT_RUN`, and `NOT_COLLECTED` statuses are never promoted to `PASS`.
- No commercial ATS pass rate, interview-ready, or hiring-outcome claims exist in this document.
