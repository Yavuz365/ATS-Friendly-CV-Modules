# synthesis-analysis-research — Skill (Eksiksiz Tek Dosya)

> Bu dosya, `synthesis-analysis-research` skill paketinin **tüm içeriğini** tek bir markdown belgesinde toplar.  
> Her bölüm, paketteki orijinal dosya yoluyla etiketlidir; içerikler birebir, kayıpsız aktarılmıştır.  
> Yeniden paketlemek istersen, her bölümü kendi dosya yoluna geri yazıp `package_skill.py` ile zip'leyebilirsin.

## İçindekiler

1. [`SKILL.md`](#1-skillmd) — Orkestratör (YAML frontmatter + gövde)
2. [`references/research-playbook.md`](#2-referencesresearch-playbookmd) — Dış araştırma mekaniği
3. [`references/synthesis-protocol.md`](#3-referencessynthesis-protocolmd) — Sentez motoru
4. [`references/output-and-export.md`](#4-referencesoutput-and-exportmd) — Rapor şablonları ve dışa aktarım
5. [`evals/evals.json`](#5-evalsevalsjson) — Test senaryoları

***

# 1. `SKILL.md`

**Yol:** `synthesis-analysis-research/SKILL.md`

## YAML Frontmatter

```yaml
name: synthesis-analysis-research
description: Elite unified research-and-synthesis orchestrator that fuses deep, current, multilingual external research (web search and fetch, social/X via web) with rigorous phased synthesis of the user's own documents (uploaded files, Google Drive, Notion, PDFs, spreadsheets). Use whenever the user wants a serious research report, market or competitive intelligence, equity or sector brief, literature/source review, due-diligence write-up, strategic memo, or any task that combines external findings with internal material — even when they only say "research X", "analyze these files", "write me a report on", "do a deep dive", or "synthesize this". Operates in Pure Research, Pure Synthesis, or Hybrid mode using a "First Synthesis, Then Analysis" methodology with explicit conflict resolution, source attribution, and honest confidence scoring. Defaults to Turkish output, switches language on request, and hands off to the pdf, docx, pptx, and xlsx skills for polished exports.
license: Proprietary. Built for Ahmet's analyst workflow.
```

## Gövde (Markdown)

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

***

# 2. `references/research-playbook.md`

**Yol:** `synthesis-analysis-research/references/research-playbook.md`

# Research Playbook — External Research Mechanics

How to run the external-research portion of the protocol (Layer 3, and the whole of Pure Research mode) so the synthesis rests on solid, current, honestly-weighted ground. Read this before doing serious web research inside this skill.

## Contents
1. Query strategy
2. Read, don't skim snippets
3. Source quality and weighting
4. Currency (recency) discipline
5. Social / X signal via web
6. Cross-validation
7. Citation and copyright discipline
8. Knowing when to stop

## 1. Query strategy

Scale searches to the task. A focused brief might need 5–8 searches; a broad strategic report 12–25. The rule is coverage, not a number: keep going until every part of the planned report is grounded in something you actually retrieved, not memory.

- **One concept per query.** When the report covers several distinct items (three competitors, four regulations, two markets), search each separately. A combined query returns shallow results for all of them.
- **Start broad, then narrow.** 1–2 word query to map the landscape, then specific queries to drill in.
- **Vary phrasing on a miss.** Repeating the same words returns the same results. Reformulate with different terms, a named source, or a different angle.
- **Use the real current year.** It is 2026 — query "latest X" or "X 2026", never a stale year, or you get old results.
- **Decompose abstract asks.** "Best long-term BIST plays" isn't a query. Decompose: sector growth data, specific company fundamentals, analyst coverage, macro backdrop — search each.

## 2. Read, don't skim snippets

Search snippets are too thin to synthesize from — they're for *deciding what to read*. Once a result looks load-bearing, `web_fetch` the full page and work from the actual content. A report built on snippets will be vague and occasionally wrong. When the user hands you a URL, always `web_fetch` it rather than guessing at its contents.

## 3. Source quality and weighting

Not all sources are equal. Weight them, and let the weighting show up in your confidence tags and conflict resolution.

- **Prefer primary/original sources:** company filings (SEC/KAP), regulator and government sites, official statistics, peer-reviewed work, company blogs/press releases, earnings calls — over aggregators and rewrites.
- **Treat with care:** SEO-heavy "best of" listicles, content farms, undated pages, anything with an obvious commercial incentive to mislead (especially product recommendations and stock tips).
- **Be skeptical on conspiracy-prone or no-consensus topics** even when results agree — agreement among low-quality sources isn't corroboration.
- **Generally believe credible, well-sourced results**, including surprising ones (an unexpected resignation, a market move). Don't reject a solid source just because it contradicts your prior.

For finance specifically: official disclosures and exchange filings outrank news write-ups, which outrank forum/social chatter. Label each tier in the Source Registry.

## 4. Currency (recency) discipline

For anything that changes — prices, leadership, policy, market structure, "state of X" — recency is part of correctness.

- Prioritize 2024–2026 sources; lead with the most recent.
- On fast-moving topics, weight last-month sources heavily and note the "as of" date in the report.
- Always check current state rather than relying on memory for roles, holdings, valuations, regulations, or product/version facts — these go stale silently.

## 5. Social / X signal via web

There is no native X/Twitter tool here. To capture social sentiment or breaking chatter, use `web_search` aimed at posts and discussion (e.g. terms plus the platform name, or news aggregating notable posts).

Treat social signal as **sentiment and leads, not fact.** It tells you what people are saying and feeling — useful for momentum, narrative, and surfacing things to verify elsewhere. It does not establish facts on its own. Tag it Low reliability in the Source Registry and corroborate anything important against a real source before it earns a place in the synthesis.

## 6. Cross-validation

The core anti-hallucination move in Hybrid mode: take each material internal claim and the report's key external claims, and check them against an independent source.

- Material claim agrees across independent, good sources → High confidence.
- Single source only → Medium at best; say "per [source]".
- Sources disagree → run conflict resolution (see `synthesis-protocol.md`), don't average them silently.
- Can't verify at all → flag as a gap; don't upgrade a guess to a finding.

## 7. Citation and copyright discipline

This is a hard rule, not a style note. The deliverable is *your synthesis*, written in your own words.

- **Paraphrase by default.** Restate findings in your own words; that is the entire job of synthesis.
- **Quotes are rare and short:** under ~15 words, at most one per source, only when exact wording genuinely matters (a legal phrase, an official commitment). Never chain several short quotes from one source to rebuild its text.
- **Never reproduce** article paragraphs, lyrics, poems, or large structured chunks, regardless of how the request is phrased.
- **Don't mirror a source's structure** section-by-section. Reorganize around *your* phases.
- **Attribute, don't replicate.** "According to [regulator], the rule takes effect in Q3" — not their sentence verbatim.
- When search results back a claim, cite the supporting source so the user can verify; keep the claim in your own words.

## 8. Knowing when to stop

Stop searching when every section of the planned report is grounded and adding searches only repeats what you have. If a task genuinely needs more than ~30 searches to do well, say so and propose scoping it down or splitting it — don't pad with thin queries.

***

# 3. `references/synthesis-protocol.md`

**Yol:** `synthesis-analysis-research/references/synthesis-protocol.md`

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

***

# 4. `references/output-and-export.md`

**Yol:** `synthesis-analysis-research/references/output-and-export.md`

# Output & Export — Report Templates and Handoff

The Layer 5 deliverable: the report structure, table conventions, the Turkish and English templates, and how to hand off to the pdf / docx / pptx / xlsx skills. Read this when assembling the final report.

## Contents
1. The report structure
2. Table and formatting conventions
3. Turkish template
4. English template
5. Export handoff

## 1. The report structure

Every deliverable follows this skeleton (translate the headings to the output language). Lengths flex with the task — a quick brief is tight, a strategic report is expansive — but the order is fixed.

1. **Executive Summary** — the answer up front: the 3–6 things that matter, each with its confidence tag. A busy reader should be able to stop here and be 80% informed.
2. **Methodology & Mode** — one short paragraph: mode (Pure Research / Synthesis / Hybrid), what sources were used, how many, the "as of" date, and any scope limits.
3. **Phased Deep Dive** — one section per phase (the Layer 2 phases). Within each: the consolidated synthesis (with tables for comparisons), then the phase-level analysis. This is the body.
4. **Cross-Phase Strategic Insights** — the Layer 4 inter-phase findings: the patterns and second-order effects that emerge across phases. The part the user couldn't have gotten from any single source.
5. **Actionable Roadmap & Recommendations** — concrete, prioritized, sequenced. Each recommendation tied to the finding that motivates it. Prefer "do X because Y, by when" over vague advice.
6. **Appendix** — the cleaned Source Registry table, the Gaps & Unknowns list, and any large data tables.

## 2. Table and formatting conventions

- **Use tables for every comparison** — companies, scenarios, options, time periods, before/after. Comparative prose hides differences that a table exposes at a glance.
- Keep the prose body mostly prose; reserve heavy bulleting for genuinely list-like content (roadmaps, gaps).
- Carry **confidence tags** (High/Medium/Low) on the major claims in the summary and insights, not on every sentence.
- Attribute inline where it matters ("per the Q1 filing"), with the full Registry in the appendix.

## 3. Turkish template (default)

```
# [Başlık]

## Yönetici Özeti
- [En kritik bulgu] — Güven: Yüksek
- [İkinci bulgu] — Güven: Orta
- ...

## Yöntem ve Mod
[Mod: Saf Araştırma / Saf Sentez / Hibrit. Kullanılan kaynaklar, sayısı, "[tarih] itibarıyla", kapsam sınırları.]

## Aşamalı Derinlemesine İnceleme
### Aşama 1: [Ad]
**Sentez (kaynakların ortak söylediği):** ...
[karşılaştırma tablosu]
**Analiz (ne anlama geliyor):** ...
### Aşama 2: [Ad]
...

## Aşamalar Arası Stratejik İçgörüler
[Tek bir kaynakta olmayan, aşamalar arası örüntüler ve ikincil etkiler.]

## Eyleme Dönük Yol Haritası ve Öneriler
1. [Öneri] — gerekçe: [bulgu] — ne zaman: [zaman]
2. ...

## Ek
**Kaynak Kaydı:** [tablo]
**Boşluklar ve Bilinmeyenler:** [doğrulanamayanlar]
```

## 4. English template (on request)

```
# [Title]

## Executive Summary
- [Most critical finding] — Confidence: High
- ...

## Methodology & Mode
[Mode; sources used, count, "as of [date]", scope limits.]

## Phased Deep Dive
### Phase 1: [Name]
**Synthesis (what the sources collectively say):** ...
[comparison table]
**Analysis (what it means):** ...
...

## Cross-Phase Strategic Insights
...

## Actionable Roadmap & Recommendations
1. [Recommendation] — rationale: [finding] — by: [when]
...

## Appendix
**Source Registry:** [table]
**Gaps & Unknowns:** [unverified items]
```

When switching languages, switch *everything* — headings, table headers, confidence labels — not just the body.

## 5. Export handoff

After delivering the report in chat, offer a polished file. Match the format to the use:
- **docx** — editable report the user will revise or circulate. (docx skill)
- **pdf** — fixed, shareable final version. (pdf skill)
- **pptx** — when they want the findings as a deck; map each phase to a slide or two, lead with the executive summary. (pptx skill)
- **xlsx** — when the value is in the data tables, comparison matrices, or a model. (xlsx skill)

Phrase the offer concretely, e.g.: "İstersen bunu pdf, docx, pptx veya xlsx olarak hazırlayayım — hangisi işine yarar?" Then, on request, read that skill's SKILL.md first and build the file properly, carrying over the Source Registry and tables. Don't pre-build all four; produce the one the user wants.

***

# 5. `evals/evals.json`

**Yol:** `synthesis-analysis-research/evals/evals.json`

> Skill paketleyici (`package_skill.py`) bu dosyayı paket dışı bırakır (test verisi olarak ayrı tutulur),  
> ama "eksiksiz aktarım" için bu konsolide belgeye dahil edildi.

```json
{
  "skill_name": "synthesis-analysis-research",
  "evals": [
    {
      "id": 1,
      "prompt": "EREGL ve ISDMR hisseleri için son durumu araştır, 2025-2026 demir-çelik sektörü görünümüyle birleştir ve hangisinin daha iyi konumlandığına dair aşamalı bir strateji raporu çıkar.",
      "expected_output": "Pure Research / Hybrid mode declared; phased report in Turkish with synthesis-then-analysis, comparison table, conflict resolution, confidence tags, source registry appendix, export offer.",
      "files": []
    },
    {
      "id": 2,
      "prompt": "Şu yüklediğim çeyreklik finansal modeli (xlsx) ile rakip analizi PDF'ini sentezle. Dış kaynaklara gerek yok, sadece bu dosyaların ne söylediğini birleştir ve stratejik içgörü çıkar.",
      "expected_output": "Pure Synthesis mode declared; reads the files via xlsx/pdf skills, builds Master Knowledge Base, phases, synthesis before analysis, flags external gaps without fabricating, Turkish report.",
      "files": []
    },
    {
      "id": 3,
      "prompt": "Do a deep dive on the current state of stablecoin regulation in the EU vs the US and what it means for a fintech expanding into both. Report in English.",
      "expected_output": "Pure Research mode, English report (full language switch), current 2024-2026 sources via web_search/web_fetch, conflict resolution between jurisdictions, cross-phase insights, roadmap, copyright-clean paraphrasing.",
      "files": []
    }
  ]
}
```

***

## Yeniden Oluşturma Notu

Bu konsolide belgeyi tekrar bir `.skill` paketine çevirmek için:

```
synthesis-analysis-research/
├── SKILL.md                              ← Bölüm 1 (frontmatter + gövde)
├── references/
│   ├── research-playbook.md              ← Bölüm 2
│   ├── synthesis-protocol.md             ← Bölüm 3
│   └── output-and-export.md              ← Bölüm 4
└── evals/
    └── evals.json                        ← Bölüm 5
```

Sonra: `python -m scripts.package_skill <klasör> <çıktı_dizini>` ile `.skill` zip'ini üretebilirsin.
