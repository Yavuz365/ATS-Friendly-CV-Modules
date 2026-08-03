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

# P0.4 fix: 6 QA modülünü rapora bağla (v1.4'te export edilmiş ama wired değildi)
from . import cv_parser, evidence_bank, jd_parser, scoring, synthesis, text
from .cliche_tone import detect_cliches
from .completeness_guard import evidence_recall
from .format_metadata_hygiene import full_hygiene_check
from .locale_consistency import locale_mismatches
from .quantification_score import quantification_audit

# P0-4 fix: create_calibration/suggest_weight_adjustment artık build_report()
# içinde çağrılmıyor (bkz. qa_checks["calibration_hint"] altındaki not) — gerçek
# dış referans skoru olan ayrı bir kalibrasyon akışı için calibration.py'de dursunlar.


def build_report(jd_text: str, framework_cv_text: str, cv_text: str | None = None,
                 parse_gate: float | None = None, corpus_texts: list[str] | None = None,
                 use_sbert: bool = True, target_low: float = 75.0) -> dict:
    """JD + Framework CV (+ opsiyonel mevcut CV) → 6 alanlık yapılandırılmış rapor.

    P0.3 fix: parse_gate=None → cv_parser.parse_safety_score() otomatik hesaplar.
    P0.4 fix: 6 QA modülü rapora bağlandı (completeness, hygiene, locale, quant, cliché, calibration).
    """
    analysis = jd_parser.parse_jd(jd_text)
    bank = evidence_bank.parse_bank(framework_cv_text)

    must_terms = analysis["_must_terms"]
    weights = analysis["_scoring_weights"]
    scored_text = cv_text if cv_text is not None else framework_cv_text

    # P0.3 fix: parse_gate=None → otomatik ParseGate hesaplama
    if parse_gate is None:
        _pg_result = cv_parser.parse_safety_score(scored_text)
        parse_gate = _pg_result["score"]

    score = scoring.ats_match_score(
        jd_text, scored_text, must_terms, corpus_texts=corpus_texts,
        weights=weights, parse_gate=parse_gate, use_sbert=use_sbert,
    )

    gaps = synthesis.classify_gaps(score["gap"], bank)
    stop = synthesis.stopping_condition(score["score_percent"], gaps["closable"], target_low)
    stuffing = synthesis.anti_stuffing_report(scored_text, must_terms)

    # 1) keywords (ağırlıklı liste)
    keywords = [
        {"term": m["term"], "modality": ("zorunlu" if m["modality"] >= 1.0 else
                                          "güçlü-ima" if m["modality"] >= 0.7 else "tercih"),
         "positional_weight": m["positional_weight"], "freq": m["freq"]}
        for m in (analysis["must_have"] + analysis["nice_to_have"])
    ]

    # 3) summary
    summary = {
        "role_essence": analysis["intent"],
        "cv_top_summary_hint": (
            "İlk 100–150 kelimede şu zorunlu terimleri konumlandır: "
            + ", ".join(must_terms[:6]) + "."
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
        ) or ["Kapatılabilir gap yok; skor hedefteyse teslim et."],
    }

    # ── Y36-11: Jobscan-style Skill/JD/Resume sayım tablosu ──────────────
    jd_tokens = text.tokenize(jd_text, ngram_max=3, drop_stopwords=True)
    cv_tokens = text.tokenize(scored_text, ngram_max=3, drop_stopwords=True)
    skill_count_table = []
    all_terms = [m["term"] for m in (analysis["must_have"] + analysis["nice_to_have"])]
    for term in all_terms:
        t_low = text.tr_lower(term)
        jd_count = sum(1 for tok in jd_tokens if t_low in tok)
        resume_count = sum(1 for tok in cv_tokens if t_low in tok)
        status = "✅ Match" if resume_count > 0 else "❌ Missing"
        skill_count_table.append({
            "skill": term, "jd_count": jd_count,
            "resume_count": resume_count, "status": status,
        })

    # ── P0.4: 6 QA modülü sonuçları ─────────────────────────────────────────
    qa_checks = {}
    try:
        qa_checks["completeness"] = evidence_recall(framework_cv_text, scored_text)
    except Exception:
        qa_checks["completeness"] = {"error": "evidence_recall hesaplanamadı"}

    try:
        qa_checks["hygiene"] = full_hygiene_check(scored_text)
    except Exception:
        qa_checks["hygiene"] = {"error": "hygiene_check hesaplanamadı"}

    try:
        qa_checks["locale"] = locale_mismatches(jd_text, scored_text)
    except Exception:
        qa_checks["locale"] = {"error": "locale_mismatches hesaplanamadı"}

    try:
        qa_checks["quantification"] = quantification_audit(scored_text)
    except Exception:
        qa_checks["quantification"] = {"error": "quantification_audit hesaplanamadı"}

    try:
        qa_checks["cliches"] = detect_cliches(scored_text)
    except Exception:
        qa_checks["cliches"] = {"error": "detect_cliches hesaplanamadı"}

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
        "note": (
            "Bu alan yalnızca GERÇEK bir dış referans skoru (ör. Jobscan) verildiğinde "
            "anlamlıdır. build_report() dış referans almıyor; motorun kendi skorunu "
            "kendisiyle karşılaştırıp sahte '✅ mükemmel korelasyon' üretmek yerine bu "
            "alan boş bırakıldı (P0-4 fix)."
        ),
    }

    return {
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
        },
        "summary": summary,
        "synthesis": synth,
        "match_score": match_score,
        "gap_analysis": gap_analysis,
        "skill_count_table": skill_count_table,
        "qa_checks": qa_checks,
    }


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
    lang_str = ", ".join(
        f"{lr['language']} ({lr['level']})" if lr.get("level") else lr["language"]
        for lr in idn["language_req"]
    ) or "—"
    lines.append(f"- **Kimlik:** {idn['title_guess']} · kıdem: {idn['seniority']} · çalışma: {idn['work_mode']} · dil: {lang_str} · deneyim: {idn['experience_years'] or '—'}")
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
    lines.append(f"- **Skor:** %{ms['score_percent']} — {ms['verdict']}")
    lines.append(f"- **Bileşenler:** Lex={ms['components']['Lex']} · Sem={ms['components']['Sem']} · "
                 f"Cov={ms['components']['Cov']} · Parse_gate={ms['components']['Parse_gate']} · "
                 f"Stuffing={ms['components']['Stuffing']}")
    lines.append(f"- **Ağırlıklar:** {ms['weights_used']}")
    lines.append(f"- **P/R/F1:** {ms['precision']} / {ms['recall']} / {ms['f1']}")
    if ms.get("warnings"):
        lines.append("- **⚠️ Uyarılar:**")
        for w in ms["warnings"]:
            lines.append(f"  - {w}")
    lines.append("")

    # Y36-11: Jobscan-style sayım tablosu
    lines.append("## Skill Count Table (Jobscan-style)")
    lines.append("| Skill | JD Count | Resume Count | Status |")
    lines.append("|-------|----------|--------------|--------|")
    for row in report.get("skill_count_table", []):
        lines.append(f"| {row['skill']} | {row['jd_count']} | {row['resume_count']} | {row['status']} |")
    lines.append("")

    # P0.4: QA Checks bölümü
    qa = report.get("qa_checks", {})
    if qa:
        lines.append("## QA Checks (v1.5 — 6 modül)")
        if "completeness" in qa and "error" not in qa["completeness"]:
            cr = qa["completeness"]
            lines.append(f"- **Completeness (Evidence Recall):** {cr.get('recall', '?')}")
        if "hygiene" in qa and "error" not in qa["hygiene"]:
            hy = qa["hygiene"]
            lines.append(f"- **Format Hygiene:** word_count={hy.get('word_budget', {}).get('word_count', '?')}, "
                         f"special_chars={hy.get('special_characters', {}).get('count', 0)}")
        if "locale" in qa and "error" not in qa["locale"]:
            lo = qa["locale"]
            lines.append(f"- **Locale:** JD={lo.get('jd_locale', '?')}, CV={lo.get('cv_locale', '?')}, "
                         f"mismatches={lo.get('mismatch_count', 0)}")
        if "quantification" in qa and "error" not in qa["quantification"]:
            qu = qa["quantification"]
            lines.append(f"- **Quantification:** found={qu.get('count', '?')}, "
                         f"target={qu.get('target_min', 5)}, verdict={qu.get('verdict', '?')}")
        if "cliches" in qa and "error" not in qa["cliches"]:
            cl = qa["cliches"]
            lines.append(f"- **Clichés:** count={cl.get('cliche_count', 0)}, "
                         f"severity={cl.get('max_severity', 'none')}")
        # P0-6 fix: calibration_hint JSON'da vardı ama Markdown raporunda hiç
        # görünmüyordu (rapor formatları birbirini tutmuyordu) — artık burada da basılıyor.
        if "calibration_hint" in qa and "error" not in qa["calibration_hint"]:
            ch = qa["calibration_hint"]
            lines.append(f"- **Calibration:** {ch.get('adjustment', '?')} — {ch.get('note', '')}")
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
