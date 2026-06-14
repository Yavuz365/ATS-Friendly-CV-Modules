"""
ats_engine.locale_consistency — AmE/BrE + LocaleGate (Y36-19).

JD'nin dilini (AmE vs BrE) tespit eder ve CV'deki tutarsızlıkları bulur.
"minimise" (BrE) vs "minimize" (AmE) gibi farklar ATS keyword match kaçırır.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import re

# Yaygın AmE/BrE farkları — ATS'de eşleşme kaçırma riski yüksek
_LOCALE_PAIRS: list[tuple[str, str]] = [
    # (AmE, BrE)
    ("optimize", "optimise"),
    ("minimize", "minimise"),
    ("maximize", "maximise"),
    ("organize", "organise"),
    ("analyze", "analyse"),
    ("recognize", "recognise"),
    ("specialize", "specialise"),
    ("standardize", "standardise"),
    ("customize", "customise"),
    ("authorize", "authorise"),
    ("utilize", "utilise"),
    ("prioritize", "prioritise"),
    ("finalize", "finalise"),
    ("harmonize", "harmonise"),
    ("digitalize", "digitalise"),
    ("centralize", "centralise"),
    ("summarize", "summarise"),
    ("rationalize", "rationalise"),
    ("synchronize", "synchronise"),
    ("categorize", "categorise"),
    ("color", "colour"),
    ("favor", "favour"),
    ("labor", "labour"),
    ("behavior", "behaviour"),
    ("center", "centre"),
    ("meter", "metre"),
    ("fiber", "fibre"),
    ("defense", "defence"),
    ("license", "licence"),
    ("catalog", "catalogue"),
    ("program", "programme"),
    ("fulfill", "fulfil"),
    ("enrollment", "enrolment"),
    ("traveled", "travelled"),
    ("modeling", "modelling"),
    ("canceled", "cancelled"),
]


def detect_locale(text: str) -> str:
    """
    Metindeki AmE/BrE işaretlerini sayarak locale tespit eder.

    Returns:
        "AmE" | "BrE" | "mixed" | "unknown"
    """
    text_low = text.lower()
    ame_count = 0
    bre_count = 0

    for ame, bre in _LOCALE_PAIRS:
        if ame in text_low:
            ame_count += text_low.count(ame)
        if bre in text_low:
            bre_count += text_low.count(bre)

    if ame_count == 0 and bre_count == 0:
        return "unknown"
    if ame_count > 0 and bre_count > 0:
        # Baskın locale belirle ama mixed flag
        return "mixed"
    return "AmE" if ame_count > 0 else "BrE"


def locale_mismatches(jd_text: str, cv_text: str) -> dict:
    """
    JD ve CV arasındaki locale tutarsızlıklarını tespit eder.

    Returns:
        {
            "jd_locale": str,
            "cv_locale": str,
            "mismatches": [{jd_term, cv_term, suggestion}],
            "verdict": str,
        }
    """
    jd_locale = detect_locale(jd_text)
    cv_locale = detect_locale(cv_text)
    jd_low = jd_text.lower()
    cv_low = cv_text.lower()

    mismatches = []
    for ame, bre in _LOCALE_PAIRS:
        # JD AmE kullanıyor ama CV BrE (veya tersi)
        if ame in jd_low and bre in cv_low and ame not in cv_low:
            mismatches.append({
                "jd_term": ame, "cv_term": bre,
                "suggestion": f"CV'de '{bre}' → '{ame}' olarak değiştir (JD locale ile eşleş)"
            })
        elif bre in jd_low and ame in cv_low and bre not in cv_low:
            mismatches.append({
                "jd_term": bre, "cv_term": ame,
                "suggestion": f"CV'de '{ame}' → '{bre}' olarak değiştir (JD locale ile eşleş)"
            })

    if not mismatches:
        verdict = "✅ Locale tutarlı — JD ve CV aynı dil varyantını kullanıyor"
    else:
        verdict = f"⚠️ {len(mismatches)} locale tutarsızlığı — ATS keyword match riski"

    return {
        "jd_locale": jd_locale,
        "cv_locale": cv_locale,
        "mismatches": mismatches,
        "verdict": verdict,
    }
