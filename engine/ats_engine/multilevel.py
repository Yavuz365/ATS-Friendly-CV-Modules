"""
ats_engine.multilevel — Üç-seviyeli ATS skorlama + dil kapısı.

Level 1  →  Araç-CV kapısı (gate): Tek bir AI aracının ürettiği CV'nin
            ham JD eşleşmesini ölçer. τ eşiğini geçemezse L2'ye taşınmaz.

Level 2  →  Sekiz-parça en-iyi-seçimi (best-of-8): Her CV bölümü (özet,
            deneyim ×4, beceriler, eğitim, sertifikalar) için tüm araçlardan
            en yüksek skoru alan parçayı seçer, birleştirir, dikiş cezası uygular.

Level 3  →  Kategori/sentetik ilan robustness skoru: Birleşik CV'yi birden
            fazla benzer ilana karşı test eder, varyans ölçer.

LangGate →  Tek-dil tutarlılığı kapısı. CV dili ile JD dili uyuşmuyorsa
            skor cezalandırılır.

Bağımlılık: yalnızca standart kütüphane (+ ats_engine alt modülleri).
"""

from __future__ import annotations

import re
from collections import Counter

from . import scoring, text

# ─── Sabitler ────────────────────────────────────────────────────────────────

L1_GATE_THRESHOLD: float = 0.70   # τ — araç-CV geçiş eşiği
L2_SEAM_PENALTY: float = 0.15     # κ — dikiş cezası katsayısı
LANG_PURITY_THRESHOLD: float = 0.85  # p₀ — dil saflık eşiği

# Dil tespiti için regex havuzları
_TR_CHARS = re.compile(r"[çÇğĞıİöÖşŞüÜ]")
_EN_WORDS = re.compile(
    r"\b(the|and|of|in|to|for|with|that|this|from|are|was|were|been|have|has|had|"
    r"will|would|could|should|can|may|might|shall|not|but|which|their|they|our|"
    r"your|about|into|through|during|before|after|between|under|over)\b",
    re.IGNORECASE,
)
_TR_WORDS = re.compile(
    r"\b(ve|veya|ile|için|bir|bu|şu|olan|olarak|gibi|üzerinde|altında|"
    r"arasında|sonra|önce|kadar|daha|ancak|fakat|ama|hem|ya|ise|"
    r"tarafından|dolayı|nedeniyle|hakkında|karşı|boyunca)\b",
    re.IGNORECASE,
)

# CV bölüm etiketleri (8 parça)
SECTION_LABELS: list[str] = [
    "summary",
    "experience_1",
    "experience_2",
    "experience_3",
    "experience_4",
    "skills",
    "education",
    "certifications",
]


# ─── Dil Tespiti ve Kapısı ──────────────────────────────────────────────────

def detect_language(doc: str) -> str:
    """
    Metnin baskın dilini tespit eder: 'tr' veya 'en'.
    Heuristik: Türkçe'ye özgü karakterler + dil-özel kelime frekansı.
    """
    if not doc or not doc.strip():
        return "en"

    tr_char_hits = len(_TR_CHARS.findall(doc))
    tr_word_hits = len(_TR_WORDS.findall(doc))
    en_word_hits = len(_EN_WORDS.findall(doc))

    tr_score = tr_char_hits * 2 + tr_word_hits
    en_score = en_word_hits

    return "tr" if tr_score > en_score else "en"


