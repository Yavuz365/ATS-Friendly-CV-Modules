"""
ats_engine.synthesis — SENTEZ katmanı ('düğümü bağlama').

Analizden çıkan dağınık, ağırlıklı parçaları; dürüst, güçlü, ilana özel CV malzemesine
dokur. synthesis-rules.md + Grammarly 'Quantification Patterns' / 'Action Verbs' /
'Active Voice' kurallarının operasyonel karşılığı.

İçerik:
  - build_xyz / build_car  : başarı cümlesi inşası (niyete göre aktif fiil + zorunlu metrik)
  - audit_bullet           : bir maddenin kalite denetimi (sayı? aktif? uzunluk?)
  - cluster_skills         : becerileri kanonik kümelere toplama (Beceriler bölümü için)
  - classify_gaps          : eksikleri kapatılabilir/kapatılamaz diye ayırma (DÖNGÜ kuralı)
  - anti_stuffing_report   : terim yoğunluğu denetimi (>%5 = şişirme)

DÜRÜSTLÜK: classify_gaps yalnızca kanıt bankasında karşılığı olanı 'kapatılabilir' sayar;
gerçekte olmayan beceri asla CV'ye eklenmez ve revizyon döngüsüne SOKULMAZ.

Bağımlılık: yalnızca standart kütüphane (+ ats_engine.lexicons, text, evidence_bank).
"""

from __future__ import annotations

from . import lexicons
from .evidence_bank import Evidence, find_support
from .text import has_quantification, looks_passive

# ----------------------------- başarı cümlesi inşası -----------------------------

def build_xyz(x_result: str, y_metric: str, z_method: str, intent: str = "achievement") -> str:
    """
    Google XYZ formülü (TR): '[Z yöntemiyle] yaparak, [Y ölçüsüyle] [X sonucunu] başardım.'
    intent'e uygun güçlü bir aktif fiille açılır.
    """
    verb = (lexicons.action_verbs_by_intent(intent) or ["achieved"])[0]
    tr_verb = {
        "led": "yöneterek", "directed": "yöneterek", "orchestrated": "koordine ederek",
        "achieved": "gerçekleştirerek", "delivered": "teslim ederek",
        "improved": "iyileştirerek", "optimized": "optimize ederek", "streamlined": "sadeleştirerek",
        "increased": "artırarak", "grew": "büyüterek", "reduced": "azaltarak", "cut": "düşürerek",
        "built": "kurarak", "created": "oluşturarak", "developed": "geliştirerek",
        "analyzed": "analiz ederek", "negotiated": "müzakere ederek", "executed": "yürüterek",
        "presented": "sunarak",
    }.get(verb, "gerçekleştirerek")
    return f"{z_method} {tr_verb} ({verb}), {y_metric} ile ölçülen {x_result} sonucunu elde ettim."


def build_car(context: str, action: str, result: str) -> str:
    """CAR (Context–Action–Result) — kısa CV maddesi için sonuç-odaklı kalıp."""
    return f"{context}; {action} → {result}."


def audit_bullet(bullet: str) -> dict:
    """
    Bir CV maddesini synthesis-rules + Grammarly kalite kurallarına göre denetler.
    issues boşsa madde 'geçti' sayılır.
    """
    issues = []
    if not has_quantification(bullet):
        issues.append("Niceleme yok: en az 1 ölçülebilir sonuç ekle (%/sayı/süre/para).")
    if looks_passive(bullet):
        issues.append("Pasif yapı sezildi: aktif güçlü fiille başlat (yönetti/optimize etti/azalttı).")
    words = len((bullet or "").split())
    if words > 34:
        issues.append(f"Çok uzun ({words} kelime): 1–2 satıra indir.")
    if words < 4:
        issues.append("Çok kısa: bağlam + eylem + sonuç içermeli.")
    return {"bullet": bullet, "ok": not issues, "issues": issues, "word_count": words}


# ----------------------------- kümeleme -----------------------------

def cluster_skills(terms: list[str]) -> list[dict]:
    """
    Becerileri kanonik kümelere toplar (ATS 'Beceriler' bölümünün düzgün ayrıştırılması için).
    Kanonik karşılığı olmayanlar 'Diğer' kümesinde toplanır.
    """
    clusters: dict[str, list[str]] = {}
    for t in terms:
        canon = lexicons.normalize_skill(t) or "Diğer / Other"
        clusters.setdefault(canon, [])
        if t not in clusters[canon]:
            clusters[canon].append(t)
    return [{"cluster_label": k, "member_skills": v} for k, v in clusters.items()]


