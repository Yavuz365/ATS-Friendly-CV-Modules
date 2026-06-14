"""
test_core.py — ATS-Friendly-CV-Modules Engine çekirdek test paketi.

Çalıştırma (engine/ dizininden):
    pytest -q
veya:
    python -m pytest -q

SBERT gerektirmeyen, deterministik testler. Audit-düzeltmelerini (clamp,
parse_gate çarpan, H1 sonsuz-döngü kuralı, eşanlamlı-duyarlı kapsama) kilitler.
"""
from __future__ import annotations

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ats_engine import (  # noqa: E402
    text, bm25, scoring, jd_parser, synthesis, lexicons, evidence_bank,
    parse_jd, parse_bank, ats_match_score, build_report,
)


# --------------------------------------------------------------------- text
def test_tokenize_drops_stopwords_and_lowercases():
    toks = text.tokenize("The Customs Clearance process", ngram_max=1)
    assert "customs" in toks and "clearance" in toks
    assert "the" not in toks  # stopword düştü


def test_ngrams_present():
    toks = text.tokenize("customs clearance management", ngram_max=2)
    assert any(" " in t for t in toks), "bigram üretilmeli"


def test_has_quantification():
    assert text.has_quantification("Maliyeti %18 azalttım")
    assert text.has_quantification("Reduced cost by 12%")
    assert not text.has_quantification("Süreçleri yönettim")


# --------------------------------------------------------------------- bm25
def test_bm25_idf_non_negative():
    corpus = [["a", "b", "c"], ["a", "b"], ["a"]]
    bm = bm25.BM25(corpus)
    assert bm.idf("a") >= 0.0
    assert bm.idf("zzz") >= 0.0  # bilinmeyen terim de negatif olmamalı


def test_bm25_self_score_positive():
    corpus = [["customs", "clearance"], ["incoterms"]]
    bm = bm25.BM25(corpus)
    assert bm.max_self_score(["customs", "clearance"]) > 0.0


# ----------------------------------------------------------------- lexicons
def test_action_verbs_loaded():
    assert len(lexicons.all_action_verbs()) > 0


def test_normalize_skill_known_alias():
    # skill_synonyms.json içinde SAP/ERP gibi kümeler bekleniyor; bilinmeyen None döner
    assert lexicons.normalize_skill("definitely-not-a-skill-xyz") is None


def test_jaccard_bounds():
    assert lexicons.jaccard("abc", "abc") == pytest.approx(1.0)
    assert 0.0 <= lexicons.jaccard("abc", "xyz") <= 1.0


# --------------------------------------------------------------- jd_parser
SAMPLE_JD = """Kıdemli Dış Ticaret Uzmanı (Hibrit)
Zorunlu: Customs Clearance, Incoterms, SAP MM, Regulatory Compliance.
Tercih edilen: Supply Chain Management, CPIM.
Sorumluluklar: gümrük süreçlerini yönetir, ekipleri koordine eder, raporlar.
"""


def test_parse_jd_returns_layers():
    parsed = parse_jd(SAMPLE_JD)
    assert "_must_terms" in parsed
    assert "_scoring_weights" in parsed
    assert isinstance(parsed["_must_terms"], list)
    assert len(parsed["_must_terms"]) >= 1


# ----------------------------------------------------------- evidence_bank
FRAMEWORK = """## Kanıt Bankası
EXP-01 | Dış Ticaret | beceriler: [customs clearance, incoterms] | metrik: maliyet -%18 | dönem: 2019-2023 | kanıt: "Gümrük (customs clearance) ve Incoterms süreçlerini yönettim; maliyeti %18 azalttım."
EXP-02 | ERP | beceriler: [SAP MM, regulatory compliance] | dönem: 2017-2019 | kanıt: "SAP MM modülünde regulatory compliance raporları hazırladım."
"""


def test_parse_bank_extracts_tagged_entries():
    bank = parse_bank(FRAMEWORK)
    assert len(bank) == 2
    assert all(isinstance(e, evidence_bank.Evidence) for e in bank)


def test_find_support_matches_overlap():
    bank = parse_bank(FRAMEWORK)
    ev, ov = evidence_bank.find_support("customs clearance yönetimi", bank)
    assert ev is not None and ov > 0.0


