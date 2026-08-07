"""G3 language mismatch + locale consistency regression tests.

Covers:
- TR JD + EN CV  → G3 WARN/REVIEW, not PASS
- EN JD + EN CV  → no false mismatch
- AmE vs BrE existing behaviour preserved
- detect_language basic cases
- detect_language_mismatch contract
"""

from __future__ import annotations

from ats_engine.contracts import ProcessStatus
from ats_engine.locale_consistency import (
    detect_language,
    detect_language_mismatch,
    locale_mismatches,
)

TR_JD = (
    "Dış Ticaret Uzmanı arıyoruz. Adayın en az 3 yıl deneyim sahibi olması ve "
    "ihracat operasyonlarını bağımsız yürütebilmesi gerekmektedir. "
    "SAP ve incoterms konusunda bilgi sahibi olması tercih edilir."
)
EN_CV = (
    "I have 4 years of experience in export operations and customs clearance. "
    "I am proficient with SAP and Incoterms procedures."
)
EN_JD = (
    "We are looking for a Foreign Trade Specialist with at least 3 years of experience. "
    "The candidate will manage export operations and customs clearance."
)
EN_CV2 = (
    "Foreign trade professional with 5 years of experience in export operations. "
    "Skills: SAP, Incoterms, customs clearance."
)


# ── detect_language ───────────────────────────────────────────────────────────


def test_detect_language_turkish():
    lang = detect_language(TR_JD)
    assert lang == "TR"


def test_detect_language_english():
    lang = detect_language(EN_JD)
    assert lang == "EN"


def test_detect_language_empty_returns_unknown():
    assert detect_language("") == "UNKNOWN"
    assert detect_language("   ") == "UNKNOWN"


# ── detect_language_mismatch ─────────────────────────────────────────────────


def test_tr_jd_en_cv_is_mismatch():
    result = detect_language_mismatch(TR_JD, EN_CV)
    # Must not produce PASS — either mismatch=True or review_required=True
    assert result["mismatch"] is True or result["review_required"] is True


def test_en_jd_en_cv_no_mismatch():
    result = detect_language_mismatch(EN_JD, EN_CV2)
    assert result["mismatch"] is False
    assert result["review_required"] is False


def test_unknown_evidence_does_not_produce_mismatch_false_with_review_false():
    """Insufficient evidence must expose review_required, never silent PASS."""
    result = detect_language_mismatch("ok", "ok")
    # With very short text, either review_required=True or mismatch can be True
    # The one forbidden outcome is mismatch=False AND review_required=False when
    # one side is UNKNOWN
    jd_lang = result["jd_language"]
    cv_lang = result["cv_language"]
    if jd_lang == "UNKNOWN" or cv_lang == "UNKNOWN":
        assert result["review_required"] is True, "UNKNOWN language evidence must not silently PASS"


# ── G3 gate via decision.build_decision_report ───────────────────────────────


def test_g3_not_pass_for_tr_jd_en_cv():
    """G3 must be WARN or REVIEW when JD/CV language mismatch is detected."""
    from ats_engine.decision import build_decision_report

    report = {"match_score": {}, "qa_checks": {}, "analysis": {"knockouts": []}}
    dr = build_decision_report(report, jd_text=TR_JD, cv_text=EN_CV)
    g3 = next(g for g in dr.gates if g.gate_id == "G3")
    assert g3.status in (ProcessStatus.WARN, ProcessStatus.REVIEW), (
        f"G3 must not PASS for TR JD + EN CV; got {g3.status}"
    )


def test_g3_pass_for_en_jd_en_cv():
    """G3 should PASS when JD and CV are both English with no locale mismatches."""
    from ats_engine.decision import build_decision_report

    report = {"match_score": {}, "qa_checks": {}, "analysis": {"knockouts": []}}
    dr = build_decision_report(report, jd_text=EN_JD, cv_text=EN_CV2)
    g3 = next(g for g in dr.gates if g.gate_id == "G3")
    assert g3.status is ProcessStatus.PASS


# ── AmE/BrE detection preserved ──────────────────────────────────────────────


def test_ame_bre_mismatch_still_works():
    jd_ame = "We need someone to optimize and standardize our processes."
    cv_bre = "I have optimised and standardised many processes in my career."
    result = locale_mismatches(jd_ame, cv_bre)
    assert len(result["mismatches"]) >= 1
    assert "optimize" in result["verdict"] or "⚠️" in result["verdict"]


def test_same_locale_no_mismatch():
    jd = "We need someone to optimize and customize our systems."
    cv = "I have optimized and customized several enterprise systems."
    result = locale_mismatches(jd, cv)
    assert result["mismatches"] == []
    assert "✅" in result["verdict"]
