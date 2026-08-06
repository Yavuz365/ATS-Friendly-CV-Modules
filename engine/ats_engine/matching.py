"""One explainable term-matching contract for counts, coverage, and gaps."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum

from . import lexicons
from .text import tr_lower


class MatchStage(str, Enum):
    EXACT = "EXACT"
    SYNONYM = "SYNONYM"
    ONTOLOGY = "ONTOLOGY"
    SEMANTIC = "SEMANTIC"
    FUZZY = "FUZZY"  # legacy alias retained for existing consumers
    HUMAN_REVIEW = "HUMAN_REVIEW"
    NONE = "NONE"


class AdapterStatus(str, Enum):
    MATCH = "MATCH"
    NO_MATCH = "NO_MATCH"
    NOT_RUN = "NOT_RUN"
    ERROR = "ERROR"


@dataclass(frozen=True)
class TermMatch:
    term: str
    matched: bool
    stage: MatchStage
    matched_variant: str | None
    count: int
    explanation: str
    adapter_id: str | None = None
    adapter_version: str | None = None
    adapter_revision: str | None = None
    confidence: float | None = None
    review_required: bool = False


@dataclass(frozen=True)
class AdapterResult:
    status: AdapterStatus
    matched_variant: str | None = None
    confidence: float | None = None
    explanation: str = ""


@dataclass(frozen=True)
class VersionedMatchAdapter:
    """A revision-pinned optional matching adapter.

    ``matcher`` receives normalized term and raw text. The revision must identify
    the immutable data/model snapshot; floating names such as ``latest`` are rejected.
    """

    adapter_id: str
    version: str
    revision: str
    matcher: Callable[[str, str], AdapterResult]
    locale: str = "und"
    domain: str = "general"

    def __post_init__(self) -> None:
        required = (self.adapter_id, self.version, self.revision, self.locale, self.domain)
        if not all(value.strip() for value in required):
            raise ValueError("Adapter kimliği, sürümü, revision, locale ve domain zorunludur.")
        if self.revision.strip().lower() in {"latest", "main", "master", "head", "floating"}:
            raise ValueError("Adapter revision immutable ve pinli olmalıdır; floating ref kullanılamaz.")


def _pattern(value: str) -> re.Pattern[str]:
    return re.compile(r"(?<!\w)" + re.escape(tr_lower(value).strip()) + r"(?!\w)")


def count_boundary_occurrences(term: str, text: str) -> int:
    """Count exact Unicode-boundary occurrences, never raw substrings."""
    normalized = tr_lower(term).strip()
    if not normalized:
        return 0
    return len(_pattern(normalized).findall(tr_lower(text)))


def _reviewed_variants(term: str, reviewed_synonyms: dict[str, Iterable[str]] | None) -> list[str]:
    values = list(lexicons.expand_lsi(term))
    if reviewed_synonyms:
        for key, variants in reviewed_synonyms.items():
            normalized_key = tr_lower(key).strip()
            normalized_variants = [tr_lower(value).strip() for value in variants if value.strip()]
            if term == normalized_key:
                values.extend(normalized_variants)
            elif term in normalized_variants:
                values.append(normalized_key)
                values.extend(value for value in normalized_variants if value != term)
    return list(dict.fromkeys(value for value in values if value and value != term))


def reviewed_synonym_revision(reviewed_synonyms: dict[str, Iterable[str]]) -> str:
    """Return a deterministic revision hash for a reviewed locale dictionary."""
    rows = []
    for key in sorted(reviewed_synonyms, key=tr_lower):
        variants = sorted({tr_lower(value).strip() for value in reviewed_synonyms[key] if value.strip()})
        rows.append(f"{tr_lower(key).strip()}={'|'.join(variants)}")
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def match_term(
    term: str,
    text: str,
    *,
    allow_fuzzy: bool = True,
    reviewed_synonyms: dict[str, Iterable[str]] | None = None,
    synonym_revision: str | None = None,
    ontology_adapter: VersionedMatchAdapter | None = None,
    semantic_adapter: VersionedMatchAdapter | None = None,
) -> TermMatch:
    """Run exact → reviewed synonym → ontology → semantic → human cascade.

    Optional ontology/semantic stages never produce a final verified/pass verdict.
    Their matches are review-required evidence signals. ``allow_fuzzy`` retains the
    legacy Jaccard signal only when no explicit semantic adapter is configured.
    """
    normalized = tr_lower(term).strip()
    if not normalized:
        return TermMatch(term, False, MatchStage.NONE, None, 0, "Boş terim eşleştirilemez.")

    exact_count = count_boundary_occurrences(normalized, text)
    if exact_count:
        return TermMatch(
            term, True, MatchStage.EXACT, normalized, exact_count, "Unicode kelime sınırında exact eşleşme."
        )

    variants = _reviewed_variants(normalized, reviewed_synonyms)
    for variant in variants:
        count = count_boundary_occurrences(variant, text)
        if count:
            return TermMatch(
                term,
                True,
                MatchStage.SYNONYM,
                variant,
                count,
                f"İncelenmiş yerel sözlük varyantı ile eşleşme: {variant}.",
                adapter_id="reviewed-synonyms",
                adapter_version="1",
                adapter_revision=synonym_revision,
            )

    for stage, adapter in (
        (MatchStage.ONTOLOGY, ontology_adapter),
        (MatchStage.SEMANTIC, semantic_adapter),
    ):
        if adapter is None:
            continue
        try:
            result = adapter.matcher(normalized, text)
        except Exception as exc:
            return TermMatch(
                term,
                False,
                MatchStage.HUMAN_REVIEW,
                None,
                0,
                f"{adapter.adapter_id} adapter hatası: {type(exc).__name__}; insan incelemesi gerekir.",
                adapter_id=adapter.adapter_id,
                adapter_version=adapter.version,
                adapter_revision=adapter.revision,
                review_required=True,
            )
        if result.status is AdapterStatus.MATCH:
            return TermMatch(
                term,
                True,
                stage,
                result.matched_variant,
                1,
                result.explanation or f"{adapter.adapter_id} aday eşleşmesi; insan incelemesi gerekir.",
                adapter_id=adapter.adapter_id,
                adapter_version=adapter.version,
                adapter_revision=adapter.revision,
                confidence=result.confidence,
                review_required=True,
            )
        if result.status is AdapterStatus.ERROR:
            return TermMatch(
                term,
                False,
                MatchStage.HUMAN_REVIEW,
                None,
                0,
                result.explanation or f"{adapter.adapter_id} sonucu ERROR; insan incelemesi gerekir.",
                adapter_id=adapter.adapter_id,
                adapter_version=adapter.version,
                adapter_revision=adapter.revision,
                review_required=True,
            )

    if allow_fuzzy and semantic_adapter is None and lexicons.matches_semantically(normalized, text):
        return TermMatch(
            term,
            True,
            MatchStage.FUZZY,
            None,
            1,
            "Jaccard tabanlı legacy fuzzy sinyal; insan incelemesi gerekir.",
            adapter_id="legacy-jaccard",
            adapter_version="1",
            adapter_revision="built-in",
            review_required=True,
        )
    return TermMatch(term, False, MatchStage.NONE, None, 0, "Tüm çalıştırılan basamaklarda destek bulunamadı.")
