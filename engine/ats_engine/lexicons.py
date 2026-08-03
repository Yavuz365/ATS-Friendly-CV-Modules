"""
ats_engine.lexicons — Grammarly-türevli dil varlıkları.

İki veri dosyasını yükler ve operasyonel hale getirir:
  - data/action_verbs.json   → aktif eylem fiili kütüphanesi (XYZ cümle açılışı + pasif tespiti)
  - data/skill_synonyms.json → beceri normalizasyonu + LSI/eşanlamlı tohum haritası (TR/EN)

Bu, Grammarly Resume Builder'ın 'Skill Normalization', 'Synonym & Semantic Matching' ve
'Action Verbs Library' yeteneklerinin hafif, deterministik karşılığıdır. SBERT yoksa
semantik eşleşmenin yerini kısmen bu sözlük + fuzzy eşleşme tutar.

DÜRÜSTLÜK NOTU: expand_lsi() yalnızca *eşleşmeyi anlamak* içindir; adayda gerçekten
karşılığı olmayan hiçbir varyant CV'ye doldurulmaz (bkz. synthesis-rules).

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import json
import os
import re
from functools import lru_cache

# P0-5 fix (packaging): veri artık paketin İÇİNDE (ats_engine/data/), bir üst
# dizinde değil. Eski "../data" yolu yalnızca kaynak-kontrolünden çalışırken
# işe yarıyordu; `pip install` ile kurulan wheel'de bu dizin hiç yoktu
# (clean-room testte doğrulandı: FileNotFoundError). Artık __file__'ın kendi
# dizini kullanılıyor — hem dev-mode hem kurulu pakette çalışır.
_DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "data"))


@lru_cache(maxsize=1)
def _load_action_verbs() -> dict:
    path = os.path.join(_DATA_DIR, "action_verbs.json")
    with open(path, encoding="utf-8") as f:
        data: dict = json.load(f)
        return data


@lru_cache(maxsize=1)
def _load_synonyms() -> dict:
    path = os.path.join(_DATA_DIR, "skill_synonyms.json")
    with open(path, encoding="utf-8") as f:
        data: dict = json.load(f)
        return data


@lru_cache(maxsize=1)
def all_action_verbs() -> frozenset[str]:
    """Tüm kategorilerdeki fiillerin düz kümesi (pasif/zayıf-açılış denetimi için)."""
    data = _load_action_verbs()
    verbs: set[str] = set()
    for key, vals in data.items():
        if key.startswith("_"):
            continue
        # Y36-10: action_verbs artık dict (cliche_risk etiketli) veya str olabilir
        for v in vals:
            verb_str = v["verb"] if isinstance(v, dict) else v
            verbs.add(verb_str.lower())
    return frozenset(verbs)


def cliche_verbs() -> frozenset[str]:
    """Klişe/AI-tetikleyici olarak işaretlenmiş fiillerin kümesi."""
    data = _load_action_verbs()
    cliches: set[str] = set()
    for key, vals in data.items():
        if key.startswith("_"):
            continue
        for v in vals:
            if isinstance(v, dict) and v.get("cliche_risk"):
                cliches.add(v["verb"].lower())
    # Meta'daki cliche_verbs listesinden de ekle
    meta = data.get("_meta", {})
    for cv in meta.get("cliche_verbs", []):
        cliches.add(cv.lower())
    return frozenset(cliches)


# P0-3 fix: intent isimleri (leadership/achievement/...) ile JSON'daki gerçek
# anahtarlar (en_tier1_impact, en_tier2_leadership, ...) hiç örtüşmüyordu →
# action_verbs_by_intent() HER ZAMAN [] dönüyor, synthesis.py sessizce sabit
# "achieved" fiiline düşüyordu (bkz. synthesis.build_xyz). Bu eşleme tabloyu
# gerçek veri anahtarlarına bağlar; her intent en az bir gerçek kategoriye gider.
_INTENT_TO_KEY = {
    "leadership": "en_tier2_leadership",
    "achievement": "en_tier1_impact",
    "improvement": "en_tier1_impact",
    "growth": "en_tier1_impact",
    "reduction": "en_tier1_impact",
    "creation": "en_tier1_impact",
    "analysis": "en_tier3_operational",
    "negotiation": "en_tier1_impact",
    "operations": "en_tier3_operational",
    "communication": "en_tier3_operational",
}


def action_verbs_by_intent(intent: str) -> list[str]:
    """
    Bir niyet/etki kategorisine uygun fiilleri döndürür.
    intent ∈ {leadership, achievement, improvement, growth, reduction, creation,
              analysis, negotiation, operations, communication}

    P0-3 fix: bkz. yukarıdaki not — artık _INTENT_TO_KEY üzerinden gerçek JSON
    anahtarına eşlenir; bilinmeyen/boş intent → en_tier1_impact (genel başarı havuzu).
    """
    data = _load_action_verbs()
    key = _INTENT_TO_KEY.get(intent, "en_tier1_impact")
    vals = data.get(key) or data.get("en_tier1_impact", [])
    return [v["verb"] if isinstance(v, dict) else v for v in vals]


@lru_cache(maxsize=1)
def _variant_index() -> dict[str, str]:
    """varyant(string, küçük harf) -> kanonik anahtar. Normalizasyonun tersine-indeksi."""
    syn = _load_synonyms()
    idx: dict[str, str] = {}
    for key, entry in syn.items():
        if key.startswith("_"):
            continue
        idx[entry["canonical"].lower()] = key
        idx[key.replace("_", " ")] = key
        for v in entry.get("variants", []):
            idx[v.lower()] = key
    return idx


def normalize_skill(term: str) -> str | None:
    """
    Bir terimi kanonik beceri etiketine indirger (ör. 'sap mm' -> 'ERP',
    'user retention' -> 'Customer Retention'). Eşleşme yoksa None.
    """
    syn = _load_synonyms()
    idx = _variant_index()
    key = idx.get((term or "").lower().strip())
    if not key:
        return None
    canonical: str = syn[key]["canonical"]
    return canonical


def expand_lsi(term: str) -> list[str]:
    """
    Bir terimin LSI/eşanlamlı varyant kümesini döndürür (eşleşmeyi ANLAMAK için).
    'tedarik zinciri' -> ['supply chain', 'scm', 'logistics', ...]
    """
    syn = _load_synonyms()
    idx = _variant_index()
    key = idx.get((term or "").lower().strip())
    if not key:
        return []
    entry = syn[key]
    out = [entry["canonical"], *entry.get("variants", [])]
    # girdinin kendisini tekrar etme
    low = (term or "").lower().strip()
    return [t for t in dict.fromkeys(out) if t.lower() != low]


def jaccard(a: str, b: str) -> float:
    """
    Token-kümesi Jaccard benzerliği [0,1] — 'fuzzy matching' için hafif ölçü
    (Grammarly'nin Jaccard/Levenshtein yaklaşımının basit karşılığı).
    'team management' ↔ 'led a cross-functional team' gibi kısmi örtüşmeleri yakalar.
    """
    sa = set((a or "").lower().split())
    sb = set((b or "").lower().split())
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union else 0.0


def _word_boundary_contains(term: str, text: str) -> bool:
    """
    P0-2 fix: eskiden düz `term in text` substring kontrolü yapılıyordu — bu,
    "sap" teriminin "sapphire" içinde (yanlış pozitif) eşleşmesine yol açıyordu.
    Artık kelime sınırı kontrolü var: önceki/sonraki karakter \\w (harf/rakam/_)
    OLMAMALI. Örn. "sap-mm" içinde "sap" hâlâ eşleşir (sonrası '-' \\w değil),
    ama "sapphire" içinde eşleşmez (sonrası 'p' \\w).
    """
    if not term:
        return False
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return re.search(pattern, text) is not None


def matches_semantically(term: str, text: str, threshold: float | None = None) -> bool:
    """
    term, metinde ya birebir/varyant olarak ya da kanonik kök üzerinden ya da
    fuzzy (Jaccard) eşik üzerinden geçiyor mu? jd_parser/synthesis kapsam denetiminde kullanılır.

    ATSE-7 fix: Jaccard eşiği artık terim uzunluğuna göre dinamik.
    Kısa terimler (1 kelime) → 0.80 eşik (kısa terimlerde false positive önlenir)
    2 kelime → 0.50
    3+ kelime → 0.34 (eski varsayılan)
    threshold parametresi verilirse o kullanılır (override).
    """
    low_text = (text or "").lower()
    low_term = (term or "").lower().strip()
    if not low_term:
        return False
    if _word_boundary_contains(low_term, low_text):
        return True
    # varyantlardan herhangi biri geçiyor mu?
    for variant in [low_term] + [v.lower() for v in expand_lsi(low_term)]:
        if variant and _word_boundary_contains(variant, low_text):
            return True
    # ATSE-7 fix: dinamik eşik — kısa terimlerde false positive önlenir.
    term_word_count = len(low_term.split())
    if threshold is None:
        if term_word_count <= 1:
            threshold = 0.80  # tek kelime → neredeyse tam eşleşme gerekli
        elif term_word_count == 2:
            threshold = 0.50  # iki kelime → makul örtüşme
        else:
            threshold = 0.34  # 3+ kelime → eski varsayılan
    # fuzzy: metnin pencerelerine karşı Jaccard
    words = low_text.split()
    n = len(low_term.split())
    for i in range(0, max(1, len(words) - n + 1)):
        window = " ".join(words[i : i + n])
        if jaccard(low_term, window) >= threshold:
            return True
    return False
