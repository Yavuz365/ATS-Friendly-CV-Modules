"""
ats_engine.text — metin işleme katmanı.

Tokenizasyon, n-gram üretimi, çok-dilli (TR/EN) durak kelime filtresi ve
dil-kalitesi yardımcıları (pasif yapı / niceleme tespiti). Tüm üst katmanlar
(bm25, scoring, jd_parser, synthesis) bu modülün ürettiği token akışına dayanır.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import os
import re
from functools import lru_cache

# Türkçe karakterleri de kapsayan kelime tokenizeri.
_TOKEN = re.compile(r"[a-zA-ZçÇğĞıİöÖşŞüÜ0-9]+")

# Sayı / yüzde / para örüntüleri (niceleme tespiti için).
_QUANT = re.compile(r"(%\s?\d+([.,]\d+)?|\d+([.,]\d+)?\s?%|[$€₺£]\s?\d|\b\d{2,}\b|\b\d+([.,]\d+)?\s?(x|kat|adet|gün|saat|ay|yıl|day|days|month|months|year|years)\b)", re.IGNORECASE)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@lru_cache(maxsize=1)
def load_stopwords() -> frozenset[str]:
    """data/stopwords_tr_en.txt dosyasını yükler; bulunamazsa küçük bir gömülü sete düşer."""
    path = os.path.normpath(os.path.join(_DATA_DIR, "stopwords_tr_en.txt"))
    words: set[str] = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    words.add(line.lower())
    except FileNotFoundError:
        words = set(
            "ve veya ile için bir bu şu da de ki mi the a an and or for to of in on "
            "with as is are be by at from that this".split()
        )
    return frozenset(words)


def tokenize(text: str, ngram_max: int = 3, drop_stopwords: bool = True) -> list[str]:
    """
    Küçük harf + token + 1..ngram_max gram üretir.
    Çok-kelimeli kavramları (ör. 'tedarik zinciri yönetimi') n-gram olarak bütün yakalar —
    bu, ATS'lerin terimi parçalamadan eşlemesini taklit eder.
    """
    words = [w.lower() for w in _TOKEN.findall(text or "")]
    if drop_stopwords:
        stop = load_stopwords()
        words = [w for w in words if w not in stop]
    grams = list(words)
    for n in range(2, max(2, ngram_max) + 1):
        for i in range(len(words) - n + 1):
            grams.append(" ".join(words[i : i + n]))
    return grams


def sentences(text: str) -> list[str]:
    """Kaba cümle bölme (nokta/satır sonu). Pasif-yapı ve niceleme denetimleri için yeterli."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", (text or "").strip())
    return [p.strip(" •-\t") for p in parts if p.strip(" •-\t")]


def has_quantification(line: str) -> bool:
    """Satırda ölçülebilir bir sonuç (yüzde, sayı, para, süre) var mı? XYZ kuralının zorunlu şartı."""
    return bool(_QUANT.search(line or ""))


# Pasif yapı tespiti için sinyal: "edildi/yapıldı" eki (TR) ve "was/were + past participle" (EN, kaba).
_TR_PASSIVE = re.compile(r"\b\w+(ıldı|ildi|uldu|üldü|andı|endi|ınd[ıi]|inmiş|ülmüş)\b", re.IGNORECASE)
_EN_PASSIVE = re.compile(r"\b(was|were|been|being|is|are)\b\s+\w+(ed|en)\b", re.IGNORECASE)


def looks_passive(line: str) -> bool:
    """Heuristik pasif-yapı işareti. Sentez katmanında aktif fiile çevirme uyarısı için kullanılır."""
    return bool(_TR_PASSIVE.search(line or "") or _EN_PASSIVE.search(line or ""))


def density(tokens: list[str], term: str) -> float:
    """Bir terimin token akışındaki yoğunluğu [0,1]. Şişirme denetiminin temelidir."""
    if not tokens:
        return 0.0
    t = term.lower().strip()
    hits = sum(1 for x in tokens if x == t)
    return hits / len(tokens)
