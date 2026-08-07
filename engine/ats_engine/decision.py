"""Evidence-first G0-G4 decision orchestration.

Lexical/semantic scores remain diagnostics. They are never universal hiring or
commercial-ATS pass/fail gates. Human approval is always explicit.
"""

from __future__ import annotations

from uuid import uuid4

from .configuration import DEFAULT_GATE_POLICY, GatePolicy
from .contracts import (
    DecisionReport,
    DiagnosticResult,
    EvaluationStatus,
    GateResult,
    ProcessStatus,
)
from .errors import ErrorCode
from .locale_consistency import detect_language_mismatch


def _overall(gates: list[GateResult]) -> ProcessStatus:
    states = {gate.status for gate in gates}
    if ProcessStatus.ERROR in states:
        return ProcessStatus.ERROR
    if ProcessStatus.FAIL in states:
        return ProcessStatus.FAIL
    if ProcessStatus.REVIEW in states or ProcessStatus.NOT_RUN in states:
        return ProcessStatus.REVIEW
    if ProcessStatus.WARN in states:
        return ProcessStatus.WARN
    return ProcessStatus.PASS


def build_decision_report(
    report: dict,
    *,
    human_approved: bool = False,
    gate_policy: GatePolicy = DEFAULT_GATE_POLICY,
    jd_text: str = "",
    cv_text: str = "",
) -> DecisionReport:
    """Build a typed decision from a legacy report payload without inventing facts."""
    match = report.get("match_score", {})
    components = match.get("components", {})
    qa = report.get("qa_checks", {})
    analysis = report.get("analysis", {})

    parse_gate = components.get("Parse_gate")
    if isinstance(parse_gate, (int, float)) and parse_gate >= gate_policy.parse_pass_min:
        g0 = GateResult(
            "G0",
            ProcessStatus.PASS,
            f"Girdi metni ve parse sinyali kullanılabilir (policy={gate_policy.id}@{gate_policy.version}).",
        )
    elif isinstance(parse_gate, (int, float)):
        g0 = GateResult(
            "G0",
            ProcessStatus.FAIL,
            f"Parse sinyali {gate_policy.parse_pass_min:.2f} altında.",
            "Belge yapısını düzeltin veya ingestion sonucunu inceleyin.",
        )
    else:
        g0 = GateResult("G0", ProcessStatus.ERROR, "Parse sinyali üretilemedi.")

    knockouts = analysis.get("knockouts", [])
    if knockouts:
        g1 = GateResult(
            "G1",
            ProcessStatus.REVIEW,
            "Knockout gereksinimleri insan doğrulaması bekliyor.",
            diagnostics=list(knockouts),
        )
    else:
        g1 = GateResult("G1", ProcessStatus.NOT_RUN, "Aday uygunluk verisi toplanmadı; otomatik PASS verilemez.")

    completeness = qa.get("completeness", {})
    if completeness.get("error"):
        g2 = GateResult("G2", ProcessStatus.ERROR, "Kanıt kapsamı kontrolü başarısız.")
    elif completeness.get("total_evidence", 0) == 0:
        g2 = GateResult(
            "G2",
            ProcessStatus.REVIEW,
            "Yapılandırılmış evidence ID bulunmadı.",
            "Kanıt bankasını etiketli girdilerle doldurun.",
        )
    else:
        g2 = GateResult(
            "G2",
            ProcessStatus.REVIEW,
            "Sözcüksel kanıt desteği bulundu; olgusal doğrulama ve kaynak incelemesi gerekiyor.",
        )

    locale = qa.get("locale", {})
    locale_mismatches = locale.get("mismatches", []) if isinstance(locale, dict) else []

    # G3: check both AmE/BrE mismatches AND JD/CV language mismatch
    lang_mismatch_info = detect_language_mismatch(jd_text, cv_text) if (jd_text or cv_text) else None

    g3_diagnostics = [str(item) for item in locale_mismatches]
    if locale_mismatches:
        g3_status = ProcessStatus.WARN
        g3_reason = "Dil/locale tanısı tamamlandı."
    elif lang_mismatch_info and (lang_mismatch_info["mismatch"] or lang_mismatch_info["review_required"]):
        g3_status = ProcessStatus.REVIEW
        g3_reason = lang_mismatch_info["verdict"]
        g3_diagnostics.append(lang_mismatch_info["verdict"])
    else:
        g3_status = ProcessStatus.PASS
        g3_reason = "Dil/locale tanısı tamamlandı."

    g3 = GateResult("G3", g3_status, g3_reason, diagnostics=g3_diagnostics)

    g4 = GateResult(
        "G4",
        ProcessStatus.PASS if human_approved else ProcessStatus.REVIEW,
        "İnsan onayı kaydedildi." if human_approved else "İnsan onayı bekleniyor.",
        "Karar raporunu inceleyip açıkça onaylayın." if not human_approved else "",
    )

    gates = [g0, g1, g2, g3, g4]
    errors = [
        {
            "code": ErrorCode.QA_ERROR.value,
            "message": f"{name}: {value.get('error_detail') or value.get('error')}",
        }
        for name, value in qa.items()
        if isinstance(value, dict) and value.get("process_status") == ProcessStatus.ERROR.value
    ]
    diagnostics = [
        DiagnosticResult(
            "LEXICAL_ALIGNMENT",
            ProcessStatus.NOT_RUN if match.get("score_percent") is None else ProcessStatus.PASS,
            "Araştırma amaçlı hizalanma tanısı; işe alım veya ticari ATS geçiş olasılığı değildir.",
            value=match.get("score_percent"),
            unit="percent",
        )
    ]
    evaluation = (
        EvaluationStatus.NOT_EVALUATED
        if match.get("evaluation_status") == EvaluationStatus.NOT_EVALUATED.value
        else EvaluationStatus.EVALUATED
    )
    return DecisionReport(
        id=f"decision-{uuid4()}",
        overall_status=ProcessStatus.ERROR if errors else _overall(gates),
        evaluation_status=evaluation,
        gates=gates,
        diagnostics=diagnostics,
        errors=errors,
        human_approved=human_approved,
    )
