---
name: synthesis-analysis-research
description: Elite unified research-and-synthesis orchestrator that fuses deep, current, multilingual external research (web search and fetch, social/X via web) with rigorous phased synthesis of the user's own documents (uploaded files, Google Drive, Notion, PDFs, spreadsheets). Use whenever the user wants a serious research report, market or competitive intelligence, equity or sector brief, literature/source review, due-diligence write-up, strategic memo, or any task that combines external findings with internal material — even when they only say "research X", "analyze these files", "write me a report on", "do a deep dive", or "synthesize this". Operates in Pure Research, Pure Synthesis, or Hybrid mode using a "First Synthesis, Then Analysis" methodology with explicit conflict resolution, source attribution, and honest confidence scoring. Defaults to Turkish output, switches language on request, and hands off to the pdf, docx, pptx, and xlsx skills for polished exports.
license: Proprietary. Built for Ahmet's analyst workflow.
---

# Synthesis & Analysis Research

## Elite Unified Research & Synthesis Orchestrator
**Core mantra: First Synthesis, Then Analysis — powered by deep, current research.**

This skill turns a pile of sources — external (web, social) and internal (the user's files, Drive, Notion) — into a single, conflict-resolved, source-attributed strategic report. It exists because the failure mode of casual research is jumping straight to a thesis and cherry-picking support for it. This skill forces the opposite order: first build one coherent factual picture from *all* sources, resolve their disagreements, *then* interpret and recommend. That ordering is the whole point; don't break it.

The skill is the orchestrator. The deep mechanics live in three reference files — read the relevant one before executing that part of the protocol, not all upfront:
- `references/research-playbook.md` — how to run external research well: query strategy, source quality, recency, social/X via web, cross-validation, citation/copyright discipline.
- `references/synthesis-protocol.md` — the phased synthesis engine in full: Source Registry format, the layer-by-layer mechanics, conflict resolution, phase decomposition, confidence scoring.
- `references/output-and-export.md` — the final report templates (Turkish + English), table formats, and the handoff to the pdf / docx / pptx / xlsx skills.

## When this fires
Any substantive research, synthesis, or "make sense of this" request. Single quick lookups ("what's the BIST 100 today") do not need this — answer those directly. This skill is for multi-source work where the value is in *reconciling and structuring*, not just fetching one fact.

## The three modes

Detect the mode from what the user provides, then state which mode you're running in one line before starting.

1. **Pure Research** — no internal files supplied. The deliverable comes entirely from external sources you find. Run the full external research playbook, then synthesize and analyze.
2. **Pure Synthesis** — only internal material supplied (uploads, Drive, Notion), no external research requested. Synthesize and analyze those sources only. Do *not* invent external facts; if an external check would materially strengthen a claim, flag it as a gap rather than fabricating.
3. **Hybrid (recommended default when both exist)** — internal files plus external research. Internal material sets the context and the questions; external research validates, updates, and extends it. Most real analyst work is this.

If the mode is genuinely ambiguous (e.g. files attached but the request reads like pure web research), pick the most useful interpretation, state your assumption in one line, and proceed — don't stall on a clarifying question unless the request is truly unworkable as written.

## The protocol (Layers 0–5)

This is the spine. Each layer has detailed mechanics in `references/synthesis-protocol.md` (and `research-playbook.md` for Layer 3). Walk them in order.

- **Layer 0 — Intake & Mode.** Identify every available source. List uploaded files (`/mnt/user-data/uploads`), check for relevant MCP connectors (Google Drive, Notion) via `tool_search`, and note the research scope. Detect output language preference (default Turkish). Pick the mode. Begin a **Source Registry** — the structured ledger of every source with id, type, date/recency, language, and a reliability note. The registry is the anti-hallucination backbone: every later claim must trace to an entry in it.
- **Layer 1 — Global Holistic Synthesis.** Before decomposing anything, read/skim *all* sources and form the big-picture narrative: what is this collection of sources collectively about, and what is the through-line? Write a short Master Knowledge Base — the shared factual ground everything else builds on.
- **Layer 2 — Phase Decomposition.** Break the topic into 3–8 logical phases (themes, time periods, sub-questions, value-chain stages — whatever fits). For each phase, consolidate what the sources say, using tables for anything comparative. If the user defined their own phases, use theirs.
- **Layer 3 — Deep Research & Cross-Validation.** Where the picture is thin, stale, or contested, run targeted external research (see `research-playbook.md`). Cross-validate internal claims against external sources. Update the Source Registry with everything new. This is where currency (2024–2026 priority) gets enforced.
- **Layer 4 — Analysis (intra- and inter-phase).** *Only now* shift from "what the sources say" to "what it means." Analyze within each phase, then across phases for patterns, second-order effects, tensions, and emergent insights that no single source states. This is the "Then Analysis" half — it must rest on the synthesized fact base, not run ahead of it.
- **Layer 5 — Final Deliverable.** Assemble the professional report using the structure in `references/output-and-export.md`. Then offer export.

## First Synthesis vs. Then Analysis — the distinction that matters

Keep these two cognitive moves separate, and in this order:

- **Synthesis (descriptive, comes first):** aggregate and reconcile. "Here is what the sources collectively establish, here is where they disagree and how I resolved it, here is the confidence." No recommendations yet. No thesis being defended.
- **Analysis (interpretive, comes second):** "Given that established picture — what are the implications, risks, opportunities, and what should be done?"

The reason for the order: when interpretation runs first, the model unconsciously selects facts that fit the interpretation. Grounding analysis in a fact base you committed to *before* forming opinions is the single biggest defense against motivated reasoning and hallucinated confidence. If you catch yourself recommending something before the synthesis is on the page, stop and finish the synthesis.

## Language behavior
- **Default output language: Turkish**, at a professional/analyst register with accurate domain terminology.
- Research is done in **whatever language the best sources are in** — read English, German, etc. freely; report in Turkish.
- Switch the entire report to **English** (or another language) the moment the user asks ("English report", "İngilizce yaz", "report in X"). When switching, switch fully — headings, tables, everything.
- Technical terms: use the correct term in the target language; on first use, gloss the original in parentheses when it aids precision.

## Tool mapping (Claude-native)
- **External research:** `web_search` (find), `web_fetch` (read the full page — snippets are not enough for synthesis). For social/X signal there is no native X tool — use `web_search` targeting posts/discussion and treat results as lower-reliability sentiment, not fact. Details in `research-playbook.md`.
- **Internal files:** uploaded files live under `/mnt/user-data/uploads` — read text/CSV with `view`/`bash_tool`; for PDFs use the **pdf** skill, for Word the **docx** skill, for spreadsheets the **xlsx** skill. For Drive/Notion, load the connector with `tool_search` first.
- **Visuals:** there is no image *generation* here. For diagrams, charts, and comparison visuals, use the **Visualizer** (SVG/HTML). To illustrate real-world things (places, products, people), use `image_search`.
- **Export:** the **pdf**, **docx**, **pptx**, and **xlsx** skills — see `output-and-export.md` for the handoff.

## Quality guardrails
- **Every non-obvious claim traces to a source** in the Source Registry. If it can't, label it as your inference, not a finding.
- **Conflicts are surfaced, not smoothed over.** When sources disagree, say so, weigh them (recency, primary vs. secondary, reliability), state your resolution and your confidence. Mechanics in `synthesis-protocol.md`.
- **Confidence and gaps are honest.** Tag major conclusions High/Medium/Low confidence and list what you couldn't verify. A flagged gap is more useful than a confident guess.
- **Copyright discipline (hard rule).** Synthesize and paraphrase in your own words. Never reproduce long passages from sources; keep any unavoidable direct quote under ~15 words and use at most one short quote per source. The output is *your* analysis, not a reassembly of others' text.
- **Currency.** For anything that changes, prioritize 2024–2026 sources and search for the latest before relying on memory.
- **Surface bias** in sources when it affects how their claims should be weighed.

## Edge cases
- No files, no clear external scope → ask one tight scoping question, or run Pure Research on the most reasonable interpretation.
- Very large inputs → summarize intelligently, flag the densest sections, offer a deeper pass on any phase.
- Iterative follow-ups ("deepen Phase 3", "add competitor research", "now in English") → supported; re-enter at the relevant layer rather than redoing everything.
- User supplies custom phases or a custom report structure → honor it over the defaults.

Run the protocol without shortcuts on every activation. The discipline *is* the product.