# ----------------------------- gap sınıflandırma (DÖNGÜ kuralı) -----------------------------

def classify_gaps(gap_terms: list[str], bank: list[Evidence], min_overlap: float = 0.18) -> dict:
    """
    Eksik zorunlu terimleri ikiye ayırır:
      closable    — kanıt bankasında karşılığı VAR, henüz CV'ye yansımamış → sentez döngüsüne gider
      uncloseable — adayda gerçekten YOK → dürüstçe kabul edilir, döngüye SOKULMAZ
    Bu, 'sonsuz revizyon döngüsü' (H1) hatasını kıran ayrımdır.
    """
    closable, uncloseable = [], []
    for term in gap_terms:
        ev, score = find_support(term, bank, min_overlap=min_overlap)
        if ev:
            closable.append({"term": term, "evidence_id": ev.id, "support_score": score,
                             "action": f"'{term}' kanıtı {ev.id} girdisinde var → ilgili deneyim maddesinde bu terimi/varyantını açıkça geçir."})
        else:
            uncloseable.append({"term": term,
                                "action": f"'{term}' için kanıt yok → CV'ye EKLENMEZ (dürüstlük). Gerçek bir deneyim varsa kanıt bankasına gerçek bir girdi ekle."})
    return {"closable": closable, "uncloseable": uncloseable,
            "loop_should_continue": len(closable) > 0}


def stopping_condition(score_pct: float, closable_gaps: list, target_low: float = 75.0) -> dict:
    """
    Revizyon döngüsünün doğru durma koşulu (H1 sonsuz-döngü düzeltmesi).

    DUR  ⟺  ( skor ≥ hedef )  VEYA  ( kapatılabilir gap kalmadı ).

    Gerekçe: Döngü yalnızca AKSİYON ALINABİLİR bir hamle kaldığında dönmeli.
    Skor hedefin altında olsa bile kapatılabilir gap yoksa, ek sentez turu
    skoru yükseltemez (kalan açık yapısal/kapatılamaz). Bu durumda eski mantık
    sonsuza dek 'DEVAM' derdi — H1 düzeltmesi bunu engeller.
    """
    at_target = score_pct >= target_low
    no_moves = len(closable_gaps) == 0
    done = at_target or no_moves

    if at_target and no_moves:
        reason = f"Hedef bant (≥{target_low}) sağlandı ve kapatılabilir gap yok → DUR (teslim)"
    elif at_target:
        reason = f"skor={score_pct} ≥ {target_low} → DUR (teslim; kalan gap'ler opsiyonel iyileştirme)"
    elif no_moves:
        reason = (f"skor={score_pct} (hedef≥{target_low}) ANCAK kapatılabilir gap=0 → DUR "
                  f"(yapısal/kapatılamaz açık; ek tur skoru yükseltmez — dürüstlük kuralı)")
    else:
        reason = (f"skor={score_pct} (hedef≥{target_low}) / kapatılabilir gap={len(closable_gaps)} "
                  f"→ DEVAM (sentez/revizyon turu)")
    return {"stop": done, "reason": reason, "at_target": at_target, "no_closable_moves": no_moves}


# ----------------------------- anti-stuffing -----------------------------

def anti_stuffing_report(cv_text: str, terms: list[str], warn_density: float = 0.05) -> dict:
    """
    Her önemli terim için CV'deki yoğunluğu hesaplar; eşiği (varsayılan %5) aşanı işaretler.
    Hedef: ~%1–3 birincil terim; coverage > density (terimi tekrar değil, farklı bölümlerde geçir).
    """
    low = (cv_text or "").lower()
    total = max(1, len(low.split()))
    flags = []
    for t in terms:
        tl = t.lower()
        count = low.count(tl)
        d = count / total
        if d > warn_density:
            flags.append({"term": t, "count": count, "density": round(d, 4),
                          "note": "ŞİŞİRME: farklı bölümlere dağıt veya eşanlamlı/varyant kullan."})
    return {"flagged": flags, "ok": not flags,
            "guidance": "Önemli terimi 2–3 kez, farklı bölümlerde (Beceriler'de iddia, Deneyim'de kanıt). >%5 = şişirme."}
