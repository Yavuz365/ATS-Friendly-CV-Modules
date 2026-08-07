"""MAT-001: link a requirement term match to a concrete evidence locator.

``match_term()`` establishes *whether* a term has an exact/synonym/ontology/
semantic boundary hit; it does not, by itself, produce the evidence-first
:class:`~ats_engine.contracts.EvidenceRecord`/:class:`~ats_engine.contracts.RequirementEvidenceMap`
pair that points at *where in the source text* that hit occurred. Those two
contracts existed but had no producer — this module is that producer.

Per CCR-018/STAB-019, a lexical boundary match is a *support signal*, not a
factual verification: linking a match to a locator never promotes
``verification_status`` past ``UNVERIFIED`` on its own.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .contracts import EvidenceRecord, JobRequirement, RequirementEvidenceMap, VerificationStatus
from .matching import MatchStage, TermMatch, _pattern, match_term
from .text import tr_lower

_EXCERPT_RADIUS = 40


def _first_locator(term: str, text: str) -> tuple[str, str] | None:
    """Return ``(locator, excerpt)`` for the first Unicode-boundary occurrence of ``term`` in ``text``.

    The locator is a stable ``char:<start>-<end>`` offset into the exact
    ``text`` passed in (case-insensitive search, original-case excerpt).
    """
    normalized = tr_lower(term).strip()
    if not normalized:
        return None
    match = _pattern(normalized).search(tr_lower(text))
    if match is None:
        return None
    start, end = match.start(), match.end()
    locator = f"char:{start}-{end}"
    lo = max(0, start - _EXCERPT_RADIUS)
    hi = min(len(text), end + _EXCERPT_RADIUS)
    excerpt = text[lo:hi].strip()
    return locator, excerpt


def _stable_evidence_id(requirement_id: str, term: str, source_artifact_id: str, locator: str) -> str:
    digest = hashlib.sha256(f"{requirement_id}\0{term}\0{source_artifact_id}\0{locator}".encode()).hexdigest()[:16]
    return f"EV-{digest}"


def link_requirement_evidence(
    requirement: JobRequirement,
    term: str,
    cv_text: str,
    *,
    source_artifact_id: str,
    candidate_fact_id: str,
    **match_term_kwargs: object,
) -> tuple[RequirementEvidenceMap, TermMatch, EvidenceRecord | None]:
    """Link one requirement's term match to a locator-bearing evidence record.

    Returns the ``RequirementEvidenceMap`` (always produced, even on no
    match — with an empty ``evidence_ids`` list and an honest reason), the
    underlying ``TermMatch`` used to decide it, and the ``EvidenceRecord``
    itself (``None`` when there is no match to point at).

    ``verification_status`` is capped at ``PARTIAL`` for a real boundary hit
    (EXACT/SYNONYM) and ``UNVERIFIED`` for a review-required adapter hit
    (ONTOLOGY/SEMANTIC) or no hit at all — a lexical/adapter match is a
    support signal, never a factual verification on its own (CCR-018).
    """
    tm = match_term(term, cv_text, **match_term_kwargs)  # type: ignore[arg-type]

    if not tm.matched:
        return (
            RequirementEvidenceMap(
                requirement_id=requirement.id,
                evidence_ids=[],
                verification_status=VerificationStatus.UNVERIFIED,
                reason=f"'{term}' için CV metninde eşleşme bulunamadı: {tm.explanation}",
            ),
            tm,
            None,
        )

    located = _first_locator(tm.matched_variant or term, cv_text)
    if located is None:
        # Adapter-only match (ontology/semantic) may not correspond to a
        # literal substring in cv_text (e.g. embedding similarity) — still
        # honestly report the match without inventing a locator.
        return (
            RequirementEvidenceMap(
                requirement_id=requirement.id,
                evidence_ids=[],
                verification_status=VerificationStatus.UNVERIFIED,
                reason=(
                    f"'{term}' {tm.stage.value} aşamasında eşleşti ancak CV metninde "
                    "doğrudan bir karakter konumu (locator) bulunamadı; insan incelemesi gerekir."
                ),
            ),
            tm,
            None,
        )

    locator, excerpt = located
    evidence = EvidenceRecord(
        id=_stable_evidence_id(requirement.id, term, source_artifact_id, locator),
        candidate_fact_id=candidate_fact_id,
        source_artifact_id=source_artifact_id,
        locator=locator,
        excerpt=excerpt,
        verification_status=(
            VerificationStatus.PARTIAL
            if tm.stage in (MatchStage.EXACT, MatchStage.SYNONYM)
            else VerificationStatus.UNVERIFIED
        ),
    )
    verification_status = (
        VerificationStatus.PARTIAL
        if tm.stage in (MatchStage.EXACT, MatchStage.SYNONYM)
        else VerificationStatus.UNVERIFIED
    )
    reason = (
        f"'{term}' {tm.stage.value} aşamasında '{locator}' konumunda bulundu; "
        "lexical eşleşme kanıt sinyalidir, tek başına doğrulama değildir."
    )
    return (
        RequirementEvidenceMap(
            requirement_id=requirement.id,
            evidence_ids=[evidence.id],
            verification_status=verification_status,
            reason=reason,
        ),
        tm,
        evidence,
    )


def measure_exact_match_false_support_rate(gold_path: str | Path) -> dict[str, Any]:
    """Measure how often a naive EXACT boundary match is a FALSE support signal.

    MAT-001: "canonical requirement/evidence locator linkage plus a measured
    false-support gold rate". This runs the real ``match_term`` cascade
    against a small, versioned, synthetic gold set (see
    ``evaluation/gold/exact_match_support_labels.json``) and reports, among
    the gold cases labelled ``true_support=False`` (the term is present but
    does not reflect genuine candidate experience — negated, aspirational,
    third-party, a future plan, or pasted job-posting text), what fraction
    the matcher still reports as ``matched=True``. That fraction is the
    measured false-support rate: it is a known, honest limitation
    (lexical/boundary matching cannot see negation, tense, or authorship —
    see CCR-018/STAB-019), not a claim that the matcher is broken.

    This is a tiny, non-statistically-powered synthetic sample (see the
    dataset card); the returned rate must never be presented as a validated,
    general-purpose error rate for the matcher.
    """
    path = Path(gold_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    labels: list[dict[str, Any]] = data["labels"]

    rows: list[dict[str, Any]] = []
    for label in labels:
        tm = match_term(label["term"], label["cv_text"], allow_fuzzy=False)
        rows.append(
            {
                "fixture_id": label["fixture_id"],
                "term": label["term"],
                "true_support": label["true_support"],
                "matcher_matched": tm.matched,
                "matcher_stage": tm.stage.value,
                "is_false_support_error": (not label["true_support"]) and tm.matched,
            }
        )

    negative_gold = [r for r in rows if not r["true_support"]]
    positive_gold = [r for r in rows if r["true_support"]]
    false_support_errors = [r for r in negative_gold if r["is_false_support_error"]]
    true_positive_hits = [r for r in positive_gold if r["matcher_matched"]]

    false_support_rate = (len(false_support_errors) / len(negative_gold)) if negative_gold else None
    true_positive_recall = (len(true_positive_hits) / len(positive_gold)) if positive_gold else None

    return {
        "dataset_id": data.get("dataset_id"),
        "dataset_version": data.get("dataset_version"),
        "sample_size": len(rows),
        "negative_gold_count": len(negative_gold),
        "positive_gold_count": len(positive_gold),
        "false_support_rate": false_support_rate,
        "false_support_errors": [r["fixture_id"] for r in false_support_errors],
        "true_positive_recall": true_positive_recall,
        "rows": rows,
        "limitation": (
            f"Tiny synthetic sample (n={len(rows)}); not a statistically powered or "
            "commercially validated error rate. Measures a known limitation: "
            "boundary matching cannot see negation, tense, or authorship."
        ),
    }