def language_purity(doc: str, expected_lang: str) -> float:
    """
    Belgenin beklenen dile ne kadar sadık olduğunu [0, 1] ölçer.
    Karışık dilli CV, ATS parser'ları şaşırtır.

    ATSE-9 fix: Bilinmeyen kelimeler artık 0.5 ağırlıkla sayılıyor (nötr).
    Eski davranış: bilinmeyen → 1.0 (beklenen dile dahil) → purity her zaman ~1.0
    oluyordu ve lang_gate hiç tetiklenmiyordu.
    Yeni: Yalnızca kesinlikle eşleşen kelimeler 1.0, karşı dil 0.0, bilinmeyen 0.5.
    """
    if not doc or not doc.strip():
        return 1.0

    words = text.tokenize(doc, ngram_max=1, drop_stopwords=False)
    if not words:
        return 1.0

    weighted_hits = 0.0
    total = len(words)

    for w in words:
        is_tr_char = bool(_TR_CHARS.search(w))
        is_tr_word = bool(_TR_WORDS.match(w))
        is_en_word = bool(_EN_WORDS.match(w))

        if expected_lang == "tr":
            if is_tr_char or is_tr_word:
                weighted_hits += 1.0   # kesin Türkçe sinyal
            elif is_en_word:
                weighted_hits += 0.0   # kesin yabancı dil
            else:
                weighted_hits += 0.5   # bilinmeyen → nötr (yarım ağırlık)
        else:  # en
            if is_en_word:
                weighted_hits += 1.0   # kesin İngilizce sinyal
            elif is_tr_char or is_tr_word:
                weighted_hits += 0.0   # kesin yabancı dil
            else:
                weighted_hits += 0.5   # bilinmeyen → nötr (yarım ağırlık)

    return weighted_hits / total if total else 1.0


def lang_gate(cv_text: str, jd_text: str, p0: float = LANG_PURITY_THRESHOLD) -> float:
    """
    Dil kapısı çarpanı [0, 1]. JD dilini tespit eder, CV'nin o dile
    sadakatini ölçer. Saflık p₀'ın altındaysa ceza başlar.

    Formül: LG = min(1.0, purity / p₀)
    """
    jd_lang = detect_language(jd_text)
    purity = language_purity(cv_text, jd_lang)
    return min(1.0, purity / p0) if p0 > 0 else 1.0


# ─── Level 1: Araç-CV Kapısı ────────────────────────────────────────────────

def level1_gate(
    jd_text: str,
    cv_text: str,
    must_terms: list[str],
    threshold: float = L1_GATE_THRESHOLD,
    **score_kwargs,
) -> dict:
    """
    Tek bir AI aracının ürettiği CV'yi JD'ye karşı skorlar.
    Geçiş eşiğini (τ) karşılayıp karşılamadığını bildirir.

    Returns:
        {"score": float, "passed": bool, "detail": dict}
    """
    result = scoring.ats_match_score(jd_text, cv_text, must_terms, **score_kwargs)
    score = result["score_percent"] / 100.0
    return {
        "score": round(score, 4),
        "passed": score >= threshold,
        "threshold": threshold,
        "detail": result,
    }


# ─── Level 2: Sekiz-Parça En-İyi Seçimi ─────────────────────────────────────

def _section_score(
    jd_text: str,
    section_text: str,
    must_terms: list[str],
    **score_kwargs,
) -> float:
    """Tek bir bölümün JD'ye kısmi eşleşme skorunu hesaplar."""
    if not section_text or not section_text.strip():
        return 0.0
    result = scoring.ats_match_score(jd_text, section_text, must_terms, **score_kwargs)
    return result["score_percent"] / 100.0


def level2_best_of(
    jd_text: str,
    tool_sections: dict[str, dict[str, str]],
    must_terms: list[str],
    **score_kwargs,
) -> dict:
    """
    Her CV bölümü için tüm araçlar arasından en yüksek skoru seçer.

    Args:
        jd_text: İş ilanı metni
        tool_sections: {araç_adı: {bölüm_adı: metin}} haritası
            Örnek: {"chatgpt": {"summary": "...", "experience_1": "...", ...},
                     "claude": {"summary": "...", ...}}
        must_terms: Zorunlu JD terimleri
        **score_kwargs: ats_match_score'a iletilecek ek parametreler

    Returns:
        {"best_sections": {bölüm: {"tool": str, "score": float, "text": str}},
         "tool_usage": Counter}
    """
    best: dict[str, dict] = {}
    tool_usage: Counter = Counter()

    for section in SECTION_LABELS:
        best_score = -1.0
        best_tool = ""
        best_text = ""

        for tool_name, sections in tool_sections.items():
            sec_text = sections.get(section, "")
            if not sec_text.strip():
                continue
            sc = _section_score(jd_text, sec_text, must_terms, **score_kwargs)
            if sc > best_score:
                best_score = sc
                best_tool = tool_name
                best_text = sec_text

        if best_tool:
            tool_usage[best_tool] += 1

        best[section] = {
            "tool": best_tool,
            "score": round(best_score, 4) if best_score >= 0 else 0.0,
            "text": best_text,
        }

    return {"best_sections": best, "tool_usage": dict(tool_usage)}


