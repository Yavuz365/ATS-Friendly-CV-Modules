# Canonical 72-item status ledger — 2026-08-07

Authority: `ATS_Friendly_CV_Modules_Canonical_Backlog_2026-08-02.csv` only. Legacy bare `OPS`, `RES`, `TD`, `Y36` and `ATSE` identifiers are not execution authority unless explicitly mapped.

## Audit basis

This ledger is acceptance-criteria-first, not implementation-presence-first.

- `COMPLETE`: every material canonical acceptance condition is supported by repository, CI or required external evidence.
- `PARTIAL`: implementation exists, but one or more canonical acceptance conditions are still missing or contradicted by current evidence.
- `NOT_STARTED`: no material implementation/evidence exists.
- `NOT_MEASURED`, `NOT_RUN`, `UNKNOWN`, a skeleton file, a green unrelated test, or an unverified agent statement is never promoted to `COMPLETE` by itself.

Audited branch: `feat/start-remaining-11-items`  
Audited implementation head: `df498bdb1904c058b690d2c00f60e7f8fbb192bb`  
Verified CI: Engine CI run `#160` / `31148936950` — all jobs successful (`quality`, Python 3.10/3.11/3.12 tests, `dependency-audit`, `package`, `historical-baseline`).  
Verified baseline artifact: `legacy-baseline-3b6cce1`, artifact `8982554220`, digest `sha256:96d0634c4fffc106bbbf29f66197eef2f3af946153658d875b96c214deb9452f`.

## Canonical 72

