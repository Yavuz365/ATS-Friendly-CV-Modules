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
    ats_match_score,
    bm25,
    build_report,
    evidence_bank,
    lexicons,
    parse_bank,
    parse_jd,
    scoring,
    synthesis,
    text,
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


# P0-2 fix: "SAP" kelime-sınırı olmadan "sapphire" içinde yanlış eşleşiyordu
def test_matches_semantically_word_boundary_no_false_positive():
    assert not lexicons.matches_semantically("SAP", "I love sapphire gemstones")
    assert lexicons.matches_semantically("SAP", "I use SAP daily for ERP work")
    # tireli terimlerde de sınır doğru çalışmalı
    assert lexicons.matches_semantically("sap", "customs-cleared via sap-mm module")


# P0-3 fix: action_verbs_by_intent artık gerçek JSON anahtarlarına eşleniyor (hiçbir zaman [] değil)
def test_action_verbs_by_intent_never_empty_for_known_intents():
    for intent in ["leadership", "achievement", "improvement", "growth", "reduction",
                   "creation", "analysis", "negotiation", "operations", "communication"]:
        verbs = lexicons.action_verbs_by_intent(intent)
        assert len(verbs) > 0, f"intent={intent} için boş liste dönmemeli"
    # bilinmeyen intent de genel havuza (en_tier1_impact) düşmeli, boş dönmemeli
    assert len(lexicons.action_verbs_by_intent("unknown-intent-xyz")) > 0


def test_synthesis_build_xyz_uses_real_verb_not_always_achieved():
    # P0-3 fix'ten önce her intent sessizce "achieved"e düşüyordu.
    sentence_leadership = synthesis.build_xyz("ekip performansı", "%20 verimlilik", "haftalık 1:1'lerle", intent="leadership")
    assert "(" in sentence_leadership  # fiil parantez içinde raporlanıyor
    # leadership havuzundan (managed/led/directed/...) bir fiil gelmeli, achieved DEĞİL
    assert "(achieved)" not in sentence_leadership


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
    # P0-10 fix: SAMPLE_JD'de açık "Zorunlu:" başlığı var → source "explicit" olmalı
    assert parsed["must_have_source"] == "explicit"
    assert all(m["modality"] == 1.0 for m in parsed["must_have"])


# P0-8 fix: dil adı + seviye kodu artık eşleştiriliyor (eskiden ayrı ayrı, eşleşmemiş çıkardı)
def test_language_requirements_paired_with_level():
    jd = "Aranan Nitelikler: İngilizce (C1) ve Almanca (B2) gerekmektedir."
    parsed = parse_jd(jd)
    langs = parsed["identity"]["language_req"]
    assert any(x["language"] == "ingilizce" and x["level"] == "c1" for x in langs)
    assert any(x["language"] == "almanca" and x["level"] == "b2" for x in langs)
    # Türkçe büyük "İ" doğru küçültülmeli (P0-9: eski .lower() "i̇ngilizce" üretiyordu)
    assert all("̇" not in x["language"] for x in langs)


# P0-10 fix: "must" bölge başlığı yoksa gövdeden türetilen terimler artık 1.0 (zorunlu)
# değil, 0.6 (tercih bandı) — ve anlamsız kısaltmalar (MM gibi) filtrelenir.
def test_no_explicit_must_section_infers_lower_modality_and_filters_noise():
    jd_no_must_header = (
        "Şirketimiz İstanbul ofisinde çalışacak bir Lojistik Uzmanı arıyor. "
        "MM birimi cinsinden ölçüm yapılan sevkiyatlarda SAP ve Incoterms deneyimi önemlidir."
    )
    parsed = parse_jd(jd_no_must_header)
    assert parsed["must_have_source"] == "inferred_from_body"
    assert all(m["modality"] == 0.6 for m in parsed["must_have"])
    assert "MM" not in parsed["_must_terms"]


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
    # P0-1 fix: bu test eskiden "must_have boşsa Cov=1.0 (sahte tam-uyum)" davranışını
    # DOĞRU sanıp test ediyordu — bu davranışın ta kendisi P0 bug'dı (alakasız bir CV
    # bile yüksek skor alabiliyordu). Artık: skor çökmüyor (Lex/Sem'e dayanarak hâlâ
    # >0 üretebilir) AMA Cov "değerlendirilemedi" olarak işaretleniyor, sahte 1.0 DEĞİL,
    # ve motor açık bir uyarı üretiyor.
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, [], use_sbert=False)
    assert res["score_percent"] >= 0.0
    assert res["coverage_evaluable"] is False
    assert res["components"]["Cov"] == "değerlendirilemedi (must_have boş)"
    assert any("DEĞERLENDİRİLEMEDİ" in w for w in res["warnings"])
    assert "KISMİ DEĞERLENDİRME" in res["verdict"]


