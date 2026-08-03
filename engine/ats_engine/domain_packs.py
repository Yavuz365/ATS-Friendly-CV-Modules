"""
ats_engine.domain_packs — Alan-özel anahtar kelime paketi yükleyici.

ATSE-8 fix: domain-packs/ dizinindeki JSON dosyaları artık kodda kullanılıyor.
Bu modül, alan paketlerini yükler ve jd_parser/scoring ile entegre eder.

Kullanım:
    from ats_engine.domain_packs import load_pack, list_packs, enrich_must_terms

    pack = load_pack("foreign-trade-logistics", lang="en")
    enriched = enrich_must_terms(must_terms, pack)

Her paket JSON formatında:
    {"domain": str, "language": str, "categories": {cat: [keyword, ...]}}

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache

# P0-5 fix (packaging): domain-packs/ eskiden repo KÖKÜNDE (engine/'in bile
# dışında) idi — hiçbir wheel/sdist bunu paketleyemezdi (paket ağacının tamamen
# dışında). Artık ats_engine/domain_pack_data/ içine taşındı; dizin adı
# domain_packs.py modülüyle çakışmasın diye "domain_pack_data" seçildi.
_PACKS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "domain_pack_data")
)


def list_packs() -> list[str]:
    """Mevcut alan paketi adlarını listeler (dizin adları)."""
    if not os.path.isdir(_PACKS_DIR):
        return []
    return sorted(
        d for d in os.listdir(_PACKS_DIR)
        if os.path.isdir(os.path.join(_PACKS_DIR, d)) and not d.startswith(".")
    )


@lru_cache(maxsize=16)
def load_pack(pack_name: str, lang: str = "en") -> dict:
    """
    Bir alan paketini yükler.

    Args:
        pack_name: Paket adı (ör. "foreign-trade-logistics")
        lang: Dil kodu ("en" veya "tr")

    Returns:
        {"domain": str, "language": str, "categories": {cat: [keyword, ...]}}

    Raises:
        FileNotFoundError: Paket veya dil dosyası bulunamazsa.
    """
    pack_dir = os.path.join(_PACKS_DIR, pack_name)
    if not os.path.isdir(pack_dir):
        raise FileNotFoundError(f"Domain pack bulunamadı: {pack_name}")

    filename = f"keywords_{lang}.json"
    filepath = os.path.join(pack_dir, filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Dil dosyası bulunamadı: {filename} ({pack_name} paketi)"
        )

    with open(filepath, encoding="utf-8") as f:
        pack: dict = json.load(f)
        return pack


def all_keywords(pack: dict) -> list[str]:
    """Paketteki tüm kategorilerdeki anahtar kelimeleri düz liste olarak döndürür."""
    keywords: list[str] = []
    categories = pack.get("categories", {})
    for _cat, terms in categories.items():
        if isinstance(terms, list):
            keywords.extend(terms)
    return keywords


def keywords_by_category(pack: dict) -> dict[str, list[str]]:
    """Kategorilere göre ayrılmış anahtar kelime sözlüğü."""
    return dict(pack.get("categories", {}))


def enrich_must_terms(
    must_terms: list[str],
    pack: dict,
    max_additions: int = 5,
) -> list[str]:
    """
    Mevcut zorunlu terimleri alan paketiyle zenginleştirir.

    Mantık: must_terms'teki terimlerle aynı kategoride bulunan ama listede
    olmayan terimleri önerir (en fazla max_additions kadar).

    Args:
        must_terms: Mevcut zorunlu terimler
        pack: load_pack() çıktısı
        max_additions: Eklenecek maksimum terim sayısı

    Returns:
        Zenginleştirilmiş terim listesi (orijinaller + önerilen ekler)
    """
    must_lower = {t.lower() for t in must_terms}
    categories = pack.get("categories", {})

    # must_terms'teki terimlerin hangi kategorilere düştüğünü bul
    matched_categories: set[str] = set()
    for cat, terms in categories.items():
        terms_lower = {t.lower() for t in terms}
        if must_lower & terms_lower:
            matched_categories.add(cat)

    # Eşleşen kategorilerden must_terms'te olmayan terimleri topla
    suggestions: list[str] = []
    for cat in matched_categories:
        for term in categories.get(cat, []):
            if term.lower() not in must_lower and term not in suggestions:
                suggestions.append(term)

    enriched = list(must_terms) + suggestions[:max_additions]
    return enriched


def detect_domain(text: str, threshold: float = 0.10) -> str | None:
    """
    Bir metin (JD) için en uygun alan paketini otomatik tespit eder.

    Yöntem: Her paketin anahtar kelimelerinin metinde kaçı geçiyor → oran en
    yüksek ve threshold'u geçen paket seçilir.

    Returns:
        Paket adı (str) veya None (hiçbiri eşleşmezse).
    """
    text_lower = (text or "").lower()
    if not text_lower.strip():
        return None

    best_name: str | None = None
    best_ratio: float = 0.0

    for pack_name in list_packs():
        try:
            # Önce İngilizce dene, yoksa Türkçe
            try:
                pack = load_pack(pack_name, lang="en")
            except FileNotFoundError:
                pack = load_pack(pack_name, lang="tr")
        except FileNotFoundError:
            continue

        keywords = all_keywords(pack)
        if not keywords:
            continue

        hits = sum(1 for kw in keywords if kw.lower() in text_lower)
        ratio = hits / len(keywords)

        if ratio > best_ratio:
            best_ratio = ratio
            best_name = pack_name

    return best_name if best_ratio >= threshold else None