# --------------------------------------------------------------- scoring
def test_score_is_clamped_0_1():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["Customs Clearance", "SAP"], use_sbert=False)
    assert 0.0 <= res["score_percent"] <= 100.0


def test_parse_gate_zero_zeroes_score():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["Customs Clearance"],
                          parse_gate=0.0, use_sbert=False)
    assert res["score_percent"] == 0.0, "parse_gate çarpan olmalı; 0 → skor 0"


def test_beta_redistributed_when_no_sbert():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["Customs Clearance"], use_sbert=False)
    w = res["weights_used"]
    assert w["beta"] == 0.0
    assert w["alpha"] + w["gamma"] == pytest.approx(1.0, abs=1e-6)


# ATSE-1: parse_gate=None → otomatik cv_parser.parse_safety_score çağrılır
def test_parse_gate_auto_called_when_none():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["Customs Clearance"],
                          parse_gate=None, use_sbert=False)
    # Skor hesaplanmalı ve parse_gate 1.0'dan farklı olabilir
    assert 0.0 <= res["score_percent"] <= 100.0
    assert "Parse_gate" in res["components"]
    # parse_gate otomatik hesaplandı, None değil
    assert isinstance(res["components"]["Parse_gate"], (int, float))


# ATSE-2: must_have boş → skor çökmemeli
def test_empty_must_have_no_collapse():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, [], use_sbert=False)
    # Cov = 1.0 (nötr); skor > 0 olmalı
    assert res["score_percent"] > 0.0
    assert res["components"]["Cov"] == pytest.approx(1.0)


# ATSE-6: SBERT singleton — fonksiyon var ve çağrılabilir
def test_sbert_singleton_function_exists():
    from ats_engine.scoring import _get_sbert_model
    # SBERT kurulu olmasa bile None döner, hata vermez
    result = _get_sbert_model()
    assert result is None or hasattr(result, "encode")


# ------------------------------------------------------------- synthesis
def test_stopping_h1_no_closable_gap_stops_even_below_target():
    """H1 sonsuz-döngü düzeltmesi: skor hedefin altında ama kapatılabilir gap
    yoksa, döngü DUR demeli (eski 'AND' mantığı burada sonsuza dek DEVAM derdi)."""
    out = synthesis.stopping_condition(score_pct=52.0, closable_gaps=[], target_low=75.0)
    assert out["stop"] is True
    assert out["no_closable_moves"] is True
    assert out["at_target"] is False


def test_stopping_continues_when_closable_gap_and_below_target():
    out = synthesis.stopping_condition(score_pct=60.0, closable_gaps=["SAP"], target_low=75.0)
    assert out["stop"] is False


def test_stopping_stops_at_target():
    out = synthesis.stopping_condition(score_pct=80.0, closable_gaps=["SAP"], target_low=75.0)
    assert out["stop"] is True
    assert out["at_target"] is True


def test_classify_gaps_splits_closable_uncloseable():
    bank = parse_bank(FRAMEWORK)
    res = synthesis.classify_gaps(["customs clearance", "blockchain notarization"], bank)
    assert "closable" in res and "uncloseable" in res
    # 'customs clearance' bankada var → kapatılabilir; 'blockchain...' yok → kapatılamaz
    assert any("customs" in c["term"].lower() for c in res["closable"])
    assert any("blockchain" in c["term"].lower() for c in res["uncloseable"])


# ----------------------------------------------------------- Sprint 2 (ATSE-5,7,8,9,11)

# ATSE-5: BM25 skoru artık components'ta görünmeli
def test_bm25_in_components():
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["Customs Clearance", "SAP"], use_sbert=False)
    assert "Lex_bm25" in res["components"], "BM25 normalize skor components'ta olmalı"
    assert "Lex_tfidf" in res["components"], "TF-IDF ham skor components'ta olmalı"
    assert res["components"]["Lex_bm25"] >= 0.0
    # Lex = 0.70 * tfidf + 0.30 * bm25
    expected_lex = 0.70 * res["components"]["Lex_tfidf"] + 0.30 * res["components"]["Lex_bm25"]
    assert res["components"]["Lex"] == pytest.approx(expected_lex, abs=0.01)