def test_nonempty_must_have_still_evaluable():
    # Kontrol testi: must_have DOLU olduğunda eski davranış (Cov sayısal, uyarı yok) korunur.
    res = ats_match_score(SAMPLE_JD, FRAMEWORK, ["python", "sql"], use_sbert=False)
    assert res["coverage_evaluable"] is True
    assert isinstance(res["components"]["Cov"], float)
    assert res["warnings"] == []


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
    from ats_engine.domain_packs import all_keywords, detect_domain, list_packs, load_pack
    packs = list_packs()
    assert "foreign-trade-logistics" in packs, "foreign-trade-logistics paketi olmalı"
    pack = load_pack("foreign-trade-logistics", lang="en")
    assert pack["domain"] == "Foreign Trade & Logistics"
    kw = all_keywords(pack)
    assert len(kw) > 10, "Pakette en az 10 anahtar kelime olmalı"
    # detect_domain test
    detected = detect_domain(SAMPLE_JD)
    # SAMPLE_JD foreign trade ile ilgili → detect edebilmeli
    # P0.2 fix: eski assertion (... or True) her zaman geçiyordu — ölü test.
    # detect_domain None veya str dönmeli, hata fırlatmamalı.
    assert detected is None or isinstance(detected, str), \
        f"detect_domain str veya None dönmeli, dönen: {type(detected)}"


# ATSE-8: enrich_must_terms çalışmalı
def test_domain_packs_enrich():
    from ats_engine.domain_packs import enrich_must_terms, load_pack
    pack = load_pack("foreign-trade-logistics", lang="en")
    must = ["customs clearance", "incoterms"]
    enriched = enrich_must_terms(must, pack, max_additions=3)
    assert len(enriched) >= len(must), "Zenginleştirilmiş liste en az orijinal kadar uzun olmalı"
    assert enriched[:2] == must, "Orijinal terimler korunmalı"


# ATSE-9: LangGate karışık dilde tetiklenmeli
def test_lang_gate_triggers_on_mixed():
    from ats_engine.multilevel import language_purity
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


# ─── Faz 0 Feature Tests ────────────────────────────────────────────────────

# Y36-9: Genişletilmiş özel karakter regex
def test_special_chars_extended():
    from ats_engine.cv_parser import _SPECIAL_CHARS
    # Eski regex yakalıyordu
    assert _SPECIAL_CHARS.search("★")
    assert _SPECIAL_CHARS.search("●")
    # Yeni eklenen karakterler
    assert _SPECIAL_CHARS.search("·"), "middle dot yakalanmalı"
    assert _SPECIAL_CHARS.search("—"), "em-dash yakalanmalı"
    assert _SPECIAL_CHARS.search("\u201c"), "smart quote yakalanmalı"
    assert _SPECIAL_CHARS.search("…"), "ellipsis yakalanmalı"
    # Normal karakterler yakalanmamalı
    assert not _SPECIAL_CHARS.search("abc 123")
    assert not _SPECIAL_CHARS.search("-")  # normal tire OK


# Y36-10: cliche_risk verbs tespiti
def test_cliche_verbs_detected():
    from ats_engine.lexicons import cliche_verbs
    cv = cliche_verbs()
    assert "spearheaded" in cv, "spearheaded cliche olmalı"
    assert "orchestrated" in cv, "orchestrated cliche olmalı"
    assert "pioneered" in cv, "pioneered cliche olmalı"
    # Normal fiiller cliche olmamalı
    assert "built" not in cv
    assert "managed" not in cv


