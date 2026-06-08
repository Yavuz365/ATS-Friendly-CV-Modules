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
