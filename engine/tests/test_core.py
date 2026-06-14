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


# ----------------------------------------------------------- integration
def test_build_report_six_fields():
    report = build_report(SAMPLE_JD, FRAMEWORK, FRAMEWORK, use_sbert=False)
    for field in ["keywords", "analysis", "summary", "synthesis", "match_score", "gap_analysis"]:
        assert field in report, f"6 alanlı sözleşme eksik: {field}"
