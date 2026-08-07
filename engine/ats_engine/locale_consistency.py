"""
ats_engine.locale_consistency — AmE/BrE + LocaleGate (Y36-19) + JD/CV language mismatch.

JD'nin dilini (AmE vs BrE) tespit eder ve CV'deki tutarsızlıkları bulur.
"minimise" (BrE) vs "minimize" (AmE) gibi farklar ATS keyword match kaçırır.

Ayrıca JD/CV dil uyumsuzluğunu (ör. Türkçe JD + İngilizce CV) tespit eder;
bu durum G3 kapısının PASS vermemesini sağlar.

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
            mismatches.append(
                {
                    "jd_term": ame,
                    "cv_term": bre,
                    "suggestion": f"CV'de '{bre}' → '{ame}' olarak değiştir (JD locale ile eşleş)",
                }
            )
        elif bre in jd_low and ame in cv_low and bre not in cv_low:
            mismatches.append(
                {
                    "jd_term": bre,
                    "cv_term": ame,
                    "suggestion": f"CV'de '{ame}' → '{bre}' olarak değiştir (JD locale ile eşleş)",
                }
            )

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


# ── JD/CV dil uyumsuzluğu tespiti ────────────────────────────────────────────

# Türkçeye özgü karakterler — sık rastlanan ise bunlar dilden bağımsız değildir
_TR_CHARS = frozenset("çÇğĞıİöÖşŞüÜ")

# Türkçe için sık geçen fonksiyonel kelimeler (duraksız küçük harfle)
_TR_FUNCTION_WORDS = frozenset(
    {
        "ve",
        "bir",
        "bu",
        "da",
        "de",
        "ile",
        "için",
        "olan",
        "olarak",
        "veya",
        "çalışma",
        "deneyim",
        "yıl",
        "aranıyor",
        "pozisyon",
        "başvuru",
        "görev",
        "tercihen",
        "aranan",
        "ekip",
        "şirket",
        "iş",
        "nitelik",
        "gereklilik",
        "sorumluluk",
        "hakkında",
    }
)

# İngilizce için sık geçen fonksiyonel kelimeler
_EN_FUNCTION_WORDS = frozenset(
    {
        "the",
        "and",
        "for",
        "with",
        "are",
        "you",
        "will",
        "have",
        "our",
        "experience",
        "skills",
        "required",
        "position",
        "team",
        "work",
        "company",
        "responsibilities",
        "requirements",
        "years",
    }
)

# En az bu kadar sinyal gerekli; daha azı UNKNOWN döndürür
_LANG_MIN_SIGNALS = 2


def detect_language(text: str) -> str:
    """Metnin birincil dilini tahmin eder: 'TR', 'EN' veya 'UNKNOWN'.

    Yalnızca hızlı sezgisel yöntemler kullanır; dış bağımlılık yoktur.
    Güven düzeyi düşükse 'UNKNOWN' döner — bu hiçbir zaman PASS olmaz.
    """
    if not text or not text.strip():
        return "UNKNOWN"

    # Türkçe karakter sayısı
    tr_char_score = sum(1 for ch in text if ch in _TR_CHARS)

    words = re.findall(r"[a-zA-ZçğışöüÇĞİŞÖÜ]+", text.lower())
    word_set = set(words)

    tr_word_score = len(word_set & _TR_FUNCTION_WORDS)
    en_word_score = len(word_set & _EN_FUNCTION_WORDS)

    # Türkçe karakterler güçlü sinyal
    if tr_char_score >= 3:
        tr_word_score += tr_char_score // 3

    if tr_word_score >= _LANG_MIN_SIGNALS and tr_word_score > en_word_score:
        return "TR"
    if en_word_score >= _LANG_MIN_SIGNALS and en_word_score > tr_word_score:
        return "EN"
    if tr_word_score == en_word_score and tr_word_score >= _LANG_MIN_SIGNALS:
        return "MIXED"
    return "UNKNOWN"


def detect_language_mismatch(jd_text: str, cv_text: str) -> dict:
    """JD ile CV arasındaki dil uyumsuzluğunu tespit eder.

    Returns:
        {
            "jd_language": str,       # 'TR' | 'EN' | 'MIXED' | 'UNKNOWN'
            "cv_language": str,
            "mismatch": bool,         # Güvenli mismatch ise True
            "verdict": str,
            "review_required": bool,  # UNKNOWN/MIXED → True
        }
    """
    jd_lang = detect_language(jd_text)
    cv_lang = detect_language(cv_text)

    known_langs = {"TR", "EN"}
    jd_known = jd_lang in known_langs
    cv_known = cv_lang in known_langs

    if not jd_known or not cv_known:
        # Yetersiz kanıt → iyimser PASS verilmez
        return {
            "jd_language": jd_lang,
            "cv_language": cv_lang,
            "mismatch": False,
            "verdict": (f"⚠️ JD/CV dil tespiti yetersiz (JD={jd_lang}, CV={cv_lang}); insan incelemesi gerekir."),
            "review_required": True,
        }

    if jd_lang != cv_lang:
        return {
            "jd_language": jd_lang,
            "cv_language": cv_lang,
            "mismatch": True,
            "verdict": (
                f"⚠️ JD ({jd_lang}) ile CV ({cv_lang}) farklı dillerde — "
                "ATS keyword eşleşmesi ve uygunluk değerlendirmesi olumsuz etkilenir."
            ),
            "review_required": True,
        }

    return {
        "jd_language": jd_lang,
        "cv_language": cv_lang,
        "mismatch": False,
        "verdict": f"✅ JD ve CV aynı dilde ({jd_lang})",
        "review_required": False,
    }
