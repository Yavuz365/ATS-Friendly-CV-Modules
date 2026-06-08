# Synthesis Protocol — The Engine

The detailed mechanics behind Layers 0–4: the Source Registry, layer-by-layer execution, conflict resolution, phase decomposition, and confidence scoring. Read this before running the synthesis engine.

## Contents
1. The Source Registry
2. Layer 0 — Intake & Mode
3. Layer 1 — Global Holistic Synthesis
4. Layer 2 — Phase Decomposition
5. Layer 3 — Deep Research & Cross-Validation
6. Layer 4 — Analysis
7. Conflict resolution framework
8. Confidence scoring

## 1. The Source Registry

The registry is the backbone of the whole skill. It is a single ledger of every source — external and internal — that anything in the report is allowed to rest on. If a claim can't point to a registry entry, it isn't a finding; it's your inference, and must be labelled as such.

Maintain it as a table. Keep it internally throughout; include a cleaned version in the report appendix.

| ID | Source | Type | Date / "as of" | Lang | Reliability | Note |
|----|--------|------|----------------|------|-------------|------|
| S1 | KAP filing, Company X | Primary / filing | 2026-02 | TR | High | Audited |
| S2 | Reuters article | News / secondary | 2026-05 | EN | High | |
| S3 | X / forum chatter | Social | 2026-05 | TR | Low | Sentiment only |
| I1 | user's "Q1_model.xlsx" | Internal / data | 2026-04 | — | (user's own) | Assumptions unverified |

Reliability tiers: **High** (primary/official/peer-reviewed), **Medium** (credible secondary, single-sourced), **Low** (social, anonymous, commercially incentivized, undated). Internal user files are treated as authoritative for *the user's own position and data* but their external claims still need cross-validation.

## 2. Layer 0 — Intake & Mode

- Enumerate sources: list `/mnt/user-data/uploads`; for each file pick the right reader (text/CSV → `view`/`bash_tool`; PDF → pdf skill; Word → docx skill; spreadsheet → xlsx skill). If the user references Drive or Notion content, load that connector via `tool_search` and pull it.
- Determine the external research scope (the questions the web needs to answer).
- Detect output language (default Turkish; honor any explicit request).
- Choose the mode (Pure Research / Pure Synthesis / Hybrid) and say so in one line.
- Open the Source Registry with everything known so far.

## 3. Layer 1 — Global Holistic Synthesis

Resist the urge to decompose immediately. First read/skim everything and answer: *what is this whole body of material collectively about, and what is the single through-line?* Write a compact **Master Knowledge Base** — a few paragraphs capturing the shared factual ground and the big-picture narrative. Everything downstream refers back to this so the phases stay coherent instead of becoming disconnected mini-reports.

## 4. Layer 2 — Phase Decomposition

Break the topic into **3–8 phases** — the logical units the report is organized around. Choose the decomposition that fits the material:
- **Thematic** (e.g. fundamentals / technicals / sentiment / macro)
- **Temporal** (past → present → outlook)
- **Value-chain or structural** (supply → production → demand)
- **Question-driven** (one phase per sub-question the user posed)

If the user defined phases, use theirs. For each phase, **consolidate** what the sources say — this is still synthesis, not analysis. Use tables for anything comparative (companies, options, time periods, scenarios); prose buries comparisons that a table makes obvious.

## 5. Layer 3 — Deep Research & Cross-Validation

Where a phase is thin, stale, or contested, run targeted external research per `research-playbook.md`. Cross-validate the load-bearing internal and external claims. Fold every new source into the Registry with its reliability tier. Enforce currency here: for anything that moves, confirm the latest state.

## 6. Layer 4 — Analysis

Only after the synthesis is on the page do you interpret. Two passes:
- **Intra-phase:** within each phase, what do the consolidated facts imply? Risks, drivers, anomalies.
- **Inter-phase:** across phases, what patterns, tensions, and second-order effects emerge that no single source states? This emergent layer is where the report earns its keep.

Guard the boundary: analysis must cite the synthesized facts it rests on. If an interpretation has no grounding in Layers 1–3, it's speculation — either ground it or drop it.

## 7. Conflict resolution framework

When sources disagree, never silently average or pick the convenient one. Resolve explicitly:

1. **State the conflict** — who claims what.
2. **Weigh the sources** — recency, primary vs. secondary, reliability tier, and incentive/bias.
3. **Resolve** — state which you favor and *why* (e.g. "the 2026 audited filing over the 2024 news estimate").
4. **Assign confidence** to the resolution, and if it stays genuinely unresolved, say so and present both with the tradeoff.

In the report, show material conflicts rather than hiding them — a transparently resolved disagreement is more trustworthy than false unanimity.

## 8. Confidence scoring

Tag major conclusions:
- **High** — corroborated across independent High-reliability sources.
- **Medium** — single credible source, or good sources with minor tension.
- **Low** — thin, social-only, or heavily inferred.

List a short **Gaps & Unknowns** set: what you could not verify and what source would settle it. Honest gaps are a feature — they tell the user exactly where to look next, and they keep the report from projecting false certainty.
