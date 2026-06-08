"""
ats_engine.scoring — Hibrit ATS Match Score (denetim-düzeltmeli).

Bir iş ilanı (JD) ile bir CV arasındaki uyumu DETERMINISTIK olarak hesaplar.
Bu, LLM 'tahmini skor'un yerine geçen sayısal pusuladır.

Bileşenler ([0,1]'e normalize):
  Lex   — TF-IDF kosinüs (tüm terimler üzerinden dağılımsal benzerlik)
  Sem   — SBERT kosinüs (varsa; eşanlamlı/parafraz yakalar), yoksa graceful-degrade
  Cov   — zorunlu terim kapsamı (eşanlamlı/fuzzy-duyarlı; modality×positional ağırlıklı)
  Stuff — şişirme (keyword stuffing) cezası
  Parse_gate — biçim ayrıştırılabilirliği (TOPLAM değil, KAPI/çarpan)

Birleşik (DENETİM-DÜZELTMELİ):
  RAW   = α·Lex + β·Sem + γ·Cov − ζ·Stuff
  Score = clamp(Parse_gate × RAW, 0, 1)

Düzeltmeler (KURULUM-VE-BULGULAR M1–M3): alt-sınır kıskaçlama, Parse'ın kapı olması,
Lex/Cov bağımlılığının ağırlıkla dengelenmesi. SBERT yoksa β, α+γ'ya orantılı dağıtılır.

Bağımlılık: standart kütüphane zorunlu; sentence-transformers VARSA Sem hesaplanır.
"""

from __future__ import annotations

import math
from collections import Counter

from . import lexicons
from .bm25 import BM25
from .text import tokenize

# Önerilen varsayılan ağırlıklar (scoring-formulas.md ile birebir).
DEFAULTS = dict(alpha=0.35, beta=0.30, gamma=0.35, zeta=0.20, k1=1.5, b=0.75)

# Eşik yorumu (yüzde).
THRESHOLDS = {"target_low": 75, "target_high": 85, "overopt": 90, "serious": 50}


# ----------------------------- TF-IDF kosinüs -----------------------------

def tfidf_cosine(jd_tokens: list[str], cv_tokens: list[str], idf_fn) -> float:
    def vec(tokens):
        if not tokens:
            return {}
        tf = Counter(tokens)
        n = len(tokens)
        return {t: (c / n) * idf_fn(t) for t, c in tf.items()}

    a, b = vec(jd_tokens), vec(cv_tokens)
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


# ----------------------------- semantik (opsiyonel) -----------------------------

def sbert_cosine(jd_text: str, cv_text: str):
    """sentence-transformers VARSA çok-dilli SBERT kosinüsü [−1,1]; yoksa None."""
    try:
        from sentence_transformers import SentenceTransformer, util  # type: ignore
    except Exception:
        return None
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    emb = model.encode([jd_text, cv_text], convert_to_tensor=True, normalize_embeddings=True)
    return float(util.cos_sim(emb[0], emb[1]).item())


# ----------------------------- kapsam & şişirme -----------------------------

def coverage(must_have: list[str], cv_text: str, weights: dict | None = None,
             synonym_aware: bool = True) -> tuple[float, list[str]]:
    """
    Zorunlu terimlerin CV'de ağırlıklı kapsanma oranı + eksik (gap) listesi.
    synonym_aware=True iken birebir değil, eşanlamlı/varyant/fuzzy eşleşme de sayılır
    (Grammarly skill-normalization mantığı) — bu, ham substring'den daha gerçekçidir.
    """
    weights = weights or {}
    num = den = 0.0
    gap: list[str] = []
    for term in must_have:
        t = term.strip()
        w = weights.get(t.lower(), 1.0)
        den += w
        present = (
            lexicons.matches_semantically(t, cv_text)
            if synonym_aware
            else (t.lower() in cv_text.lower())
        )
        if present:
            num += w
        else:
            gap.append(term)
    cov = num / den if den else 0.0
    return cov, gap


def stuffing_penalty(cv_tokens: list[str], max_density: float = 0.05) -> float:
    """En sık içerik teriminin yoğunluğu eşiği aşarsa orantılı ceza [0,1]."""
    if not cv_tokens:
        return 0.0
    top, freq = Counter(cv_tokens).most_common(1)[0]
    d = freq / len(cv_tokens)
    if d <= max_density:
        return 0.0
    return min(1.0, (d - max_density) / max_density)


# ----------------------------- precision / recall / f1 -----------------------------