# Y36-13: TR-aware casefold (P0.1 güncelleme: acronym-safe)
def test_tr_lower_casefold():
    from ats_engine.text import tr_lower
    assert tr_lower("İSTANBUL") == "istanbul", "İ → i dönüşümü"
    # P0.1: I→i (EN standart) — I→ı yerine. INCOTERMS doğruluğu > KISA doğruluğu
    assert tr_lower("KISA") == "kisa", "I → i (acronym-safe, EN standart)"
    assert tr_lower("GÜNEŞ") == "güneş", "diğer TR karakterler"
    assert tr_lower("HELLO") == "hello", "EN kelimeler"


# Y36-13: tokenize artık TR-aware
def test_tokenize_tr_aware():
    tokens = text.tokenize("İSTANBUL ve ANKARA", ngram_max=1)
    assert "istanbul" in tokens, "İSTANBUL → istanbul olmalı"
    assert "ankara" in tokens


# Y36-11: report.py skill count table
def test_report_has_skill_count_table():
    report = build_report(SAMPLE_JD, FRAMEWORK, FRAMEWORK, use_sbert=False)
    assert "skill_count_table" in report, "skill_count_table raporun parçası olmalı"
    table = report["skill_count_table"]
    assert len(table) > 0, "En az bir satır olmalı"
    # Her satırda gerekli alanlar
    for row in table:
        assert "skill" in row
        assert "jd_count" in row
        assert "resume_count" in row
        assert "status" in row


# Y36-12: skill_synonyms genişletilmiş
def test_skill_synonyms_expanded():
    from ats_engine.lexicons import normalize_skill
    # Yeni eklenen giriş: "multimodal transport" → "intermodal transport" eşleşmeli
    result = normalize_skill("intermodal transport")
    assert result == "multimodal transport", f"Beklenen: multimodal transport, Gelen: {result}"


# Y36-15: sample_cv temizliği (· ve — olmamalı)
def test_sample_cv_clean():
    import os
    sample_path = os.path.join(
        os.path.dirname(__file__), "..", "examples", "sample_cv.txt"
    )
    with open(sample_path, encoding="utf-8") as f:
        content = f.read()
    assert "·" not in content, "middle dot temizlenmeli"
    assert "—" not in content, "em-dash temizlenmeli"


# ─── Faz 1 Feature Tests ────────────────────────────────────────────────────

# Y36-16: completeness_guard
def test_evidence_recall():
    from ats_engine.completeness_guard import evidence_recall
    result = evidence_recall(FRAMEWORK, FRAMEWORK, threshold=0.3)
    assert "total_evidence" in result
    assert "recall_percent" in result
    assert "verdict" in result
    # Framework vs kendisi → recall yüksek olmalı
    assert result["recall_percent"] >= 50.0


# Y36-17: format_metadata_hygiene
def test_hygiene_check():
    from ats_engine.format_metadata_hygiene import full_hygiene_check
    result = full_hygiene_check(FRAMEWORK)
    assert "word_budget" in result
    assert "paragraph_length" in result
    assert "special_characters" in result
    assert "bullet_count" in result
    assert "word_count" in result["word_budget"]


# Y36-19: locale_consistency
def test_locale_detection():
    from ats_engine.locale_consistency import detect_locale, locale_mismatches
    assert detect_locale("We optimize and organize processes") == "AmE"
    assert detect_locale("We optimise and organise processes") == "BrE"
    assert detect_locale("Hello world") == "unknown"

    # Mismatch tespiti
    result = locale_mismatches(
        "We need someone who can optimize operations",
        "I optimise business processes daily"
    )
    assert len(result["mismatches"]) > 0, "AmE JD vs BrE CV → mismatch olmalı"


# Y36-20: quantification_score
def test_quantification_audit():
    from ats_engine.quantification_score import quantification_audit
    cv_with_numbers = (
        "- Revenue'yi %30 artırdım.\n"
        "- 50 kişilik ekibi yönettim.\n"
        "- Maliyeti $200K düşürdüm.\n"
        "- 3 yıllık deneyim.\n"
        "- Süreçleri optimize ettim.\n"
    )
    result = quantification_audit(cv_with_numbers, target_min=3)
    assert result["total_quantified"] >= 3
    assert result["score_percent"] >= 90.0


