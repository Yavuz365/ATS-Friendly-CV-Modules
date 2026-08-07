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
| STAB-015 | PARTIAL | Unicode boundary regressions exist for several cases, but current matcher still treats `C` as an exact boundary hit inside `C++`; canonical `C/C++` gold criterion is not satisfied. |
| STAB-016 | COMPLETE | Coverage/explanation and skill-table match status now use the shared matcher semantics; exact vs synonym/ontology stages are exposed. |
| STAB-017 | COMPLETE | Action-verb intent mapping is repaired and regression-covered. |
| STAB-018 | COMPLETE | No recognized required section yields review/unknown rather than promoting arbitrary body skills to MUST. |
| STAB-019 | COMPLETE | Lexical overlap remains `UNVERIFIED` support and cannot become factual `VERIFIED`. |
| STAB-020 | COMPLETE | Ruff lint/format and mypy are required CI gates and run successfully on the current head. |
| STAB-021 | COMPLETE | Pull-request CI covers tests, schemas/goldens, package build/install, runtime data, dependency audit and historical evidence. |
| STAB-022 | COMPLETE | Third-party Actions use full commit SHAs; dependency audit/provenance gate is present. |
| STAB-023 | COMPLETE | Active README/CLI/module-status/limitations are aligned with supported commands and non-production limits; current CI exercises command paths. |
| REL-151 | PARTIAL | Current clean CI is green, but canonical stabilization cannot be considered fully closed while STAB-015's explicit `C/C++` acceptance case remains open. |
| C-001 | COMPLETE | ADR-001 defines product boundary and non-goals. |
| C-002 | COMPLETE | Versioned SourceArtifact/CandidateFact/Evidence contracts and Draft 2020-12 schemas exist. |
| C-003 | COMPLETE | Versioned JobPostingSnapshot/JobRequirement/mapping contracts exist. |
| C-004 | COMPLETE | ParseResult/GateResult/DiagnosticResult contracts contain status/method/diagnostic boundaries. |
| C-005 | COMPLETE | ChangeSet/DecisionReport/ApplicationEvent contracts exist with approval/version/missing-censoring semantics. |
| C-006 | COMPLETE | Shared enums are centralized; unknown/error/not-run states are not numerically promoted to PASS. |
| C-007 | PARTIAL | Stable error codes and CLI behavior exist, but canonical acceptance also requires per-error severity, retryability and exit/HTTP mapping; current public error objects do not provide the full mapping. |
| C-008 | COMPLETE | G0-G4 typed gate/diagnostic interfaces are implemented; language mismatch now cannot silently PASS G3. |
| C-009 | PARTIAL | Versioned GatePolicy/EvaluationProfile exist, but canonical metadata requires owner, rationale/evidence, locale/domain and review date for each configured value; legacy scoring weights/threshold metadata also remains outside that complete registry. |
| C-010 | PARTIAL | Legacy diagnostic is explicitly labeled uncalibrated, but `build_report()` still invokes it as the default match-score path; canonical criterion says legacy output is opt-in. |
| C-011 | COMPLETE | Producer/consumer schema, golden and renderer/contract tests exist and run in CI. |
| REL-20A1 | PARTIAL | Commit-pinned alpha release manifests exist, but immutable `v2.0.0-alpha.1`/`alpha.2` tags/prereleases and their required release assets/checksums are not evidenced as published. |
| ING-001 | PARTIAL | Real OOXML parsing handles paragraphs/tables/header/footer/textboxes and the duplication defect is fixed, but canonical acceptance also requires drawings/columns/spans to be represented or explicitly unsupported; that contract is incomplete. |
| ING-002 | PARTIAL | Text-layer PDF parsing records page text/method/warnings, but canonical page span/box and column evidence is not implemented. |
| ING-003 | PARTIAL | Scanned/mixed detection and optional OCR boundary are explicit, but mixed-page per-page confidence required by the canonical criterion is not recorded. |
| ING-004 | PARTIAL | Deterministic binary DOCX/PDF fixtures exist, including a true textbox/header/table, but the canonical gold corpus also requires drawings, columns, nested tables, multi-page, mixed and corrupt artifacts with ground truth; current corpus has only three simple fixtures. |
| ING-005 | PARTIAL | Field evaluator and dataset card exist and CI is green, but canonical acceptance requires reproducible precision/recall/F1, abstention, crash rate and TR/EN/error slices; the current card explicitly leaves full metric tables for future work. |
| JOB-001 | COMPLETE | Immutable job-posting snapshot persistence preserves source, capture time, locale, hash and version linkage. |
| JOB-002 | PARTIAL | Raw spans, modality, negation and useful categories are extracted, but the implemented category vocabulary does not satisfy the canonical `ELIGIBILITY/REQUIRED/PREFERRED/RESPONSIBILITY/CONTEXT/BENEFIT/UNKNOWN` contract. |
| JOB-003 | COMPLETE | Low-confidence/ambiguous requirements remain review-first and append-only approval versions exist. |
| JOB-004 | PARTIAL | Versioned synthetic TR/EN gold labels and tests exist, but inter-annotator process/agreement, confusion matrix, span IoU and review-rate evidence are not reported; the dataset card marks the agreement study future work. |
| EVD-001 | COMPLETE | CandidateFact/Evidence/Conflict persistence preserves verification state, source locator and conflict semantics. |
| EVD-002 | PARTIAL | Consent, sensitivity, redaction, retention and revocation controls are implemented, but canonical acceptance also requires tested export/delete paths and local-first/log-redaction guarantees; those paths are not evidenced. |
| MAT-001 | PARTIAL | Exact Unicode-boundary matching and explanations exist, but canonical requirement/evidence locator linkage plus a measured false-support gold rate is not evidenced. |
| MAT-002 | PARTIAL | A revision-hashed reviewed-synonym adapter interface exists, but no accepted versioned reviewed/conflict-tested locale synonym dataset with abstention evidence is present. |
| MAT-003 | PARTIAL | Default-off review-required ESCO research adapter/micro fixture exists, but official pinned ESCO ID/version/source/licence/checksum provenance and measured incremental gain over baseline are absent. |
| MAT-004 | PARTIAL | Revision-pinned semantic adapter boundary and failure-to-review behavior exist, but no real pinned model/runtime evaluation or measured incremental value is present. |
| MAT-005 | COMPLETE | Exact → synonym → ontology → semantic → human-review precedence is implemented; lower-trust matches cannot override higher-trust exact matches and ontology/semantic matches require review. |
| SYN-001 | COMPLETE | Untrusted document content cannot execute tools/instructions; EN/TR injection signals are regression-covered and execution boundary is fixed to data-only. |
| SYN-002 | PARTIAL | Allowlisted evidence-bound ChangeSet enforces path/old/new/evidence/reason, but canonical acceptance also requires model/prompt metadata on each change; current `SynthesisChange` contract lacks it. |
| SYN-003 | COMPLETE | Identity/company/title/date/degree/language-level/metric mutation paths are protected and regression-tested. |
| SYN-004 | COMPLETE | Explicit approval/rejection/apply/rollback flow is reversible and auditable. |
| QA-001 | PARTIAL | Typed rule status/severity/blocking/message/details exist, but canonical rule contract also requires explicit evidence and remediation fields for each rule; those are not complete first-class fields. |
| QA-002 | COMPLETE | Style, cliché and quantification remain advisory rather than universal blocking/hiring claims. |
| EVAL-001 | PARTIAL | Reviewed labels and binary fixtures exist, but canonical acceptance specifically requires genuine textbox plus multi-page diverse fixtures; current gold corpus is single-page/simple beyond the DOCX textbox case. |
| EVAL-002 | PARTIAL | Durable append-only SQLite provenance logging and reopen tests exist, but canonical acceptance requires every research query's screened/included/exclusion trail and figure-to-table hashes; no such complete evidence trail is present. |
| EVAL-003 | PARTIAL | Versioned parser/requirement/matching/synthesis/provenance cards exist, but required metrics/error slices/version links are incomplete and multiple card dimensions are explicitly `NOT_MEASURED`. |
| EVAL-004 | PARTIAL | Closed source-versioned vendor registry schema/policy exists, but live registry is intentionally empty; no real official source-versioned observation with retrieval date/edition/scope/confidence/stale policy is accepted. |
| OPS-001 | PARTIAL | Append-only ApplicationEvent storage and censoring behavior exist, but canonical criterion requires event versions, source, distinct observed/occurred time and event privacy/retention tests; `ApplicationEvent` has `occurred_at` but no distinct observed-time field and event privacy/retention evidence is incomplete. |
| OPS-002 | PARTIAL | Integration specification/stubs exist, but authenticated least-privilege GitHub/Notion/Drive/work-tracker integration tests and system-of-record/idempotency/audit evidence are not complete. |
| OPS-003 | PARTIAL | Schema/specification exists, but no verified real MySQL deployment + Metabase outcome dashboard with versioned metric definitions is evidenced. |
| OPS-004 | PARTIAL | Orchestration contracts/stubs exist, but no authenticated least-privilege, idempotent, logged, reversible n8n/OpenClaw execution with required human approval is evidenced. |
| OUT-001 | PARTIAL | Prospective outcome-study design exists, but target/sample/labels/censoring/split/confidence/drift/stop criteria are not evidenced as preregistered/approved before collection. |
| REL-20 | PARTIAL | Production-readiness checklist exists, but supported deployment SLO, security/privacy, complete evaluation, pilot, rollback/monitoring and independent human sign-off do not all pass yet. |

## Totals — strict canonical acceptance

| Status | Count |
|---|---:|
| COMPLETE | 42 |
| PARTIAL | 30 |
| NOT_STARTED | 0 |
| TOTAL | 72 |

## Partial set — 30

`STAB-015`, `REL-151`, `C-007`, `C-009`, `C-010`, `REL-20A1`, `ING-001`, `ING-002`, `ING-003`, `ING-004`, `ING-005`, `JOB-002`, `JOB-004`, `EVD-002`, `MAT-001`, `MAT-002`, `MAT-003`, `MAT-004`, `SYN-002`, `QA-001`, `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `OPS-001`, `OPS-002`, `OPS-003`, `OPS-004`, `OUT-001`, `REL-20`.

## Reconciliation note

The previous `59 COMPLETE / 13 PARTIAL` ledger was a repository-implementation progress view and became stale after additional fixes/CI evidence. This revision applies the original canonical CSV acceptance text literally. It therefore both promotes newly evidenced work (notably `F0-001`) and reopens items whose implementation does not yet satisfy every acceptance clause. Green CI proves the current code passes its present automated gates; it does not by itself prove missing datasets, external integrations, measured evaluation metrics, release publication or human evidence.