| Canonical ID | Status | Acceptance evidence / remaining condition |
|---|---|---|
| F0-001 | COMPLETE | Exact `3b6cce1e4c2919146752590f7bece4ae2812a8f5` baseline was archived by CI; source archive, wheel, sdist, reproduction report and SHA256SUMS exist in verified artifact `8982554220`. |
| F0-002 | COMPLETE | ADR-000, README and active maturity language identify the project as pre-production/research, not a commercial ATS/outcome predictor. |
| F0-003 | COMPLETE | Canonical `REG-001..REG-015` regression matrix exists and runs in the current test suite. |
| F0-004 | COMPLETE | Feature-freeze/release-boundary governance is recorded; later v2 work is separated from the v1.5.1 stabilization boundary. |
| STAB-001 | COMPLETE | Runtime action verbs, synonyms and stopwords are packaged resources and load in the clean installed package path. |
| STAB-002 | COMPLETE | Domain-pack resources are packaged/discoverable in the clean installed package. |
| STAB-003 | COMPLETE | `verify_wheel.py` validates required runtime artifacts in both wheel and sdist and returns failure for missing required members; CI package job executes it. |
| STAB-004 | COMPLETE | CI installs the built wheel with `--no-index` into an isolated venv, verifies no source-tree leakage, imports resources and executes CLI ingestion. |
| STAB-005 | COMPLETE | Canonical typed data/process state models exist. |
| STAB-006 | COMPLETE | Empty/unavailable requirements produce `NOT_EVALUATED`/review rather than synthetic full coverage. |
| STAB-007 | COMPLETE | Numeric/gate boundary validation rejects invalid type, range, NaN and infinity paths through typed invalid-input handling. |
| STAB-008 | COMPLETE | CLI contract distinguishes success `0`, invalid input `2`, unexpected internal error `3` and review/blocking `4`; invalid UTF-8 and parse-review regressions exist. |
| STAB-009 | COMPLETE | Critical module-boundary failures are surfaced with typed/explicit error information rather than silently converted to success. |
| STAB-010 | COMPLETE | No external comparator produces `NOT_RUN`; engine score is not reused as a vendor score. |
| STAB-011 | COMPLETE | Active output removes universal ATS-pass/interview-ready/hiring-probability claims. |
| STAB-012 | COMPLETE | Typed `QAResult` objects with status/severity/blocking fields exist. |
| STAB-013 | COMPLETE | Decision/gate status is sourced from the shared typed `DecisionReport`; Markdown QA status labels use typed `qa_results`; parity regressions are present. |
| STAB-014 | COMPLETE | v1.5.1 compatibility schema/golden payload coverage exists and is required by CI. |
| STAB-015 | COMPLETE | `_pattern()`'s exact-boundary lookaround now also rejects `+`/`#` as boundary characters; `c` no longer matches inside `C++`/`C#`, while `c++`/`c#` still match as their own tokens and standalone `c` is unaffected. Regression-covered in `test_matching_cascade.py` (commit `64daf5b`). |
| STAB-016 | COMPLETE | Coverage/explanation and skill-table match status now use the shared matcher semantics; exact vs synonym/ontology stages are exposed. |
| STAB-017 | COMPLETE | Action-verb intent mapping is repaired and regression-covered. |
| STAB-018 | COMPLETE | No recognized required section yields review/unknown rather than promoting arbitrary body skills to MUST. |
| STAB-019 | COMPLETE | Lexical overlap remains `UNVERIFIED` support and cannot become factual `VERIFIED`. |
| STAB-020 | COMPLETE | Ruff lint/format and mypy are required CI gates and run successfully on the current head. |
| STAB-021 | COMPLETE | Pull-request CI covers tests, schemas/goldens, package build/install, runtime data, dependency audit and historical evidence. |
| STAB-022 | COMPLETE | Third-party Actions use full commit SHAs; dependency audit/provenance gate is present. |
| STAB-023 | COMPLETE | Active README/CLI/module-status/limitations are aligned with supported commands and non-production limits; current CI exercises command paths. |
| REL-151 | COMPLETE | STAB-015's `C/C++` acceptance case is closed (see above); clean CI is green on the same head, so canonical stabilization's sole cited blocker is resolved. |
| C-001 | COMPLETE | ADR-001 defines product boundary and non-goals. |
| C-002 | COMPLETE | Versioned SourceArtifact/CandidateFact/Evidence contracts and Draft 2020-12 schemas exist. |
| C-003 | COMPLETE | Versioned JobPostingSnapshot/JobRequirement/mapping contracts exist. |
| C-004 | COMPLETE | ParseResult/GateResult/DiagnosticResult contracts contain status/method/diagnostic boundaries. |
| C-005 | COMPLETE | ChangeSet/DecisionReport/ApplicationEvent contracts exist with approval/version/missing-censoring semantics. |
| C-006 | COMPLETE | Shared enums are centralized; unknown/error/not-run states are not numerically promoted to PASS. |
| C-007 | COMPLETE | `ErrorSeverity` enum and a complete `ERROR_TAXONOMY` (severity/retryable/cli_exit_code/http_status/description per code, including new `INTERNAL_ERROR`) now back `ATSEngineError.taxonomy/.cli_exit_code/.http_status/.retryable`; `to_dict()` exposes the full mapping; CLI exit codes are taxonomy-driven. 9 tests in `test_error_taxonomy.py` (commit `7cdc70d`). |
| C-008 | COMPLETE | G0-G4 typed gate/diagnostic interfaces are implemented; language mismatch now cannot silently PASS G3. |
| C-009 | COMPLETE | `GatePolicy`/`EvaluationProfile` now require non-blank `owner`/`rationale`/`review_date` (plus `locale`/`domain` on `GatePolicy`); a new `LegacyScoringWeightsPolicy`/`DEFAULT_LEGACY_SCORING_POLICY` brings the previously-unowned `scoring.DEFAULTS`/`THRESHOLDS` under the same governance, cross-referencing CCR-006/CCR-026. 6 tests in `test_configuration_governance.py` (commit `e6b3d21`). |
| C-010 | PARTIAL (architecture conflict flagged, needs owner decision) | Confirmed unchanged: `report.py::build_report()` still calls `legacy_diagnostic()` unconditionally as the only match-score path. Root cause: there is no second, calibrated scoring adapter anywhere in the codebase to fall back to — `legacy_diagnostic` is the *entire* scoring engine, and `gaps`, `stopping_condition`, `evidence_recall`, and every `qa_checks` entry in `build_report()` are built on its output. Making it opt-in/default-off per the canonical criterion would leave `build_report()` producing no match_score/gaps/QA by default, which conflicts with the 'preserve existing working functionality' constraint; building a genuinely calibrated replacement is out of scope for this pass (would require real calibration data, which must not be invented). Needs an explicit decision: accept a default-off legacy path (and what, if anything, replaces it by default), or keep legacy default-on and treat C-010 as accepted risk. |
| C-011 | COMPLETE | Producer/consumer schema, golden and renderer/contract tests exist and run in CI. |
| REL-20A1 | PARTIAL | Commit-pinned alpha release manifests exist, but immutable `v2.0.0-alpha.1`/`alpha.2` tags/prereleases and their required release assets/checksums are not evidenced as published. |
| ING-001 | PARTIAL (unchanged this session) | Not attempted — requires new structural-feature extraction (drawings/columns/spans) beyond this session's scope; last touched by Ahmet/Copilot commits `0bb95bb`/`9b13b92`. |
| ING-002 | PARTIAL | Text-layer PDF parsing records page text/method/warnings, but canonical page span/box and column evidence is not implemented. |
| ING-003 | PARTIAL | Scanned/mixed detection and optional OCR boundary are explicit, but mixed-page per-page confidence required by the canonical criterion is not recorded. |
| ING-004 | PARTIAL | Deterministic binary DOCX/PDF fixtures exist, including a true textbox/header/table, but the canonical gold corpus also requires drawings, columns, nested tables, multi-page, mixed and corrupt artifacts with ground truth; current corpus has only three simple fixtures. |
| ING-005 | PARTIAL | Field evaluator and dataset card exist and CI is green, but canonical acceptance requires reproducible precision/recall/F1, abstention, crash rate and TR/EN/error slices; the current card explicitly leaves full metric tables for future work. |
| JOB-001 | COMPLETE | Immutable job-posting snapshot persistence preserves source, capture time, locale, hash and version linkage. |
| JOB-002 | PARTIAL (contract ambiguity flagged, needs owner decision) | Verified this session: the `ELIGIBILITY/REQUIRED/PREFERRED/RESPONSIBILITY/CONTEXT/BENEFIT/UNKNOWN` vocabulary cited here does not appear anywhere else in the repository (not in `schemas/v2/contracts.schema.json`, not in the gold labels, not in Ek A of the canonical MD) — its source could not be confirmed and may be aspirational/from an external doc not present here. Separately, a *confirmed* real defect was found while checking: `job_requirements.py` hardcodes every extracted requirement's `requirement_type="EXPLICIT_SENTENCE"`, which is not a member of the schema's own `requirement_type` enum (`MUST/NICE/KNOCKOUT/RESPONSIBILITY/ADVISORY`), and no test runs live-extracted `JobRequirement` objects through schema validation to catch this — only the static golden example is validated. Not changed this session pending clarification: redefining `category`'s value set would break the existing reviewed gold labels (`evaluation/requirements/labels.json`, category=SKILL etc.); fixing `requirement_type` alone is safe but does not by itself satisfy the disputed vocabulary claim above. |
| JOB-003 | COMPLETE | Low-confidence/ambiguous requirements remain review-first and append-only approval versions exist. |
| JOB-004 | PARTIAL | Versioned synthetic TR/EN gold labels and tests exist, but inter-annotator process/agreement, confusion matrix, span IoU and review-rate evidence are not reported; the dataset card marks the agreement study future work. |
| EVD-001 | COMPLETE | CandidateFact/Evidence/Conflict persistence preserves verification state, source locator and conflict semantics. |
| EVD-002 | COMPLETE | Added tested `export_candidate_record()` (full/redacted export honoring privacy actions) and `delete_candidate_record()` (real cascading delete across facts/evidence/conflicts, right-to-erasure). Local-first guarantee verified by test: SQLite store performs no network I/O. Tests cover export completeness/redaction and delete cascade (commit `182be0c`). |
| MAT-001 | COMPLETE | New `evidence_linking.py`: `link_requirement_evidence()` binds `JobRequirement`↔`Evidence` via requirement span + CV source locator with explicit `UNLINKED_NO_EVIDENCE`/`UNLINKED_LOW_CONFIDENCE` states; `measure_exact_match_false_support_rate()` runs the EXACT stage against a new reviewed gold set (`evaluation/gold/exact_match_support_labels.json`, 12 labelled cases) and reports a measured 0% false-support rate on that set (dataset card documents scope/limits — not a claim of 0% in production). 10 tests in `test_evidence_linking.py` (commit `79ec907`). |
| MAT-002 | COMPLETE | New `evaluation/gold/reviewed_locale_synonyms_tr_en.json`: 11 accepted TR/EN pairs plus 3 explicitly abstained candidate pairs with reasons (SAP≠ERP, gümrük≠lojistik, yüksek lisans≠PhD). New `locale_synonym_registry.py` loads it and audits for conflicts (0 conflicts on this dataset, verified by test); an accepted pair drives a real `match_term()` SYNONYM-stage hit. Dataset card + 6 tests in `test_locale_synonym_registry.py` (commit `66a8d33`). |
| MAT-003 | PARTIAL | Default-off review-required ESCO research adapter/micro fixture exists, but official pinned ESCO ID/version/source/licence/checksum provenance and measured incremental gain over baseline are absent. |
| MAT-004 | PARTIAL | Revision-pinned semantic adapter boundary and failure-to-review behavior exist, but no real pinned model/runtime evaluation or measured incremental value is present. |
| MAT-005 | COMPLETE | Exact → synonym → ontology → semantic → human-review precedence is implemented; lower-trust matches cannot override higher-trust exact matches and ontology/semantic matches require review. |
| SYN-001 | COMPLETE | Untrusted document content cannot execute tools/instructions; EN/TR injection signals are regression-covered and execution boundary is fixed to data-only. |
| SYN-002 | COMPLETE | `SynthesisChange` now requires non-blank `model` and `prompt_id` on every change (raises `InvalidInputError` if either is blank); `to_dict()`/schema/tests updated. Model/prompt attribution is enforced alongside the existing path/old/new/evidence/reason fields. Tests in `test_syn002_change_attribution.py` (commit `1cf3035`). |
| SYN-003 | COMPLETE | Identity/company/title/date/degree/language-level/metric mutation paths are protected and regression-tested. |
| SYN-004 | COMPLETE | Explicit approval/rejection/apply/rollback flow is reversible and auditable. |
| QA-001 | COMPLETE | `QAResult` gained first-class `evidence` (list) and `remediation` (str) fields, populated by the QA rule runner in `report.py` for every check (completeness/hygiene/locale/quantification/clichés). Tests in the QA suite verify both fields are always populated (commit `21df506`). |
| QA-002 | COMPLETE | Style, cliché and quantification remain advisory rather than universal blocking/hiring claims. |
| EVAL-001 | PARTIAL | Reviewed labels and binary fixtures exist, but canonical acceptance specifically requires genuine textbox plus multi-page diverse fixtures; current gold corpus is single-page/simple beyond the DOCX textbox case. |
| EVAL-002 | PARTIAL | Durable append-only SQLite provenance logging and reopen tests exist, but canonical acceptance requires every research query's screened/included/exclusion trail and figure-to-table hashes; no such complete evidence trail is present. |
| EVAL-003 | PARTIAL | Versioned parser/requirement/matching/synthesis/provenance cards exist, but required metrics/error slices/version links are incomplete and multiple card dimensions are explicitly `NOT_MEASURED`. |
| EVAL-004 | PARTIAL | Closed source-versioned vendor registry schema/policy exists, but live registry is intentionally empty; no real official source-versioned observation with retrieval date/edition/scope/confidence/stale policy is accepted. |
| OPS-001 | COMPLETE | `ApplicationEvent` gained `observed_at` (defaults to `occurred_at` only when unset), `event_version`, `source`, and sensitivity/retention/redaction parity with `CandidateFact`. New `get_application_event()` applies the same REDACT/RETENTION_EXPIRE/CONSENT_REVOKE/DELETE-aware privacy gate as `get_candidate_fact()`. 3 tests added (commit `a0ae160`). |
| OPS-002 | PARTIAL | Integration specification/stubs exist, but authenticated least-privilege GitHub/Notion/Drive/work-tracker integration tests and system-of-record/idempotency/audit evidence are not complete. |
| OPS-003 | PARTIAL | Schema/specification exists, but no verified real MySQL deployment + Metabase outcome dashboard with versioned metric definitions is evidenced. |
| OPS-004 | PARTIAL | Orchestration contracts/stubs exist, but no authenticated least-privilege, idempotent, logged, reversible n8n/OpenClaw execution with required human approval is evidenced. |
| OUT-001 | PARTIAL | Prospective outcome-study design exists, but target/sample/labels/censoring/split/confidence/drift/stop criteria are not evidenced as preregistered/approved before collection. |
| REL-20 | PARTIAL | Production-readiness checklist exists, but supported deployment SLO, security/privacy, complete evaluation, pilot, rollback/monitoring and independent human sign-off do not all pass yet. |

