# Exact-Match False-Support Gold Set — v0.1.0

## Purpose (MAT-001)

`match_term()`'s EXACT/SYNONYM stages establish that a term has a real Unicode
word-boundary occurrence in a CV text. They cannot see negation, tense,
authorship, or intent — a boundary match is a **support signal**, never a
factual verification (CCR-018/STAB-019). This gold set measures, on a small
synthetic sample, how often that gap actually produces a false support signal
versus a genuine one, using `evidence_linking.measure_exact_match_false_support_rate()`.

This is a **research evaluation fixture**, not a commercial accuracy benchmark.

## Scope (v0.1.0) — 12 fixtures, TR + EN

| Fixture ID | True support? | Failure mode being probed |
|---|---|---|
| `SUP-TR-TRUE-001`, `SUP-EN-TRUE-001`, `SUP-EN-TRUE-002`, `SUP-TR-TRUE-002`, `SUP-EN-TRUE-COURSEWORK-001` | yes | genuine first-person claimed experience (no failure expected) |
| `SUP-TR-FALSE-NEGATION-001`, `SUP-EN-FALSE-NEGATION-001` | no | explicit negation ("no SAP experience") |
| `SUP-TR-FALSE-ASPIRATIONAL-001` | no | future intent, not existing experience |
| `SUP-TR-FALSE-THIRDPARTY-001` | no | someone else's (manager's) experience |
| `SUP-TR-FALSE-FUTUREPLAN-001` | no | a company plan, not the candidate's experience |
| `SUP-TR-FALSE-PASTEDJD-001` | no | job-posting requirements text pasted into a CV |
| `SUP-EN-FALSE-COURSEWORK-001` | no | academic exposure explicitly framed as never used professionally |

## Measured result (this repository, this commit)

Run `measure_exact_match_false_support_rate("evaluation/gold/exact_match_support_labels.json")`:

- **False-support rate: 7/7 = 100%** of the 7 negative-gold cases (negation,
  aspirational, third-party, future-plan, pasted-JD, unused-coursework) still
  register as `matched=True` at the `EXACT` stage.
- **True-positive recall: 5/5 = 100%** of the 5 positive-gold cases matched.

## Interpretation

This is a real, measured confirmation of a known, already-documented
limitation (CCR-018/STAB-019): plain Unicode-boundary term matching has **no
negation, tense, or authorship awareness on the CV side** (JD-side negation
*is* handled separately by `job_requirements.py`'s `_NEGATION_RE`). A 100%
false-support rate on this adversarial sample does not mean the matcher is
"broken" for its stated purpose (a coverage/support signal) — it means the
existing "lexical overlap is not factual verification" warnings on
`match_term`/QA output are load-bearing and must stay visible to any human
reviewer, not decorative.

## Known limits

- n=12, hand-authored, **not statistically powered** — do not extrapolate a
  general-purpose error rate from this sample.
- Only probes English/Turkish sentence-level negation/authorship patterns
  explicitly designed to trigger the gap; it is not a random sample of real
  CVs.
- Does not measure the SYNONYM/ONTOLOGY/SEMANTIC cascade stages separately.
- Fully synthetic: no real employer names, candidate data, or job postings.

## Privacy

Fully synthetic. No personal data.
