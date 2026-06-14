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

from . import jd_parser, scoring, synthesis, evidence_bank, text


def build_report(jd_text: str, framework_cv_text: str, cv_text: str | None = None,
                 parse_gate: float = 1.0, corpus_texts: list[str] | None = None,
                 use_sbert: bool = True, target_low: float = 75.0) -> dict:
    """JD + Framework CV (+ opsiyonel mevcut CV) → 6 alanlık yapılandırılmış rapor."""
    analysis = jd_parser.parse_jd(jd_text)
    bank = evidence_bank.parse_bank(framework_cv_text)

    must_terms = analysis["_must_terms"]
    weights = analysis["_scoring_weights"]
    scored_text = cv_text if cv_text is not None else framework_cv_text

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
        },
        "summary": summary,
        "synthesis": synth,
        "match_score": match_score,
        "gap_analysis": gap_analysis,
        "skill_count_table": skill_count_table,
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
    lines.append(f"- **Kimlik:** {idn['title_guess']} · kıdem: {idn['seniority']} · çalışma: {idn['work_mode']} · dil: {', '.join(idn['language_req']) or '—'} · deneyim: {idn['experience_years'] or '—'}")
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
    lines.append("")

    # Y36-11: Jobscan-style sayım tablosu
    lines.append("## Skill Count Table (Jobscan-style)")
    lines.append("| Skill | JD Count | Resume Count | Status |")
    lines.append("|-------|----------|--------------|--------|")
    for row in report.get("skill_count_table", []):
        lines.append(f"| {row['skill']} | {row['jd_count']} | {row['resume_count']} | {row['status']} |")
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