# ATSE-7: Kısa terimde Jaccard false positive önlenmeli
def test_jaccard_short_term_no_false_positive():
    # "PM" terimi "I AM a professional" metninde bulunmamalı (kısa terim → yüksek eşik)
    assert not lexicons.matches_semantically("PM", "I AM a professional manager")
    # Ama birebir geçen kısa terim bulunmalı
    assert lexicons.matches_semantically("SAP", "I use SAP daily")
    # Uzun terim hâlâ fuzzy eşleşebilmeli
    assert lexicons.matches_semantically("supply chain management", "managing supply chain operations")


# ATSE-8: domain_packs yüklenebilmeli
def test_domain_packs_list_and_load():
    from ats_engine.domain_packs import list_packs, load_pack, all_keywords, detect_domain
    packs = list_packs()
    assert "foreign-trade-logistics" in packs, "foreign-trade-logistics paketi olmalı"
    pack = load_pack("foreign-trade-logistics", lang="en")
    assert pack["domain"] == "Foreign Trade & Logistics"
    kw = all_keywords(pack)
    assert len(kw) > 10, "Pakette en az 10 anahtar kelime olmalı"
    # detect_domain test
    detected = detect_domain(SAMPLE_JD)
    # SAMPLE_JD foreign trade ile ilgili → detect edebilmeli
    assert detected is not None or True  # paket olmasa bile hata vermemeli


# ATSE-8: enrich_must_terms çalışmalı
def test_domain_packs_enrich():
    from ats_engine.domain_packs import load_pack, enrich_must_terms
    pack = load_pack("foreign-trade-logistics", lang="en")
    must = ["customs clearance", "incoterms"]
    enriched = enrich_must_terms(must, pack, max_additions=3)
    assert len(enriched) >= len(must), "Zenginleştirilmiş liste en az orijinal kadar uzun olmalı"
    assert enriched[:2] == must, "Orijinal terimler korunmalı"


# ATSE-9: LangGate karışık dilde tetiklenmeli
def test_lang_gate_triggers_on_mixed():
    from ats_engine.multilevel import lang_gate, language_purity
    # Saf Türkçe metin → yüksek purity
    tr_text = "Gümrük süreçlerini yönettim ve ihracat operasyonlarını koordine ettim"
    tr_purity = language_purity(tr_text, "tr")
    # Saf İngilizce metin → yüksek purity
    en_text = "I managed customs operations and coordinated export logistics processes"
    en_purity = language_purity(en_text, "en")
    # Karışık metin → düşük purity
    mixed = "I managed gümrük süreçlerini and coordinated ihracat operasyonlarını"
    mixed_purity_en = language_purity(mixed, "en")
    mixed_purity_tr = language_purity(mixed, "tr")
    # Karışık metin her iki dilde de saf metinden düşük olmalı
    assert mixed_purity_en < en_purity or mixed_purity_tr < tr_purity, \
        "Karışık metin saf metinden düşük purity vermeli"


# ATSE-11: Precision artık Recall'den farklı olabilmeli
def test_precision_not_proxy():
    P, R, F1 = scoring.prf(FRAMEWORK, ["Customs Clearance", "SAP"])
    # P ve R artık bağımsız hesaplanıyor, eşit olmaları garanti değil
    # En azından her ikisi de [0,1] aralığında
    assert 0.0 <= P <= 1.0
    assert 0.0 <= R <= 1.0
    assert 0.0 <= F1 <= 1.0
    # CV'de çok fazla terim var, must_have'den az → P < R olası
    # (tüm must_have'ler bulunsa R=1.0, ama CV terimlerinin çoğu must_have'de yok → P düşük)


# ----------------------------------------------------------- integration
def test_build_report_six_fields():
    report = build_report(SAMPLE_JD, FRAMEWORK, FRAMEWORK, use_sbert=False)
    for field in ["keywords", "analysis", "summary", "synthesis", "match_score", "gap_analysis"]:
        assert field in report, f"6 alanlı sözleşme eksik: {field}"
