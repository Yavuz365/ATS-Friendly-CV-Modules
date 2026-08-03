"""
ats_engine.format_metadata_hygiene — Format/Metadata Kontrol Modülü (Y36-17).

Jobscan'in kontrol ettiği ama pipeline'da eksik olan format/metadata kuralları:
  - Kelime bütçesi (hedef: 600-1000)
  - Paragraf uzunluğu (>40 kelime uyarısı)
  - Özel karakter audit
  - Bullet/cümle sayısı

Bağımlılık: yalnızca standart kütüphane + ats_engine.text
"""

from __future__ import annotations

from .cv_parser import _SPECIAL_CHARS
from .text import sentences


def check_word_budget(cv_text: str, min_words: int = 600, max_words: int = 1000) -> dict:
    """Kelime sayısı bütçe kontrolü."""
    words = cv_text.split()
    count = len(words)
    if count < min_words:
        verdict = f"⚠️ Çok kısa ({count} kelime) — hedef: {min_words}-{max_words}"
    elif count > max_words:
        verdict = f"⚠️ Çok uzun ({count} kelime) — hedef: {min_words}-{max_words}"
    else:
        verdict = f"✅ Bütçe dahilinde ({count} kelime)"
    return {"word_count": count, "min": min_words, "max": max_words, "verdict": verdict}


def check_paragraph_length(cv_text: str, max_sentence_words: int = 40) -> dict:
    """Uzun cümle/paragraf tespiti."""
    sents = sentences(cv_text)
    long_sentences = []
    for s in sents:
        word_count = len(s.split())
        if word_count > max_sentence_words:
            long_sentences.append({"text": s[:80] + "..." if len(s) > 80 else s, "words": word_count})
    return {
        "total_sentences": len(sents),
        "long_sentences": len(long_sentences),
        "details": long_sentences,
        "verdict": (
            f"⚠️ {len(long_sentences)} uzun cümle (>{max_sentence_words} kelime)"
            if long_sentences
            else "✅ Tüm cümleler uygun uzunlukta"
        ),
    }


def check_special_characters(cv_text: str) -> dict:
    """ATS-kırıcı özel karakter audit'i."""
    matches = _SPECIAL_CHARS.findall(cv_text)
    unique_chars = set(matches)
    return {
        "total_special": len(matches),
        "unique_chars": sorted(unique_chars),
        "verdict": (
            f"⚠️ {len(matches)} özel karakter bulundu: {', '.join(sorted(unique_chars))}"
            if matches
            else "✅ Özel karakter yok"
        ),
    }


def check_bullet_count(cv_text: str, min_per_role: int = 3, max_per_role: int = 6) -> dict:
    """Bullet point sayısı kontrolü (deneyim bölümlerinde)."""
    lines = cv_text.split("\n")
    bullet_lines = [ln.strip() for ln in lines if ln.strip().startswith(("-", "•", "–"))]
    return {
        "total_bullets": len(bullet_lines),
        "recommended_per_role": f"{min_per_role}-{max_per_role}",
        "verdict": (
            "✅ Bullet sayısı uygun"
            if len(bullet_lines) >= min_per_role
            else f"⚠️ Sadece {len(bullet_lines)} bullet — en az {min_per_role} önerilir"
        ),
    }


def full_hygiene_check(cv_text: str) -> dict:
    """Tüm format/metadata kontrollerini tek seferde çalıştır."""
    return {
        "word_budget": check_word_budget(cv_text),
        "paragraph_length": check_paragraph_length(cv_text),
        "special_characters": check_special_characters(cv_text),
        "bullet_count": check_bullet_count(cv_text),
    }