def prf(cv_text: str, must_have: list[str], cv_terms: list[str] | None = None) -> tuple[float, float, float]:
    """
    R  = Recall   = zorunluların kapsanma oranı (eksik must-have = gap → R düşer)
    P  = Precision = CV'de öne çıkarılan terimlerin ne kadarı zorunlularla ilgili
                     (cv_terms verilmezse must-have havuzu üzerinden kapsam-temelli proxy)
    F1 = harmonik ortalama
    Not: gerçek precision CV'nin tüm terim havuzunu ister; cv_terms ile geçilebilir.
    """
    M = [m.strip() for m in must_have if m.strip()]
    if not M:
        return 0.0, 0.0, 0.0
    hit = [m for m in M if lexicons.matches_semantically(m, cv_text)]
    R = len(hit) / len(M)
    if cv_terms:
        relevant = [t for t in cv_terms if lexicons.matches_semantically(t, " ".join(M))]
        P = len(relevant) / len(cv_terms) if cv_terms else 0.0
    else:
        P = R  # proxy: CV'nin sunduğu zorunlu-terim örtüşmesini ilgililik vekili say
    F1 = (2 * P * R / (P + R)) if (P + R) else 0.0
    return round(P, 3), round(R, 3), round(F1, 3)


# ----------------------------- hibrit skor -----------------------------

def ats_match_score(
    jd_text: str,
    cv_text: str,
    must_have: list[str],
    corpus_texts: list[str] | None = None,
    weights: dict | None = None,
    parse_gate: float = 1.0,
    lang_gate: float = 1.0,
    alpha: float = DEFAULTS["alpha"],
    beta: float = DEFAULTS["beta"],
    gamma: float = DEFAULTS["gamma"],
    zeta: float = DEFAULTS["zeta"],
    k1: float = DEFAULTS["k1"],
    b: float = DEFAULTS["b"],
    use_sbert: bool = True,
) -> dict:
    """
    Denetim-düzeltmeli hibrit ATS Match Score.
      RAW   = α·Lex + β·Sem + γ·Cov − ζ·Stuff
      Score = clamp(lang_gate × parse_gate × RAW, 0, 1)
    """
    jd_tok = tokenize(jd_text)
    cv_tok = tokenize(cv_text)

    docs = [jd_tok, cv_tok]
    if corpus_texts:
        docs += [tokenize(t) for t in corpus_texts]
    bm = BM25(docs, k1=k1, b=b)

    # Lex: unigram TF-IDF kosinüs — corpus yoksa muhafazakâr çıkar; skoru GÖRELİ oku.
    jd_uni = tokenize(jd_text, ngram_max=1)
    cv_uni = tokenize(cv_text, ngram_max=1)
    Lex = max(0.0, min(1.0, tfidf_cosine(jd_uni, cv_uni, bm.idf)))

    # Sem
    Sem = sbert_cosine(jd_text, cv_text) if use_sbert else None
    if Sem is not None:
        Sem = max(0.0, Sem)

    # Cov (eşanlamlı-duyarlı)
    Cov, gap = coverage(must_have, cv_text, weights)

    # Stuff
    Stuff = stuffing_penalty(cv_tok)

    # ağırlıklar — Sem yoksa β'yı α+γ'ya orantılı dağıt
    a, bb, g = alpha, beta, gamma
    if Sem is None:
        total = a + g
        a, g = a / total, g / total
        bb = 0.0
        sem_term = 0.0
    else:
        sem_term = bb * Sem

    RAW = a * Lex + sem_term + g * Cov - zeta * Stuff
    Score = max(0.0, min(1.0, lang_gate * parse_gate * RAW))

    P, R, F1 = prf(cv_text, must_have)
    pct = round(Score * 100, 1)
    return {
        "score_percent": pct,
        "verdict": _verdict(pct),
        "components": {
            "Lex": round(Lex, 3),
            "Sem": (round(Sem, 3) if Sem is not None else "yok (SBERT kurulu değil)"),
            "Cov": round(Cov, 3),
            "Parse_gate": parse_gate,
            "Stuffing": round(Stuff, 3),
        },
        "weights_used": {"alpha": round(a, 3), "beta": round(bb, 3), "gamma": round(g, 3), "zeta": zeta},
        "gap": gap,
        "precision": P,
        "recall": R,
        "f1": F1,
        "interpretation": "hedef %75-85 | >%90 şişirme sinyali | <%50 ciddi iyileştirme",
    }


def _verdict(pct: float) -> str:
    t = THRESHOLDS
    if pct >= t["overopt"]:
        return "AŞIRI OPTİMİZASYON ŞÜPHESİ (>%90) — şişirme/geri tepme riski"
    if pct >= t["target_low"]:
        return "MÜLAKATA HAZIR BANT (%75-85 hedef)"
    if pct >= t["serious"]:
        return "HEDEFİN ALTINDA — sentez (revizyon) turu önerilir"
    return "CİDDİ İYİLEŞTİRME GEREKİR (<%50)"
