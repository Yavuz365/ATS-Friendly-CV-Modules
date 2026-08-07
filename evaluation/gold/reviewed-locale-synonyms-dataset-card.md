# Reviewed Locale Synonym Dictionary (TR/EN) — v0.1.0

## Purpose (MAT-002)

`matching.match_term()`'s SYNONYM stage had a revision-hashed *interface*
(`reviewed_synonyms`/`reviewed_synonym_revision`) but no accepted, versioned
dataset behind it, and no record of which candidate pairs were reviewed and
rejected. This is that dataset.

## Review method

Each accepted pair was checked for genuine equivalence — not just frequent
co-occurrence in job postings — before inclusion. Each **abstained** (rejected)
candidate pair is recorded with a reason, so a future reviewer does not
re-propose it without new evidence (mirrors the Claim Conflict Registry
pattern used elsewhere in this repository).

## Scope (v0.1.0)

- 11 accepted TR→EN canonical pairs (foreign-trade/logistics + education +
  language domain, matching this engine's existing `foreign-trade-logistics`
  domain pack).
- 3 explicitly abstained candidate pairs with reasons (SAP≠ERP,
  gümrük≠lojistik, yüksek lisans≠PhD).

## Conflict audit

`locale_synonym_registry.audit_reviewed_synonym_conflicts()` verifies no
variant string is claimed by two different canonical keys, and no canonical
key also appears as someone else's variant. **Result on this dataset: 0
conflicts** (verified by `test_locale_synonym_registry.py`).

## Known limits

- n=11 accepted pairs — a starting reviewed set, not exhaustive domain
  coverage.
- TR/EN only (matches this repository's validated-locale scope, CCR-025).
- Does not measure downstream match precision/recall on a labelled CV
  corpus — see `evaluation/gold/exact_match_support_labels.json` (MAT-001)
  for that kind of measurement on the EXACT stage.

## Privacy

Fully synthetic terminology list. No personal data.
