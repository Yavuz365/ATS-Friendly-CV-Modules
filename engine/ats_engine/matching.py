"""One explainable term-matching contract for counts, coverage, and gaps."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from . import lexicons
from .text import tr_lower


class MatchStage(str, Enum):
    EXACT = "EXACT"
    SYNONYM = "SYNONYM"
    FUZZY = "FUZZY"
    NONE = "NONE"


@dataclass(frozen=True)
class TermMatch:
    term: str
    matched: bool
    stage: MatchStage
    matched_variant: str | None
    count: int
    explanation: str


def _pattern(value: str) -> re.Pattern[str]:
    return re.compile(r"(?<!\w)" + re.escape(tr_lower(value).strip()) + r"(?!\w)")


def count_boundary_occurrences(term: str, text: str) -> int:
    """Count exact Unicode-boundary occurrences, never raw substrings."""
    normalized = tr_lower(term).strip()
    if not normalized:
        return 0
    return len(_pattern(normalized).findall(tr_lower(text)))


def match_term(term: str, text: str, *, allow_fuzzy: bool = True) -> TermMatch:
    """Return the strongest deterministic match and its explanation."""
    normalized = tr_lower(term).strip()
    if not normalized:
        return TermMatch(term, False, MatchStage.NONE, None, 0, "Boş terim eşleştirilemez.")

    exact_count = count_boundary_occurrences(normalized, text)
    if exact_count:
        return TermMatch(
            term, True, MatchStage.EXACT, normalized, exact_count, "Unicode kelime sınırında exact eşleşme."
        )

    for variant in lexicons.expand_lsi(normalized):
        count = count_boundary_occurrences(variant, text)
        if count:
            return TermMatch(
                term,
                True,
                MatchStage.SYNONYM,
                variant,
                count,
                f"İncelenmiş yerel sözlük varyantı ile eşleşme: {variant}.",
            )

    if allow_fuzzy and lexicons.matches_semantically(normalized, text):
        return TermMatch(
            term,
            True,
            MatchStage.FUZZY,
            None,
            1,
            "Jaccard tabanlı fuzzy sinyal; insan incelemesi gerekir.",
        )
    return TermMatch(term, False, MatchStage.NONE, None, 0, "Exact, synonym veya fuzzy destek bulunamadı.")
