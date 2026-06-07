#!/usr/bin/env python3
"""
ats_score.py — ATS CV Architect skorlama çekirdeği (Yol 2).

Bir iş ilanı (JD) ile bir CV arasındaki hibrit ATS Match Score'unu DETERMINISTIK
olarak hesaplar. LLM "tahmini skor" yerine gerçek sayı üretir.

Hesaplananlar:
  - TF-IDF kosinüs benzerliği
  - BM25 (Okapi) bazlı lexical eşleşme  (Lex)
  - Zorunlu terim kapsamı               (Cov)   [graded modality destekli]
  - Şişirme (keyword stuffing) cezası   (Stuff)
  - (opsiyonel) SBERT semantik benzerlik (Sem)  [sentence-transformers varsa]
  - Hibrit skor (denetim-düzeltmeli: parse KAPI olarak, 0-1'e kıskaçlı)
  - precision / recall / F1 + gap (kapatılabilir/kapatılamaz ayrımı çağıran tarafa)

Bağımlılık: yalnızca standart kütüphane zorunlu. numpy/scikit-learn/sentence-transformers
varsa kullanılır; yoksa saf-python yedeğe düşer.

Kullanım:
  python ats_score.py --jd jd.txt --cv cv.txt \
      --must "akreditif,incoterms,gtip,landed cost,kpi" \
      --corpus corpus_dir/   # opsiyonel; yoksa sadece JD+CV ile idf kabası

  # ya da modül olarak:
  from ats_score import ats_match_score
"""

import argparse
import math
import os
import re
from collections import Counter

# ----------------------------- metin işleme -----------------------------

_TOKEN = re.compile(r"[a-zA-ZçÇğĞıİöÖşŞüÜ0-9]+")

# küçük çok-dilli stop-word seti (genişletilebilir)
STOP = set("""
ve veya ile için bir bu şu da de ki mi mu çok daha en gibi olarak the a an and or for to of in on with as is are be by at from that this
""".split())


def tokenize(text, ngram_max=3):
    """küçük harf + token + 1..n gram. Çok kelimeli kavramları (n-gram) bütün yakalar."""
    words = [w.lower() for w in _TOKEN.findall(text or "")]
    words = [w for w in words if w not in STOP]
    grams = list(words)
    for n in range(2, ngram_max + 1):
        for i in range(len(words) - n + 1):
            grams.append(" ".join(words[i:i + n]))
    return grams


# ----------------------------- BM25 -----------------------------

class BM25:
    """Okapi BM25. corpus = list[list[token]]."""

    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.corpus = corpus
        self.N = len(corpus)
        self.avgdl = sum(len(d) for d in corpus) / max(1, self.N)
        self.df = Counter()
        for d in corpus:
            for t in set(d):
                self.df[t] += 1
        self.tf = [Counter(d) for d in corpus]

    def idf(self, term):
        # yumuşatılmış idf (negatif olmaz)
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query_tokens, doc_index):
        tf = self.tf[doc_index]
        dl = len(self.corpus[doc_index])
        s = 0.0
        for q in set(query_tokens):
            f = tf.get(q, 0)
            if f == 0:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += self.idf(q) * (f * (self.k1 + 1)) / denom
        return s

    def max_self_score(self, query_tokens):
        """Q'nun kendisini belge sayarak alabileceği teorik tavan (normalizasyon için)."""
        q = list(query_tokens)
        tmp = BM25([q], k1=self.k1, b=self.b)
        # idf'leri ana corpustan al ki ölçek tutarlı olsun
        tmp.idf = self.idf  # type: ignore
        return tmp.score(q, 0)


# ----------------------------- TF-IDF kosinüs -----------------------------

def tfidf_cosine(jd_tokens, cv_tokens, idf_fn):
    def vec(tokens):
        tf = Counter(tokens)
        return {t: (c / len(tokens)) * idf_fn(t) for t, c in tf.items()} if tokens else {}
    a, b = vec(jd_tokens), vec(cv_tokens)
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


# ----------------------------- semantik (opsiyonel) -----------------------------

def sbert_cosine(jd_text, cv_text):
    """sentence-transformers varsa SBERT kosinüsü; yoksa None döner."""
    try:
        from sentence_transformers import SentenceTransformer, util  # type: ignore
    except Exception:
        return None
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    emb = model.encode([jd_text, cv_text], convert_to_tensor=True, normalize_embeddings=True)
    return float(util.cos_sim(emb[0], emb[1]).item())


# ----------------------------- kapsam & şişirme -----------------------------

def coverage(must_have, cv_tokens, weights=None):
    """
    must_have: list[str]  (zorunlu terimler; çok kelimeli olabilir)
    weights:   dict term->float (modality*positional). Yoksa hepsi 1.0.
    CV'de geçen zorunlu terimlerin ağırlıklı oranı + gap listesi.
    """
    cv_set = set(cv_tokens)
    cv_text = " ".join(cv_tokens)
    weights = weights or {}
    num = den = 0.0
    gap = []
    for term in must_have:
        t = term.lower().strip()
        w = weights.get(t, 1.0)
        den += w
        present = (t in cv_set) or (t in cv_text)
        if present:
            num += w
        else:
            gap.append(term)
    cov = num / den if den else 0.0
    return cov, gap