def _seam_penalty(tool_usage: dict[str, int], total_sections: int = 8) -> float:
    """
    Dikiş cezası: farklı araçlardan birleştirilen parça sayısı arttıkça
    tutarlılık riski artar.

    Formül: κ × (1 − dominant_tool_ratio)
    """
    if not tool_usage or total_sections == 0:
        return 0.0

    max_count = max(tool_usage.values(), default=0)
    dominant_ratio = max_count / total_sections
    return L2_SEAM_PENALTY * (1.0 - dominant_ratio)


def level2_final(
    jd_text: str,
    tool_sections: dict[str, dict[str, str]],
    must_terms: list[str],
    **score_kwargs,
) -> dict:
    """
    Level 2 tam sonucu: en-iyi parçaları birleştir, dikiş cezası uygula,
    birleşik CV'yi yeniden skorla.

    Returns:
        {"combined_text": str, "combined_score": float, "seam_penalty": float,
         "final_score": float, "best_sections": dict, "tool_usage": dict}
    """
    l2 = level2_best_of(jd_text, tool_sections, must_terms, **score_kwargs)
    best = l2["best_sections"]
    usage = l2["tool_usage"]

    # Birleşik metni oluştur
    parts = []
    for section in SECTION_LABELS:
        t = best.get(section, {}).get("text", "")
        if t.strip():
            parts.append(t.strip())
    combined = "\n\n".join(parts)

    # Birleşik CV'yi yeniden skorla
    if combined.strip():
        res = scoring.ats_match_score(jd_text, combined, must_terms, **score_kwargs)
        raw_score = res["score_percent"] / 100.0
    else:
        raw_score = 0.0

    # Dikiş cezası
    penalty = _seam_penalty(usage)
    final = max(0.0, raw_score - penalty)

    return {
        "combined_text": combined,
        "combined_score": round(raw_score, 4),
        "seam_penalty": round(penalty, 4),
        "final_score": round(final, 4),
        "best_sections": best,
        "tool_usage": usage,
    }


# ─── Level 3: Kategori / Sentetik İlan Robustness ───────────────────────────

def level3_category(
    cv_text: str,
    jd_texts: list[str],
    must_terms: list[str],
    **score_kwargs,
) -> dict:
    """
    Birleşik CV'yi aynı kategorideki birden fazla ilana karşı test eder.
    Varyans düşükse CV robust (dayanıklı), yüksekse aşırı uyarlanmış.

    Args:
        cv_text: Birleşik/final CV metni
        jd_texts: Aynı kategorideki JD metinleri listesi
        must_terms: Kategorinin ortak zorunlu terimleri
        **score_kwargs: ats_match_score'a ek parametreler

    Returns:
        {"scores": list[float], "mean": float, "std": float,
         "min": float, "max": float, "robust": bool}
    """
    if not jd_texts:
        return {
            "scores": [], "mean": 0.0, "std": 0.0,
            "min": 0.0, "max": 0.0, "robust": False,
        }

    scores = []
    for jd in jd_texts:
        res = scoring.ats_match_score(jd, cv_text, must_terms, **score_kwargs)
        scores.append(res["score_percent"] / 100.0)

    n = len(scores)
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / n
    std = variance ** 0.5

    return {
        "scores": [round(s, 4) for s in scores],
        "mean": round(mean, 4),
        "std": round(std, 4),
        "min": round(min(scores), 4),
        "max": round(max(scores), 4),
        "robust": std <= 0.10,  # σ ≤ 0.10 → robust
    }