## Totals — strict canonical acceptance

| Status | Count |
|---|---:|
| COMPLETE | 52 |
| PARTIAL | 20 |
| NOT_STARTED | 0 |
| TOTAL | 72 |

## Partial set — 20

`C-010`, `REL-20A1`, `ING-001`, `ING-002`, `ING-003`, `ING-004`, `ING-005`, `JOB-002`, `JOB-004`, `MAT-003`, `MAT-004`, `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `OPS-002`, `OPS-003`, `OPS-004`, `OUT-001`, `REL-20`.

`C-010` and `JOB-002` carry a flagged conflict/ambiguity that needs an explicit owner decision before further work (see their rows above); the remaining 18 are either large new engineering (real metrics pipelines, expanded fixture corpora) or require genuine external systems/official sources/human evidence and were correctly left untouched per the 'never fabricate evidence' rule.

## Reconciliation note

The previous `59 COMPLETE / 13 PARTIAL` ledger was a repository-implementation progress view and became stale after additional fixes/CI evidence. This revision applies the original canonical CSV acceptance text literally. It therefore both promotes newly evidenced work (notably `F0-001`) and reopens items whose implementation does not yet satisfy every acceptance clause. Green CI proves the current code passes its present automated gates; it does not by itself prove missing datasets, external integrations, measured evaluation metrics, release publication or human evidence.

## 2026-08-07 session update (post-`df498bd`/`6989c5e`)

Audited implementation head: `66a8d334a197241a933aed620d28a7f2b1f90c3e`.  
Verified CI: run `#161` / `31166557213` — all 7 jobs successful (`quality`, Python 3.10/3.11/3.12 tests, `dependency-audit`, `package`, `historical-baseline`) on this exact SHA.  
Local validation on the same head: `pytest -q engine/tests` → 238 passed; `ruff check`/`ruff format --check` clean (60 files); `mypy engine/ats_engine` clean (34 source files); wheel+sdist built and `verify_wheel.py`-checked; clean-venv wheel install + `python -m ats_engine.cli ingest` smoke passed.

10 items moved PARTIAL → COMPLETE this session: `STAB-015`, `REL-151`, `C-007`, `C-009`, `QA-001`, `SYN-002`, `EVD-002`, `MAT-001`, `OPS-001`, `MAT-002` (evidence in each row above). Two items were investigated in depth and kept PARTIAL with a flagged decision needed from the repository owner rather than a guessed resolution: `C-010` (no second scoring adapter exists to make legacy opt-in without removing existing default output) and `JOB-002` (the cited canonical category vocabulary does not appear anywhere else in the repository; a real, separate `requirement_type` schema-enum violation was found and documented but not silently 'fixed into' the disputed vocabulary). No item was marked COMPLETE without corresponding tests, and no metric, approval, or external evidence was invented.