def stuffing_penalty(cv_tokens, max_density=0.05):
    """En sık içerik teriminin yoğunluğu eşiği aşarsa orantılı ceza [0,1]."""
    if not cv_tokens:
        return 0.0
    c = Counter(cv_tokens)
    top, freq = c.most_common(1)[0]
    density = freq / len(cv_tokens)
    if density <= max_density:
        return 0.0
    return min(1.0, (density - max_density) / max_density)


# ----------------------------- precision / recall / f1 -----------------------------

def prf(cv_tokens, must_have):
    cv_set = set(cv_tokens)
    cv_text = " ".join(cv_tokens)
    M = set(m.lower().strip() for m in must_have)
    hit = set(m for m in M if (m in cv_set) or (m in cv_text))
    # precision: CV terimlerinin ne kadarı M ile ilgili (kaba: hit / benzersiz cv terim örtüşmesi)
    P = len(hit) / max(1, len(cv_set & M)) if (cv_set & M) else (len(hit) / max(1, len(M)))
    R = len(hit) / max(1, len(M))
    F1 = (2 * P * R / (P + R)) if (P + R) else 0.0
    return round(P, 3), round(R, 3), round(F1, 3)


# ----------------------------- hibrit skor -----------------------------

def ats_match_score(jd_text, cv_text, must_have, corpus_texts=None,
                    weights=None, parse_gate=1.0,
                    alpha=0.35, beta=0.30, gamma=0.35, zeta=0.20,
                    k1=1.5, b=0.75, use_sbert=True):
    """
    Denetim-düzeltmeli hibrit ATS Match Score.
      RAW   = alpha*Lex + beta*Sem + gamma*Cov - zeta*Stuff
      Score = clamp(parse_gate * RAW, 0, 1)
    Sem yoksa (SBERT yok) beta ağırlığı alpha+gamma'ya orantılı dağıtılır.
    """
    jd_tok = tokenize(jd_text)
    cv_tok = tokenize(cv_text)

    docs = [jd_tok, cv_tok]
    if corpus_texts:
        docs += [tokenize(t) for t in corpus_texts]
    bm = BM25(docs, k1=k1, b=b)

    # Lex: JD ile CV arasında TF-IDF KOSINÜS benzerliği (unigram) — standart, doğal [0,1].
    # NOT: idf gerçek bir corpus ister; corpus YOKSA (sadece JD+CV) idf dejenere olur ve
    # Lex muhafazakâr/düşük çıkar. Bu durumda skoru MUTLAK değil GÖRELİ oku (güçlü vs zayıf
    # ayrımı geçerlidir). Gerçek kalibrasyon için 50-100 ilanlık corpus + SBERT (Sem) gerekir.
    jd_uni, cv_uni = tokenize(jd_text, ngram_max=1), tokenize(cv_text, ngram_max=1)
    Lex = max(0.0, min(1.0, tfidf_cosine(jd_uni, cv_uni, bm.idf)))

    # Sem
    Sem = sbert_cosine(jd_text, cv_text) if use_sbert else None
    if Sem is not None:
        Sem = max(0.0, Sem)

    # Cov
    Cov, gap = coverage(must_have, cv_tok, weights)

    # Stuffing
    Stuff = stuffing_penalty(cv_tok)

    # ağırlıklar (Sem yoksa beta'yı yeniden dağıt)
    a, bb, g = alpha, beta, gamma
    if Sem is None:
        total = a + g
        a, g = a / total, g / total
        bb = 0.0
        sem_term = 0.0
    else:
        sem_term = bb * Sem

    RAW = a * Lex + sem_term + g * Cov - zeta * Stuff
    Score = max(0.0, min(1.0, parse_gate * RAW))

    P, R, F1 = prf(cv_tok, must_have)
    return {
        "score_percent": round(Score * 100, 1),
        "components": {
            "Lex": round(Lex, 3),
            "Sem": (round(Sem, 3) if Sem is not None else "yok (SBERT kurulu değil)"),
            "Cov": round(Cov, 3),
            "Parse_gate": parse_gate,
            "Stuffing": round(Stuff, 3),
        },
        "weights_used": {"alpha": round(a, 3), "beta": round(bb, 3), "gamma": round(g, 3), "zeta": zeta},
        "gap": gap,
        "precision": P, "recall": R, "f1": F1,
        "interpretation": ("hedef %75-85 | >%90 şişirme sinyali | <%50 ciddi iyileştirme"),
    }


# ----------------------------- CLI -----------------------------

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="ATS hibrit match score (denetim-düzeltmeli)")
    ap.add_argument("--jd", required=True, help="iş ilanı metin dosyası")
    ap.add_argument("--cv", required=True, help="CV metin dosyası")
    ap.add_argument("--must", default="", help="zorunlu terimler, virgülle ayrık")
    ap.add_argument("--corpus", default=None, help="opsiyonel corpus klasörü (.txt'ler)")
    ap.add_argument("--parse-gate", type=float, default=1.0, help="biçim kapısı 0.6-1.0")
    ap.add_argument("--no-sbert", action="store_true", help="semantik katmanı atla")
    args = ap.parse_args()

    corpus = None
    if args.corpus and os.path.isdir(args.corpus):
        corpus = [_read(os.path.join(args.corpus, f))
                  for f in os.listdir(args.corpus) if f.endswith(".txt")]

    must = [m.strip() for m in args.must.split(",") if m.strip()]
    res = ats_match_score(_read(args.jd), _read(args.cv), must,
                          corpus_texts=corpus, parse_gate=args.parse_gate,
                          use_sbert=not args.no_sbert)

    import json
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
