"""
ats_engine.cliche_tone — Buzzword / Klişe Dedektörü (Y36-21).

Jobscan "Resume Tone: Cliches found" uyarısı — GPT ile rewriting yapıldığında
klişe fiiller ekleniyor. Bu modül AI-tetikleyici ifadeleri tespit eder.

Bağımlılık: yalnızca standart kütüphane + ats_engine.lexicons
"""

from __future__ import annotations

from .lexicons import cliche_verbs
from .text import tr_lower

# Ek buzzword/klişe kalıplar (fiil dışı)
_BUZZWORD_PATTERNS: list[str] = [
    "synergy", "synergize", "paradigm shift", "best-in-class",
    "thought leader", "game-changer", "disruptive", "cutting-edge",
    "world-class", "bleeding edge", "next-generation", "mission-critical",
    "results-driven", "self-starter", "go-getter", "team player",
    "think outside the box", "hit the ground running",
    "move the needle", "low-hanging fruit", "deep dive",
    "circle back", "take it to the next level",
    "proactive", "dynamic", "seasoned professional",
    "track record of success", "proven ability",
]


def detect_cliches(cv_text: str) -> dict:
    """
    CV'deki klişe fiiller ve buzzword'leri tespit eder.

    Returns:
        {
            "cliche_verb_hits": [{"verb": str, "count": int}],
            "buzzword_hits": [{"phrase": str, "count": int}],
            "total_cliches": int,
            "tone_verdict": str,
        }
    """
    cv_low = tr_lower(cv_text)
    cv_words = cv_low.split()

    # Cliche verb tespiti
    cliches = cliche_verbs()
    verb_hits: list[dict] = []
    for verb in sorted(cliches):
        # Fiil ve türevlerini say (ör. spearheaded, spearheading)
        count = sum(1 for w in cv_words if w.startswith(verb[:6]))
        if count > 0:
            verb_hits.append({"verb": verb, "count": count})

    # Buzzword tespiti
    buzz_hits: list[dict] = []
    for phrase in _BUZZWORD_PATTERNS:
        count = cv_low.count(phrase.lower())
        if count > 0:
            buzz_hits.append({"phrase": phrase, "count": count})

    total = sum(v["count"] for v in verb_hits) + sum(b["count"] for b in buzz_hits)

    if total == 0:
        tone = "✅ Clean tone — klişe/buzzword yok"
    elif total <= 2:
        tone = f"⚠️ {total} klişe tespit edildi — düzeltme önerilir"
    else:
        tone = f"❌ {total} klişe/buzzword — AI-detection riski yüksek, acil düzelt"

    return {
        "cliche_verb_hits": verb_hits,
        "buzzword_hits": buzz_hits,
        "total_cliches": total,
        "tone_verdict": tone,
    }