# Y36-21: cliche_tone
def test_cliche_detection():
    from ats_engine.cliche_tone import detect_cliches
    cv_with_cliches = "I spearheaded the transformation and orchestrated a paradigm shift"
    result = detect_cliches(cv_with_cliches)
    assert result["total_cliches"] > 0
    assert "❌" in result["tone_verdict"] or "⚠️" in result["tone_verdict"]

    # Temiz CV
    clean = "I managed the project and delivered results on time"
    result2 = detect_cliches(clean)
    assert result2["total_cliches"] == 0


# Y36-18: calibration
def test_calibration():
    from ats_engine.calibration import create_calibration, suggest_weight_adjustment
    jd_results = [
        ("Siegwerk", 86.7, 70.0),
        ("TestCo", 82.0, 78.0),
        ("AnotherJD", 90.5, 85.0),
    ]
    report = create_calibration(jd_results)
    assert len(report.entries) == 3
    assert report.mean_delta > 0  # engine inflated
    assert report.bias_direction == "engine_inflated"

    suggestions = suggest_weight_adjustment(report)
    assert len(suggestions["suggested_changes"]) > 0


# P0.1: tr_lower acronym-safe test
def test_tr_lower_acronym_safe():
    """P0.1 fix: INCOTERMS, ERP, SAP gibi EN acronymler bozulmamalı."""
    from ats_engine.text import tr_lower
    # EN acronymler doğru dönüşmeli
    assert tr_lower("INCOTERMS") == "incoterms", "INCOTERMS → incoterms olmalı"
    assert tr_lower("ERP") == "erp", "ERP → erp olmalı"
    assert tr_lower("SAP") == "sap", "SAP → sap olmalı"
    assert tr_lower("ISO") == "iso", "ISO → iso olmalı"
    # TR özel karakterler hala doğru dönüşmeli
    assert tr_lower("İSTANBUL") == "istanbul", "İSTANBUL → istanbul olmalı"
    assert tr_lower("GÜÇLÜ") == "güçlü", "GÜÇLÜ → güçlü olmalı"
    assert tr_lower("ÖĞRENCİ") == "öğrenci", "ÖĞRENCİ → öğrenci olmalı"
    assert tr_lower("ŞEKER") == "şeker", "ŞEKER → şeker olmalı"
    assert tr_lower("ÇELİK") == "çelik", "ÇELİK → çelik olmalı"
    # Karışık metin
    assert "ıncoterms" not in tr_lower("INCOTERMS 2020"), "ıncoterms olmamalı"


# P0.4: QA modülleri report'a bağlı mı testi
def test_report_has_qa_checks():
    """P0.4 fix: build_report() çıktısında qa_checks alanı olmalı."""
    from ats_engine.report import build_report
    result = build_report(SAMPLE_JD, FRAMEWORK, use_sbert=False)
    assert "qa_checks" in result, "build_report çıktısında qa_checks olmalı"
    qa = result["qa_checks"]
    # En az birkaç QA kontrol sonucu olmalı
    expected_checks = ["completeness", "hygiene", "quantification", "cliches"]
    for check in expected_checks:
        assert check in qa, f"qa_checks içinde '{check}' olmalı"


# P0-4 fix: calibration_hint artık motorun kendi skorunu kendisiyle karşılaştırmıyor
def test_calibration_hint_not_self_referential():
    from ats_engine.report import build_report
    result = build_report(SAMPLE_JD, FRAMEWORK, use_sbert=False)
    ch = result["qa_checks"]["calibration_hint"]
    assert ch["adjustment"] == "not_available"
    assert "dış referans" in ch["note"]


# P0-6 fix: Markdown raporu artık calibration_hint'i de göstermeli (JSON/MD tutarlılığı)
def test_markdown_includes_calibration_line():
    from ats_engine.report import build_report, to_markdown
    result = build_report(SAMPLE_JD, FRAMEWORK, use_sbert=False)
    md = to_markdown(result)
    assert "Calibration" in md
