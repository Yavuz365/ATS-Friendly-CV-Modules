"""Review-first TR/EN job requirement extraction.

This module extracts explicit sentence spans and never promotes arbitrary body
keywords into mandatory requirements. Output remains REVIEW until a human creates
an immutable approval version in the contract store.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from .contracts import DataStatus, JobRequirement, ProcessStatus

_SENTENCE_RE = re.compile(r"[^\n.!?]+(?:[.!?]+|$)", re.UNICODE)
_NEGATION_RE = re.compile(
    r"\b(?:not|required\s+not|no\s+need|without|değil|aranmamaktadır|gerekmemektedir|zorunlu\s+değildir)\b",
    re.IGNORECASE | re.UNICODE,
)
_MUST_RE = re.compile(
    # JOB-002 fix: Turkish "zorunlu" carries suffixes (zorunludur, zorunluluk, …)
    # that a bare `\bzorunlu\b` cannot reach because there is no word boundary
    # between "zorunlu" and its suffix. `\w*` extends the match to cover those
    # inflected forms; the leading `\b` still anchors it to a real word start,
    # so it cannot fire mid-word inside an unrelated token.
    r"\b(?:must|required|mandatory|essential|shall|zorunlu\w*|gereklidir|aranmaktadır|şarttır|olmalıdır)\b",
    re.IGNORECASE | re.UNICODE,
)
_PREFERRED_RE = re.compile(
    # JOB-002 fix: same morphology issue for "tercih sebebi/sebebidir".
    r"\b(?:preferred|nice\s+to\s+have|advantage|plus|tercihen|tercih\s+sebeb\w*|avantaj|artı)\b",
    re.IGNORECASE | re.UNICODE,
)
_RESPONSIBILITY_RE = re.compile(
    r"\b(?:responsible|responsibilities|manage|coordinate|prepare|track|yürüt|yönet|koordine|hazırla|takip)\w*\b",
    re.IGNORECASE | re.UNICODE,
)

_CATEGORY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "LANGUAGE",
        re.compile(
            r"\b(?:english|german|french|turkish|ingilizce|almanca|fransızca|türkçe|b[12]|c[12])\b", re.IGNORECASE
        ),
    ),
    (
        "EDUCATION",
        re.compile(
            r"\b(?:degree|bachelor|master|university|lisans|yüksek\s+lisans|üniversite|mezun)\w*\b", re.IGNORECASE
        ),
    ),
    (
        # JOB-004 fix: gold set draws a real distinction between tenure
        # ("3 years"/"3 yıl" of experience -> EXPERIENCE) and domain-skill
        # familiarity ("hands-on experience with Incoterms" -> SKILL, see
        # REQ-EN-MUST-001 / REQ-TR-MUST-001). Bare "experience"/"deneyim"
        # without an adjacent duration is not a tenure requirement, so it is
        # only counted here when a number precedes a year unit.
        "EXPERIENCE",
        re.compile(r"\b\d+\+?\s*(?:years?|yıl(?:lık)?)\b", re.IGNORECASE),
    ),
    ("CERTIFICATION", re.compile(r"\b(?:certificate|certification|sertifika|belge)\w*\b", re.IGNORECASE)),
    (
        "LOCATION",
        re.compile(r"\b(?:location|located|relocate|travel|lokasyon|ikamet|seyahat|taşın)\w*\b", re.IGNORECASE),
    ),
    (
        # "experience"/"deneyim"/"tecrübe" land here (not EXPERIENCE above)
        # whenever there is no adjacent duration signal — i.e. familiarity
        # with a domain tool/skill rather than a tenure requirement.
        "SKILL",
        re.compile(
            r"\b(?:skill|knowledge|proficien|hakim|bilgi|beceri|yetkin|experience|deneyim|tecrübe)\w*\b",
            re.IGNORECASE,
        ),
    ),
)


@dataclass(frozen=True)
class RequirementExtraction:
    requirements: list[JobRequirement]
    review_required: bool
    source_sha256: str
    extractor_version: str = "job-requirements/1.0.0"


def _category(sentence: str, modality: str) -> str:
    # JOB-004 fix: the gold schema always pairs modality=RESPONSIBILITY with
    # category=RESPONSIBILITY. A responsibility sentence (e.g. "prepare
    # export documents") can still contain a generic noun like "belge"
    # (document) that noun-based patterns below would otherwise misread as
    # CERTIFICATION. Once `_modality` has already decided this is a
    # responsibility sentence (no MUST/PREFERRED signal), that verdict wins.
    if modality == "RESPONSIBILITY":
        return "RESPONSIBILITY"
    for category, pattern in _CATEGORY_PATTERNS:
        if pattern.search(sentence):
            return category
    if _RESPONSIBILITY_RE.search(sentence):
        return "RESPONSIBILITY"
    return "OTHER"


def _modality(sentence: str) -> str:
    if _MUST_RE.search(sentence):
        return "MUST"
    if _PREFERRED_RE.search(sentence):
        return "PREFERRED"
    if _RESPONSIBILITY_RE.search(sentence):
        return "RESPONSIBILITY"
    return "UNKNOWN"


def _stable_id(job_posting_id: str, start: int, end: int, text: str) -> str:
    digest = hashlib.sha256(f"{job_posting_id}\0{start}\0{end}\0{text}".encode()).hexdigest()[:16]
    return f"REQ-{digest}"


def extract_job_requirements(job_posting_id: str, text: str) -> RequirementExtraction:
    """Extract explicit requirement candidates with source spans.

    Sentences without requirement/responsibility signals are omitted. Negated
    statements remain visible and REVIEW; they are never converted into positive
    requirements. No keyword-only body promotion is performed.
    """
    if not job_posting_id.strip():
        raise ValueError("job_posting_id zorunludur.")
    source_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    requirements: list[JobRequirement] = []

    for match in _SENTENCE_RE.finditer(text):
        raw = match.group(0)
        stripped = raw.strip()
        if not stripped:
            continue
        leading = len(raw) - len(raw.lstrip())
        start = match.start() + leading
        end = start + len(stripped)
        modality = _modality(stripped)
        negated = bool(_NEGATION_RE.search(stripped))
        if modality == "UNKNOWN" and not negated:
            continue
        requirements.append(
            JobRequirement(
                id=_stable_id(job_posting_id, start, end, stripped),
                job_posting_id=job_posting_id,
                text=stripped,
                requirement_type="EXPLICIT_SENTENCE",
                explicit=True,
                data_status=DataStatus.KNOWN,
                category=_category(stripped, modality),
                modality=modality,
                negated=negated,
                span_start=start,
                span_end=end,
                review_status=ProcessStatus.REVIEW,
                approval_version=None,
            )
        )

    return RequirementExtraction(
        requirements=requirements,
        review_required=bool(requirements),
        source_sha256=source_sha256,
    )
