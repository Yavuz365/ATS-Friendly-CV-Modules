"""
ats_engine.completeness_guard — Kanıt Kullanım/Recall Modülü (Y36-16).

Evidence bank'taki kanıtların CV'ye ne kadar aktarıldığını ölçer.
Jobscan 70 puanının KÖK NEDENİ: Framework CV'deki kanıtlar CV'ye aktarılmamış.

Akış:
    evidence_bank → tüm kanıtlar
    CV metni      → kullanılan kanıtlar
    Sonuç         → kullanım oranı + atlanmış kanıt listesi
"""

from __future__ import annotations

from . import evidence_bank, text


def evidence_recall(
    framework_cv_text: str,
    cv_text: str,
    threshold: float = 0.5,
) -> dict:
    """
    Framework CV'deki kanıtların CV'de kullanılma oranını ölçer.

    Args:
        framework_cv_text: Orijinal framework CV (tüm kanıtları içerir)
        cv_text: Son CV taslağı
        threshold: Jaccard benzerlik eşiği (eşleşme kabul sınırı)

    Returns:
        {
            "total_evidence": int,
            "used_evidence": int,
            "recall_percent": float,       # 0-100
            "used": [...],                 # eşleşen kanıtlar
            "missed": [...],               # atlanmış kanıtlar
            "verdict": str,
        }
    """
    bank = evidence_bank.parse_bank(framework_cv_text)
    cv_tokens_set = set(text.tokenize(cv_text, ngram_max=2, drop_stopwords=True))

    used: list[dict] = []
    missed: list[dict] = []

    for ev in bank:
        ev_source = ev.sentence or ev.raw or ev.haystack()
        ev_tokens = set(text.tokenize(ev_source, ngram_max=2, drop_stopwords=True))
        if not ev_tokens:
            continue
        overlap = len(ev_tokens & cv_tokens_set) / len(ev_tokens)
        entry = {"tag": ev.id, "text": ev_source[:100], "overlap": round(overlap, 2)}
        if overlap >= threshold:
            used.append(entry)
        else:
            missed.append(entry)

    total = len(used) + len(missed)
    recall_pct = (len(used) / total * 100) if total > 0 else 0.0

    if recall_pct >= 90:
        verdict = "Yüksek sözcüksel kullanım sinyali — olgusal doğrulama değildir"
    elif recall_pct >= 70:
        verdict = "Bazı kanıt girdileri sözcüksel olarak atlanmış; inceleyin"
    elif recall_pct >= 50:
        verdict = "Birçok kanıt girdisi sözcüksel olarak atlanmış; inceleyin"
    else:
        verdict = "Kanıt girdilerinin çoğu sözcüksel olarak eşleşmedi; inceleyin"

    return {
        "total_evidence": total,
        "used_evidence": len(used),
        "recall_percent": round(recall_pct, 1),
        "used": used,
        "missed": missed,
        "verdict": verdict,
        "verification_status": "UNVERIFIED",
        "limitation": "Lexical overlap is not factual verification.",
    }
