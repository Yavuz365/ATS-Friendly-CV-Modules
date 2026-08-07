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
    r"\b(?:must|required|mandatory|essential|shall|zorunlu(?:dur|dır|dur)?|gereklidir|aranmaktadır|şarttır|olmalıdır)\b",
    re.IGNORECASE | re.UNICODE,
)
_PREFERRED_RE = re.compile(
    r"\b(?:preferred|nice\s+to\s+have|advantage|plus|tercihen|tercih\s+sebebidir|tercih\s+sebebi|avantaj|artı)\b",
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
    # Duration-based experience (e.g. "3 years", "3 yıl") is classified as
    # EXPERIENCE.  Must be checked before the SKILL catch-all so that duration
    # sentences are not mis-classified as SKILL.
    ("EXPERIENCE", re.compile(r"\b\d+\s+(?:years?|yıl)\b", re.IGNORECASE)),
    (
        # "experience with/in/using" and Turkish inflected forms (e.g. deneyimi)
        # without a numeric duration marker are classified as SKILL.
        "SKILL",
        re.compile(
            r"\b(?:experience\s+(?:with|in|using)|deneyim\w+|bilgi\w*|skill|knowledge|proficien|hakim|beceri|yetkin)\w*\b",
            re.IGNORECASE,
        ),
    ),
    # Plain experience/duration words without a preceding count.
    ("EXPERIENCE", re.compile(r"\b(?:experience|years?|deneyim|tecrübe|yıl)\b", re.IGNORECASE)),
    ("CERTIFICATION", re.compile(r"\b(?:certificate|certification|sertifika)\w*\b", re.IGNORECASE)),
    (
        "LOCATION",
        re.compile(r"\b(?:location|located|relocate|travel|lokasyon|ikamet|seyahat|taşın)\w*\b", re.IGNORECASE),
    ),
)


@dataclass(frozen=True)
class RequirementExtraction:
    requirements: list[JobRequirement]
    review_required: bool
    source_sha256: str
    extractor_version: str = "job-requirements/1.0.0"


def _category(sentence: str) -> str:
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
                category=_category(stripped),
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
