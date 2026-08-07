# Canonical 72-item status ledger — 2026-08-07

Authority: the 72-item Canonical Backlog only. Legacy bare `OPS`, `RES`, `TD`, `Y36` and `ATSE` identifiers are not execution authority unless explicitly mapped.

Status rule:

- `COMPLETE` means repository-side acceptance evidence exists in code/tests/docs.
- `PARTIAL` means repository implementation exists or has started, but a required CI artifact, external system, official source, publication or human approval is still missing.
- A file or skeleton alone is not completion evidence.

Current branch: `feat/start-remaining-11-items`.

| Canonical ID | Status | Evidence or remaining acceptance condition |
|---|---|---|
| F0-001 | PARTIAL | Historical-baseline workflow and freeze script exist; requires a verified green Actions run and uploaded `legacy-baseline-3b6cce1` artifact. |
| F0-002 | COMPLETE | ADR-000 and non-production maturity language are present. |
| F0-003 | COMPLETE | Historical P0 failures are represented by regression tests. |
| F0-004 | COMPLETE | Feature-freeze/release-boundary documentation exists. |
| STAB-001 | COMPLETE | Runtime data moved into installable package resources. |
| STAB-002 | COMPLETE | Domain-pack data is packaged and discoverable. |
| STAB-003 | COMPLETE | Wheel/sdist manifest verification exists. |
| STAB-004 | COMPLETE | Clean-wheel installation and runtime smoke are in CI. |
| STAB-005 | COMPLETE | Typed data/process status contracts exist. |
| STAB-006 | COMPLETE | Empty requirements produce `NOT_EVALUATED`, not fake full coverage. |
| STAB-007 | COMPLETE | Gate and numeric-boundary validation exists. |
| STAB-008 | COMPLETE | CLI exit-code and top-level error contract exists. |
| STAB-009 | COMPLETE | Module-boundary errors are surfaced through typed/explicit handling. |
| STAB-010 | COMPLETE | Circular external-comparator calibration is disabled. |
| STAB-011 | COMPLETE | Universal ATS/interview-ready verdict language is removed from active product output. |
| STAB-012 | COMPLETE | Typed QA result objects exist. |
| STAB-013 | COMPLETE | JSON/Markdown/CLI render from the shared decision contract. |
| STAB-014 | COMPLETE | v1.5.1 schema and golden payloads exist. |
| STAB-015 | COMPLETE | Unicode/token-boundary matching regressions exist. |
| STAB-016 | COMPLETE | Coverage and explanation paths use the shared matcher. |
| STAB-017 | COMPLETE | Action-verb intent mapping is repaired. |
| STAB-018 | COMPLETE | Arbitrary JD body skills are not promoted to MUST. |
| STAB-019 | COMPLETE | Lexical support is not labelled factual verification. |
| STAB-020 | COMPLETE | Ruff and type-check policy are configured as required gates. |
| STAB-021 | COMPLETE | Build/install/schema/data/docs/security workflow gates exist. |
| STAB-022 | COMPLETE | GitHub Actions are commit-SHA pinned and dependency provenance is recorded. |
| STAB-023 | COMPLETE | Active README/CLI/module-status/limitations documentation is aligned. |
| REL-151 | COMPLETE | v1.5.1 stabilization release-gate evidence is documented. |
| C-001 | COMPLETE | ADR-001 product boundary and non-goals are accepted. |
| C-002 | COMPLETE | SourceArtifact, CandidateFact and Evidence contracts exist. |
| C-003 | COMPLETE | JobPostingSnapshot and JobRequirement contracts exist. |
| C-004 | COMPLETE | ParseResult, GateResult and DiagnosticResult contracts exist. |
| C-005 | COMPLETE | ChangeSet, DecisionReport and ApplicationEvent contracts exist. |
| C-006 | COMPLETE | Shared enums and conversion rules are centralized. |
| C-007 | COMPLETE | Stable error taxonomy and API/CLI mappings exist. |
| C-008 | COMPLETE | G0-G4 gate and diagnostic interfaces are implemented. |
| C-009 | COMPLETE | Versioned policy/configuration registry exists. |
| C-010 | COMPLETE | Legacy score is isolated behind an explicit uncalibrated adapter. |
| C-011 | COMPLETE | Producer-consumer contract tests exist. |
| REL-20A1 | PARTIAL | Commit-pinned release manifests exist; requires actual `v2.0.0-alpha.1` and `v2.0.0-alpha.2` tags/prereleases with wheel, sdist, source archive and SHA256SUMS. |
| ING-001 | COMPLETE | Real DOCX OOXML ingestion with structural reporting exists. |
| ING-002 | COMPLETE | Text-layer PDF ingestion with page evidence exists. |
| ING-003 | COMPLETE | Scanned/mixed-PDF detection and optional OCR boundary exist. |
| ING-004 | COMPLETE | Deterministic genuine binary gold corpus exists. |
| ING-005 | PARTIAL | Field-level evaluator, stable ordering, missing-field failures, summary output and corpus tests exist; requires verified green CI/binary-corpus evidence. |
| JOB-001 | COMPLETE | Immutable job-posting snapshots exist. |
| JOB-002 | COMPLETE | Requirement spans/categories/modality/negation extraction exists. |
| JOB-003 | COMPLETE | Immutable requirement review/approval versioning exists. |
| JOB-004 | PARTIAL | Synthetic TR/EN gold labels and tests exist; requires real human-reviewed annotation approval/version evidence. |
| EVD-001 | COMPLETE | CandidateFact/Evidence/Conflict persistence exists. |
| EVD-002 | COMPLETE | Sensitivity, consent, redaction and retention controls exist. |
| MAT-001 | COMPLETE | Exact-boundary baseline and explanations exist. |
| MAT-002 | COMPLETE | Reviewed locale-aware synonym adapter exists. |
| MAT-003 | PARTIAL | Default-off review-required ESCO research adapter exists; requires official pinned ESCO source, licence and checksum provenance. |
| MAT-004 | COMPLETE | Revision-pinned semantic adapter boundary exists. |
| MAT-005 | COMPLETE | Exact→synonym→ontology→semantic→human-review cascade exists. |
| SYN-001 | COMPLETE | Untrusted-document/prompt-separation boundary exists. |
| SYN-002 | COMPLETE | Allowlisted evidence-bound ChangeSet exists. |
| SYN-003 | COMPLETE | Protected identity/company/title/date/degree/language/metric invariants exist. |
| SYN-004 | COMPLETE | Human approval, rejection and rollback workflow exists. |
| QA-001 | COMPLETE | Severity/blocking rules replace an aggregate health verdict. |
| QA-002 | COMPLETE | Style, cliché and quantification signals are advisory. |
| EVAL-001 | COMPLETE | Research labels and genuine complex fixtures are repaired/available. |
| EVAL-002 | PARTIAL | Durable append-only SQLite provenance reads and reopen tests exist; requires a verified green CI run on this head. |
| EVAL-003 | PARTIAL | Versioned evaluation cards and automated fixture/test-reference drift checks exist; requires verified green CI. |
| EVAL-004 | PARTIAL | Closed vendor-registry schema and empty registry policy exist; requires an accepted real reviewed source-versioned entry unless empty operation is accepted by the human owner. |
| OPS-001 | COMPLETE | ApplicationEvent store preserves missing/censoring semantics. |
| OPS-002 | PARTIAL | Repository interface/docs can be prepared; requires authenticated least-privilege read-only probes for GitHub, Notion, Drive and one tracker. |
| OPS-003 | PARTIAL | Schema/specification work can be prepared; requires a real MySQL deployment and verified Metabase dashboard. |
| OPS-004 | PARTIAL | Orchestration contracts/stubs can be prepared; requires an authenticated controlled n8n/OpenClaw smoke run. |
| OUT-001 | PARTIAL | Prospective-study design skeleton exists; requires preregistration/ethics/consent and explicit human approval before data collection. |
| REL-20 | PARTIAL | Production-readiness checklist exists; requires all gate evidence SHAs, verified timestamps, security/privacy/ops evidence and human sign-off. |

## Totals

| Status | Count |
|---|---:|
| COMPLETE | 59 |
| PARTIAL | 13 |
| NOT_STARTED | 0 |
| TOTAL | 72 |

## Partial set

`F0-001`, `REL-20A1`, `ING-005`, `JOB-004`, `MAT-003`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `OPS-002`, `OPS-003`, `OPS-004`, `OUT-001`, `REL-20`.

This ledger must not be changed to `COMPLETE` based only on code presence. Each remaining acceptance condition must be linked to actual evidence.
