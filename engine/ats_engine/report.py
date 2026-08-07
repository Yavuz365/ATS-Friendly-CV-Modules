"""
ats_engine.report — 6 Alanlık Çıktı Birleştiricisi.

ats-cv-architect'in sözleşmesi: her ilandan TAM OLARAK şu 6 alan üretilir —
  1) keywords  2) analysis  3) summary  4) synthesis  5) match_score  6) gap_analysis
Bu modül jd_parser + scoring + synthesis + evidence_bank katmanlarını tek bir
deterministik rapora bağlar (output-fields-template.md ile uyumlu) ve hem JSON hem
insan-okur Markdown üretir.

Mod:
  - cv_text verilirse → TEŞHİS modu (mevcut CV skorlanır).
  - verilmezse        → Framework CV taban alınır (sentez öncesi başlangıç skoru).

Bağımlılık: yalnızca standart kütüphane (+ ats_engine alt modülleri).
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable

# P0.4 fix: 6 QA modülünü rapora bağla (v1.4'te export edilmiş ama wired değildi)
from . import cv_parser, evidence_bank, jd_parser, multilevel, synthesis
from .cliche_tone import detect_cliches
from .completeness_guard import evidence_recall
from .configuration import EvaluationProfile
from .contracts import ProcessStatus, QAResult, QASeverity, to_primitive
from .decision import build_decision_report
from .format_metadata_hygiene import full_hygiene_check
from .legacy_adapter import legacy_diagnostic
from .locale_consistency import locale_mismatches
from .matching import count_boundary_occurrences, match_term
from .quantification_score import quantification_audit

# A9 fix (hardening): QA alt modüllerinden gelen beklenmedik hatalar artık
# sessizce yutulmuyor — logger'a (traceback dahil) yazılıyor ve gerçek hata
# mesajı (yalnızca sabit "hesaplanamadı" değil) rapora da ekleniyor. Rapor
# yine de üretilmeye devam eder (bir QA alt-modülünün çökmesi tüm raporu
# düşürmemeli) ama artık arıza *görünür* — CI/log izleme bunu yakalayabilir.
logger = logging.getLogger(__name__)

# P0-4 fix: create_calibration/suggest_weight_adjustment artık build_report()
# içinde çağrılmıyor (bkz. qa_checks["calibration_hint"] altındaki not) — gerçek
# dış referans skoru olan ayrı bir kalibrasyon akışı için calibration.py'de dursunlar.


# QA-001: static, per-check remediation guidance. Kept generic and check-scoped
# (not fabricated per document) so QAResult.remediation is always a truthful,
# actionable next step rather than an invented specific claim about this run.
_QA_REMEDIATION: dict[str, str] = {
    "completeness": (
        "Add or rephrase framework CV evidence bullets so more claims lexically overlap the "
        "CV; verify manually — lexical overlap is a support signal, not factual verification."
    ),
    "hygiene": "Address the flagged formatting/length/metadata issues listed in evidence/details.",
    "locale": "Resolve the JD/CV language or spelling-variant mismatches listed in evidence.",
    "quantification": "Add concrete, verifiable metrics to the bullets listed as non-quantified in evidence.",
    "cliches": "Rewrite the flagged clichéd verbs/buzzwords in evidence with specific, evidence-backed language.",
    "calibration_hint": "No action needed: this field only becomes meaningful when a real external comparator score is supplied.",
}


def _qa_evidence(name: str, value: dict) -> list[str]:
    """Pull a short, concrete evidence list out of a QA sub-module's raw payload.

    QA-001: ``details`` alone forces every caller to know each sub-module's
    private shape to find *what* triggered the status. This surfaces the
    handful of items that actually explain the verdict as plain strings.
    """
    if name == "hygiene":
        out: list[str] = []
        for sub in value.values():
            if isinstance(sub, dict) and sub.get("details"):
                out.extend(str(item) for item in sub["details"][:3])
        return out[:5]
    key_candidates = {
        "completeness": ("missed",),
        "locale": ("mismatches",),
        "quantification": ("non_quantified_lines",),
        "cliches": ("cliche_verb_hits", "buzzword_hits"),
    }.get(name, ())
    out = []
    for key in key_candidates:
        items = value.get(key) or []
        out.extend(str(item) for item in items[:5])
    return out[:5]


def _run_qa_check(name: str, fn: Callable[..., dict], *args) -> dict:
    """A9 fix: 6 QA alt-modülü çağrısı için ortak hata sözleşmesi.

    Eskiden her çağrı kendi `except Exception: {"error": "<sabit metin>"}` bloğuna
    sahipti — hangi hata tipi/mesajının oluştuğu tamamen kayboluyordu (sessiz yutma).
    Artık: (1) beklenmedik hata `logger.warning` ile traceback dahil loglanır,
    (2) rapora yalnızca "hesaplanamadı" değil gerçek exception tipi+mesajı da yazılır,
    (3) tek bir QA alt-modülünün çökmesi tüm raporu düşürmez (kasıtlı fail-soft —
    QA alanları rapora ek bilgi katar, ana skor/karar zincirinin parçası değildir).
    """
    try:
        result = fn(*args)
        return {**result, "process_status": ProcessStatus.PASS.value}
    except Exception as exc:  # kasıtlı geniş yakalama, bkz. docstring
        logger.warning("QA check '%s' failed: %s: %s", name, type(exc).__name__, exc, exc_info=True)
        return {
            "error": f"{name} hesaplanamadı",
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "process_status": ProcessStatus.ERROR.value,
        }


def build_report(
    jd_text: str,
    framework_cv_text: str,
    cv_text: str | None = None,
    parse_gate: float | None = None,
    corpus_texts: list[str] | None = None,
    use_sbert: bool = True,
    evaluation_profile: EvaluationProfile | None = None,
    target_low: float | None = None,
    human_approved: bool = False,
) -> dict:
    """JD + Framework CV (+ opsiyonel mevcut CV) → 6 alanlık yapılandırılmış rapor.

    P0.3 fix: parse_gate=None → cv_parser.parse_safety_score() otomatik hesaplar.
    P0.4 fix: 6 QA modülü rapora bağlandı (completeness, hygiene, locale, quant, cliché, calibration).
    """
    if evaluation_profile is not None and target_low is not None:
        raise ValueError("evaluation_profile ve target_low birlikte verilemez.")
    if target_low is not None:
        evaluation_profile = EvaluationProfile(
            id="legacy-explicit-target",
            version="1.0.0",
            source="Explicit caller-provided diagnostic stop target",
            effective_date="2026-08-05",
            locale="unspecified",
            domain="unspecified",
            comparator_version="caller-defined",
            owner="caller",
            rationale=(
                "Caller passed target_low directly via the legacy --target CLI/API "
                "parameter instead of a named EvaluationProfile; ownership and "
                "justification for this number are the caller's, not the engine's."
            ),
            review_date="unspecified",
            diagnostic_stop_min=target_low,
        )

    analysis = jd_parser.parse_jd(jd_text)
    bank = evidence_bank.parse_bank(framework_cv_text)

    must_terms = analysis["_must_terms"]
    weights = analysis["_scoring_weights"]
    scored_text = cv_text if cv_text is not None else framework_cv_text

    # P0.3 fix: parse_gate=None → otomatik ParseGate hesaplama
    if parse_gate is None:
        _pg_result = cv_parser.parse_safety_score(scored_text)
        parse_gate = _pg_result["score"]

    score = legacy_diagnostic(
        jd_text,
        scored_text,
        must_terms,
        corpus_texts=corpus_texts,
        weights=weights,
        parse_gate=parse_gate,
        lang_gate=multilevel.lang_gate(scored_text, jd_text),
        use_sbert=use_sbert,
    )

    gaps = synthesis.classify_gaps(score["gap"], bank)
    stop = synthesis.stopping_condition(score["score_percent"], gaps["closable"], evaluation_profile)
    stuffing = synthesis.anti_stuffing_report(scored_text, must_terms)

    # 1) keywords (ağırlıklı liste)
    keywords = [
        {
            "term": m["term"],
            "modality": ("zorunlu" if m["modality"] >= 1.0 else "güçlü-ima" if m["modality"] >= 0.7 else "tercih"),
            "positional_weight": m["positional_weight"],
            "freq": m["freq"],
        }
        for m in (analysis["must_have"] + analysis["nice_to_have"])
    ]

    # 3) summary
    summary = {
        "role_essence": analysis["intent"],
        "cv_top_summary_hint": (
            "İlk 100–150 kelimede yalnız kanıtla desteklenen açık zorunlu terimleri konumlandır: "
            + ", ".join(must_terms[:6])
            + "."
            if must_terms
            else "Açık zorunlu terim çıkarılamadı; ilanı insan incelemesine gönder ve gövde terimlerini must sayma."
        ),
    }

    # 4) synthesis
    synth = {
        "semantic_clusters": synthesis.cluster_skills(must_terms),
        "lsi_expansions": analysis["lsi"],
        "xyz_template": "[Z yöntemiyle] (aktif fiil), [Y ölçüsüyle] [X sonucunu] elde ettim.",
        "anti_stuffing": stuffing,
        "section_map": ["Özet", "Deneyim", "Beceriler", "Eğitim", "Sertifikalar"],
        "evidence_bank_size": len(bank),
    }

    # 5) match_score (zaten dict)
    match_score = score

    # 6) gap_analysis
    gap_analysis = {
        "closable_gaps": gaps["closable"],
        "uncloseable_gaps": gaps["uncloseable"],
        "precision": score["precision"],
        "recall": score["recall"],
        "f1": score["f1"],
        "revision_loop": stop,
        "recommendations": (
            [g["action"] for g in gaps["closable"]]
            + ([f["note"] for f in stuffing["flagged"]] if stuffing["flagged"] else [])
        )
        or ["Kapatılabilir gap yok; skor hedefteyse teslim et."],
    }

    # ── Y36-11: Jobscan-style Skill/JD/Resume sayım tablosu ──────────────
    # B1/STAB-015 (kalan parça, 2026-08-03): bu tablo A1'in düzelttiği
    # matches_semantically() yolunu KULLANMIYORDU -- ayrı, hala bozuk bir
    # `t_low in tok` alt-string kontrolüyle sayıyordu. text.tokenize()
    # 1..3-gram'lık HER PENCEREYİ tek tek üretir (üst üste biner); bir terim
    # bu pencerelerin çoğunun içinde alt-string olarak da geçtiği için tek
    # bir gerçek geçiş 3-6 kata kadar şişiyordu (canlı kanıt: JD'de 2 kez
    # geçen "incoterms" bu yolla 12 olarak sayılıyordu). jd_parser.py'nin
    # kendi freq hesaplaması (satır ~215) zaten doğru deseni kullanıyor --
    # Counter üzerinden TAM eşleşme arama, alt-string değil. Aynı desen
    # burada da uygulandı.
    # STAB-016 fix: use match_term (canonical matcher) for status/stage; keep
    # count_boundary_occurrences for exact occurrence counts only.
    # Synonym/ontology/semantic matches expose their stage — no substring inflation.
    skill_count_table = []
    all_terms = [m["term"] for m in (analysis["must_have"] + analysis["nice_to_have"])]
    for term in all_terms:
        jd_count = count_boundary_occurrences(term, jd_text)
        tm = match_term(term, scored_text)
        if not tm.matched:
            resume_count = 0
            status = "❌ Missing"
            match_stage = tm.stage.value
        elif tm.stage.value == "EXACT":
            resume_count = tm.count
            status = "✅ Match"
            match_stage = tm.stage.value
        else:
            # Non-exact match: use tm.count (the matched variant's occurrences) so
            # resume_count stays consistent with the matcher result and is never 0
            # while status shows a match. Never re-count the original unmatched term.
            resume_count = tm.count
            status = f"⚠️ Match ({tm.stage.value})"
            match_stage = tm.stage.value
        skill_count_table.append(
            {
                "skill": term,
                "jd_count": jd_count,
                "resume_count": resume_count,
                "status": status,
                "match_stage": match_stage,
            }
        )

    # ── P0.4: 6 QA modülü sonuçları ─────────────────────────────────────────
    # A9 fix: her alt-modül çağrısı artık ortak bir sarmalayıcıdan geçiyor —
    # beklenmedik hata sessizce yutulmuyor; logger'a yazılıyor ve gerçek
    # exception tipi+mesajı (yalnızca sabit metin değil) rapora ekleniyor.
    qa_checks: dict = {}
    qa_checks["completeness"] = _run_qa_check("completeness", evidence_recall, framework_cv_text, scored_text)
    qa_checks["hygiene"] = _run_qa_check("hygiene", full_hygiene_check, scored_text)
    qa_checks["locale"] = _run_qa_check("locale", locale_mismatches, jd_text, scored_text)
    qa_checks["quantification"] = _run_qa_check("quantification", quantification_audit, scored_text)
    qa_checks["cliches"] = _run_qa_check("cliches", detect_cliches, scored_text)

    # P0-4 fix: eskiden burada motorun KENDİ skoru hem "engine_score" hem
    # "jobscan_score" olarak calibration'a veriliyordu → delta her zaman 0,
    # sonuç her zaman "✅ mükemmel korelasyon" (sahte kalibrasyon — motor kendi
    # kendisiyle karşılaştırılıyordu, dış bir referans yoktu). create_calibration()/
    # suggest_weight_adjustment() GERÇEK bir dış (ör. Jobscan) skoru verildiğinde
    # anlamlıdır (bkz. calibration.py — ayrı bir kalibrasyon script'inde kullanılabilir);
    # build_report() burada dış referans ALMADIĞI için sahte veri üretmek yerine
    # dürüstçe "N/A" işaretliyoruz.
    qa_checks["calibration_hint"] = {
        "adjustment": "not_available",
        "process_status": ProcessStatus.NOT_RUN.value,
        "note": (
            "Bu alan yalnızca GERÇEK bir dış referans skoru (ör. Jobscan) verildiğinde "
            "anlamlıdır. build_report() dış referans almıyor; motorun kendi skorunu "
            "kendisiyle karşılaştırıp sahte '✅ mükemmel korelasyon' üretmek yerine bu "
            "alan boş bırakıldı (P0-4 fix)."
        ),
    }

    qa_results = []
    for name, value in qa_checks.items():
        status = ProcessStatus(value.get("process_status", ProcessStatus.PASS.value))
        severity = QASeverity.REVIEW if status is ProcessStatus.ERROR else QASeverity.ADVISORY
        qa_results.append(
            QAResult(
                check_id=f"QA_{name.upper()}",
                status=status,
                severity=severity,
                message=value.get("error") or value.get("verdict") or f"{name} tamamlandı",
                blocking=status is ProcessStatus.ERROR,
                details=value,
                evidence=_qa_evidence(name, value),
                remediation=_QA_REMEDIATION.get(name, ""),
            )
        )

    payload = {
        "mode": "diagnostic" if cv_text is not None else "framework-baseline",
        "keywords": keywords,
        "analysis": {
            "identity": analysis["identity"],
            "must_have": analysis["must_have"],
            "nice_to_have": analysis["nice_to_have"],
            "responsibilities": analysis["responsibilities"],
            "knockouts": analysis["knockouts"],
            "intent": analysis["intent"],
            "must_have_source": analysis["must_have_source"],
            "review_required": analysis["review_required"],
            "review_reason": analysis["review_reason"],
        },
        "summary": summary,
        "synthesis": synth,
        "match_score": match_score,
        "gap_analysis": gap_analysis,
        "skill_count_table": skill_count_table,
        "qa_checks": qa_checks,
        "qa_results": to_primitive(qa_results),
    }
    payload["decision_report"] = build_decision_report(
        payload,
        human_approved=human_approved,
        jd_text=jd_text,
        cv_text=cv_text or "",
    ).to_dict()
    return payload


def to_json(report: dict, indent: int = 2) -> str:
    return json.dumps(report, ensure_ascii=False, indent=indent)


def to_markdown(report: dict) -> str:
    a = report["analysis"]
    ms = report["match_score"]
    ga = report["gap_analysis"]
    lines = []
    lines.append(f"# ATS Match Raporu — mod: {report['mode']}\n")

    lines.append("## 1. keywords (ağırlıklı liste)")
    for k in report["keywords"]:
        lines.append(f"- **{k['term']}** — {k['modality']} · konum×{k['positional_weight']} · freq {k['freq']}")
    lines.append("")

    lines.append("## 2. analysis (7 katman özeti)")
    idn = a["identity"]
    # P0-8 fix: language_req artık [{"language":..,"level":..}, ...] (dil+seviye
    # eşleşmiş) — eskiden düz bir string listesiydi ve dil/seviye hiç eşleşmiyordu.
    lang_str = (
        ", ".join(
            f"{lr['language']} ({lr['level']})" if lr.get("level") else lr["language"] for lr in idn["language_req"]
        )
        or "—"
    )
    lines.append(
        f"- **Kimlik:** {idn['title_guess']} · kıdem: {idn['seniority']} · çalışma: {idn['work_mode']} · dil: {lang_str} · deneyim: {idn['experience_years'] or '—'}"
    )
    lines.append(f"- **Zorunlu:** {', '.join(m['term'] for m in a['must_have']) or '—'}")
    lines.append(f"- **Tercih:** {', '.join(m['term'] for m in a['nice_to_have']) or '—'}")
    lines.append(f"- **Sorumluluk fiilleri:** {', '.join(a['responsibilities'][:12]) or '—'}")
    lines.append(f"- **Knockouts:** {', '.join(a['knockouts']) or '—'}")
    lines.append(f"- **Niyet:** {a['intent']}")
    lines.append("")

    lines.append("## 3. summary")
    lines.append(f"- **Rolün özü:** {report['summary']['role_essence']}")
    lines.append(f"- **Üst-özet ipucu:** {report['summary']['cv_top_summary_hint']}")
    lines.append("")

    lines.append("## 4. synthesis")
    for c in report["synthesis"]["semantic_clusters"]:
        lines.append(f"- **{c['cluster_label']}:** {', '.join(c['member_skills'])}")
    lines.append(f"- **Bölüm haritası:** {', '.join(report['synthesis']['section_map'])}")
    lines.append(f"- **Kanıt bankası girdi sayısı:** {report['synthesis']['evidence_bank_size']}")
    if report["synthesis"]["anti_stuffing"]["flagged"]:
        lines.append(f"- **Şişirme uyarısı:** {report['synthesis']['anti_stuffing']['flagged']}")
    lines.append("")

    lines.append("## 5. match_score")
    score_text = f"%{ms['score_percent']}" if ms["score_percent"] is not None else "NOT_EVALUATED"
    lines.append(f"- **Hizalanma tanısı:** {score_text} — {ms['verdict']}")
    lines.append(
        f"- **Bileşenler:** Lex={ms['components']['Lex']} · Sem={ms['components']['Sem']} · "
        f"Cov={ms['components']['Cov']} · Parse_gate={ms['components']['Parse_gate']} · "
        f"Stuffing={ms['components']['Stuffing']}"
    )
    lines.append(f"- **Ağırlıklar:** {ms['weights_used']}")
    lines.append(f"- **P/R/F1:** {ms['precision']} / {ms['recall']} / {ms['f1']}")
    if ms.get("warnings"):
        lines.append("- **⚠️ Uyarılar:**")
        for w in ms["warnings"]:
            lines.append(f"  - {w}")
    lines.append("")

    decision = report.get("decision_report", {})
    if decision:
        lines.append("## Decision Report")
        lines.append(f"- **Genel durum:** {decision.get('overall_status', '?')}")
        lines.append(f"- **Değerlendirme:** {decision.get('evaluation_status', '?')}")
        for gate in decision.get("gates", []):
            lines.append(f"- **{gate['gate_id']}:** {gate['status']} — {gate['reason']}")
        lines.append("")

    # Y36-11: Jobscan-style sayım tablosu
    lines.append("## Skill Count Table (Jobscan-style)")
    lines.append("| Skill | JD Count | Resume Count | Status | Match Stage |")
    lines.append("|-------|----------|--------------|--------|-------------|")
    for row in report.get("skill_count_table", []):
        stage = row.get("match_stage", "")
        lines.append(f"| {row['skill']} | {row['jd_count']} | {row['resume_count']} | {row['status']} | {stage} |")
    lines.append("")

    # P0.4: QA Checks bölümü
    # STAB-013 fix: status/severity comes from typed qa_results; qa_checks used for
    # informational detail only — no second independent PASS/WARN/REVIEW derivation.
    qa = report.get("qa_checks", {})
    qa_results_list = report.get("qa_results", [])
    # Build a status lookup from typed qa_results (canonical source of truth)
    qa_status_map = {qr["check_id"]: qr["status"] for qr in qa_results_list if isinstance(qr, dict)}
    if qa:
        lines.append("## QA Checks (v1.5 — 6 modül)")
        if "completeness" in qa and "error" not in qa["completeness"]:
            cr = qa["completeness"]
            status_str = qa_status_map.get("QA_COMPLETENESS", "")
            lines.append(
                f"- **Completeness (Evidence Recall):** %{cr.get('recall_percent', '?')}"
                + (f" [{status_str}]" if status_str else "")
            )
        if "hygiene" in qa and "error" not in qa["hygiene"]:
            hy = qa["hygiene"]
            status_str = qa_status_map.get("QA_HYGIENE", "")
            lines.append(
                f"- **Format Hygiene:** word_count={hy.get('word_budget', {}).get('word_count', '?')}, "
                f"special_chars={hy.get('special_characters', {}).get('total_special', 0)}"
                + (f" [{status_str}]" if status_str else "")
            )
        if "locale" in qa and "error" not in qa["locale"]:
            lo = qa["locale"]
            status_str = qa_status_map.get("QA_LOCALE", "")
            lines.append(
                f"- **Locale:** JD={lo.get('jd_locale', '?')}, CV={lo.get('cv_locale', '?')}, "
                f"mismatches={len(lo.get('mismatches', []))}" + (f" [{status_str}]" if status_str else "")
            )
        if "quantification" in qa and "error" not in qa["quantification"]:
            qu = qa["quantification"]
            status_str = qa_status_map.get("QA_QUANTIFICATION", "")
            lines.append(
                f"- **Quantification:** found={qu.get('total_quantified', '?')}, "
                f"target={qu.get('target', 5)}, verdict={qu.get('verdict', '?')}"
                + (f" [{status_str}]" if status_str else "")
            )
        if "cliches" in qa and "error" not in qa["cliches"]:
            cl = qa["cliches"]
            status_str = qa_status_map.get("QA_CLICHES", "")
            lines.append(
                f"- **Clichés:** count={cl.get('total_cliches', 0)}, durum={cl.get('tone_verdict', 'none')}"
                + (f" [{status_str}]" if status_str else "")
            )
        # P0-6 fix: calibration_hint JSON'da vardı ama Markdown raporunda hiç
        # görünmüyordu (rapor formatları birbirini tutmuyordu) — artık burada da basılıyor.
        if "calibration_hint" in qa and "error" not in qa["calibration_hint"]:
            ch = qa["calibration_hint"]
            status_str = qa_status_map.get("QA_CALIBRATION_HINT", "")
            lines.append(
                f"- **Calibration:** {ch.get('adjustment', '?')} — {ch.get('note', '')}"
                + (f" [{status_str}]" if status_str else "")
            )
        lines.append("")

    lines.append("## 6. gap_analysis")
    lines.append(f"- **Kapatılabilir gap:** {[g['term'] for g in ga['closable_gaps']] or '—'}")
    lines.append(f"- **Kapatılamaz gap:** {[g['term'] for g in ga['uncloseable_gaps']] or '—'}")
    lines.append(f"- **Revizyon döngüsü:** {ga['revision_loop']['reason']}")
    lines.append("- **Öneriler:**")
    for r in ga["recommendations"]:
        lines.append(f"  - {r}")
    lines.append("")
    return "\n".join(lines)
