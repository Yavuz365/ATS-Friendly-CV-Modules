"""
ats_engine.quantification_score — Ölçülebilir Sonuç Metriki (Y36-20).

Jobscan: "Measurable Results: 3 found, 5+ recommended"
Mevcut text.py sadece bullet bazında boolean döndürüyor.
Bu modül toplam sayı, hedef ve CV-genelinde skor hesaplar.

Bağımlılık: yalnızca standart kütüphane + ats_engine.text
"""

from __future__ import annotations

from .text import has_quantification, sentences


def quantification_audit(
    cv_text: str,
    target_min: int = 5,
) -> dict:
    """
    CV'deki ölçülebilir sonuçların toplam sayısını ve dağılımını hesaplar.

    Args:
        cv_text: CV metni
        target_min: Minimum önerilen ölçülebilir sonuç (Jobscan: 5+)

    Returns:
        {
            "total_quantified": int,
            "target": int,
            "quantified_lines": [...],
            "non_quantified_lines": [...],
            "score_percent": float,   # 0-100, min(total/target*100, 100)
            "verdict": str,
        }
    """
    sents = sentences(cv_text)
    quantified: list[str] = []
    non_quantified: list[str] = []

    for s in sents:
        if has_quantification(s):
            quantified.append(s[:100])
        else:
            # Sadece bullet-like satırları raporla (öneriler için)
            if s.strip() and len(s.split()) > 5:
                non_quantified.append(s[:100])

    total = len(quantified)
    score = min(total / target_min * 100, 100.0) if target_min > 0 else 100.0

    if total >= target_min:
        verdict = f"✅ {total} ölçülebilir sonuç — hedef ({target_min}+) karşılandı"
    elif total >= target_min // 2:
        verdict = f"⚠️ {total}/{target_min} — daha fazla rakam/yüzde/metrik ekle"
    else:
        verdict = f"❌ {total}/{target_min} — yetersiz; her deneyim maddesine XYZ sonucu ekle"

    return {
        "total_quantified": total,
        "target": target_min,
        "quantified_lines": quantified,
        "non_quantified_lines": non_quantified[:10],  # ilk 10 öneri
        "score_percent": round(score, 1),
        "verdict": verdict,
    }
