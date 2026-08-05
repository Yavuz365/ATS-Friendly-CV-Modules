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
from functools import lru_cache
from importlib.resources import files

from .errors import ResourceMissingError


# P0-5 fix (packaging): domain-packs/ eskiden repo KÖKÜNDE (engine/'in bile
# dışında) idi — hiçbir wheel/sdist bunu paketleyemezdi (paket ağacının tamamen
# dışında). Artık ats_engine/domain_pack_data/ içine taşındı; dizin adı
# domain_packs.py modülüyle çakışmasın diye "domain_pack_data" seçildi.
def _packs_root():
    return files("ats_engine").joinpath("domain_pack_data")


def list_packs() -> list[str]:
    """Mevcut alan paketi adlarını listeler (dizin adları)."""
    root = _packs_root()
    try:
        return sorted(item.name for item in root.iterdir() if item.is_dir() and not item.name.startswith("."))
    except FileNotFoundError as exc:
        raise ResourceMissingError(
            "Domain pack kökü paket artefaktında bulunamadı; boş liste fallback'i uygulanmadı.",
            field="ats_engine/domain_pack_data",
        ) from exc


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
    filename = f"keywords_{lang}.json"
    resource = _packs_root().joinpath(pack_name).joinpath(filename)
    try:
        with resource.open("r", encoding="utf-8") as f:
            pack: dict = json.load(f)
            return pack
    except FileNotFoundError as exc:
        raise ResourceMissingError(
            f"Domain pack kaynağı bulunamadı: {pack_name}/{filename}",
            field=f"ats_engine/domain_pack_data/{pack_name}/{filename}",
        ) from exc


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
            except (FileNotFoundError, ResourceMissingError):
                pack = load_pack(pack_name, lang="tr")
        except (FileNotFoundError, ResourceMissingError):
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
