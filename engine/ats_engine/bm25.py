"""
ats_engine.bm25 — Okapi BM25 sözcüksel skorlama çekirdeği.

BM25, klasik TF-IDF'in fiili-standart türevidir (Elasticsearch / Lucene). İki kritik
parametresi vardır:
  - k1 (doyum): tekrar eden terimin katkısını asimptotik bir sınıra (k1+1) bağlar →
    'keyword stuffing' matematiksel olarak işe yaramaz.
  - b   (uzunluk normalizasyonu): aynı terimi içeren iki belgeden kısa/öz olanı ödüllendirir.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import math
from collections import Counter


class BM25:
    """Okapi BM25. corpus = list[list[token]] (her belge önceden tokenize edilmiş)."""

    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.corpus = corpus
        self.N = len(corpus)
        self.avgdl = sum(len(d) for d in corpus) / max(1, self.N)
        self.df: Counter[str] = Counter()
        for d in corpus:
            for t in set(d):
                self.df[t] += 1
        self.tf = [Counter(d) for d in corpus]

    def idf(self, term: str) -> float:
        """Yumuşatılmış IDF (negatif olmaz): log(1 + (N - n + 0.5)/(n + 0.5))."""
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query_tokens: list[str], doc_index: int) -> float:
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

    def max_self_score(self, query_tokens: list[str]) -> float:
        """
        Sorgunun kendisini belge sayarak alabileceği teorik tavan — normalizasyon paydası.
        IDF'leri ana corpustan alır ki ölçek tutarlı kalsın.
        """
        q = list(query_tokens)
        tmp = BM25([q], k1=self.k1, b=self.b)
        tmp.idf = self.idf  # type: ignore[method-assign]
        return tmp.score(q, 0)
