# ATS-Friendly-CV-Modules

> **Evidence-based, AI-agnostic ATS CV Engine**

A deterministic Python engine that measures job description (JD) to CV alignment, guides evidence-based CV generation, and prevents hallucination through provenance tracking.

[![CI](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions/workflows/test.yml/badge.svg)](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Version](https://img.shields.io/badge/version-1.5.1-green)
![Tests](https://img.shields.io/badge/tests-43%20passed-brightgreen)
![License](https://img.shields.io/badge/license-Proprietary-red)

---

## 🎯 What It Does

```
Job Description (JD)  ──→  7-Layer Decomposition  ──→  Hybrid ATS Score  ──→  Gap Analysis
                                 │                            │                       │
Framework CV  ──────→  Evidence Bank  ──→  Provenance Check  ──→  Revision Loop
```

1. **Decomposes JD into 7 layers** — must-have terms, skills, intent, weights
2. **Computes hybrid score** — BM25 + TF-IDF + SBERT + Coverage − Stuffing penalty
3. **Gap analysis** — closable vs unclosable gaps
4. **Provenance verification** — every CV bullet traces to Framework CV; fabrication blocked
5. **3-level scoring** — Tool gate → 8-part best-of → Category robustness

## 🏗️ Repository Structure

```
ATS-Friendly-CV-Modules/
├── engine/                           ← Python engine (core)
│   ├── ats_engine/
│   │   ├── __init__.py               ← All API exports (v1.5.0)
│   │   ├── scoring.py                ← Hybrid ATS Match Score (TF-IDF+BM25+SBERT)
│   │   ├── multilevel.py             ← 3-level scoring + LangGate
│   │   ├── cv_parser.py              ← CV section detection + parse safety score
│   │   ├── jd_parser.py              ← 7-layer JD decomposition
│   │   ├── bm25.py                   ← Okapi BM25 (Lex=0.70×TF-IDF+0.30×BM25)
│   │   ├── evidence_bank.py          ← Evidence bank + provenance
│   │   ├── synthesis.py              ← XYZ/CAR, gap classification, anti-stuffing
│   │   ├── lexicons.py               ← Skill normalization, synonym matching
│   │   ├── text.py                   ← Tokenization, n-gram, stopwords, tr_lower()
│   │   ├── report.py                 ← 6-field output (JSON + Markdown)
│   │   ├── domain_packs.py           ← Domain-specific keyword pack loader (v1.3)
│   │   ├── calibration.py            ← Score calibration module (v1.4)
│   │   ├── cliche_tone.py            ← Buzzword/cliché detector (v1.4)
│   │   ├── completeness_guard.py     ← Section completeness check (v1.4)
│   │   ├── format_metadata_hygiene.py← Format & metadata hygiene (v1.4)
│   │   ├── locale_consistency.py     ← Language consistency check (v1.4)
│   │   ├── quantification_score.py   ← Quantification/metrics scoring (v1.4)
│   │   ├── cli.py                    ← Command-line interface
│   │   ├── data/                     ← P0-5 fix: moved INSIDE the package (was engine/data/)
│   │   │   ├── action_verbs.json     ← 260+ action verbs (TR/EN, 13 categories, cliche_risk)
│   │   │   ├── skill_synonyms.json   ← 61 canonicalization entries
│   │   │   └── stopwords_tr_en.txt   ← Stopwords (TR + EN)
│   │   └── domain_pack_data/         ← P0-5 fix: moved INSIDE the package (was repo-root domain-packs/)
│   │       └── foreign-trade-logistics/
│   │           ├── keywords_en.json  ← 65 keywords (English)
│   │           └── keywords_tr.json  ← 73 keywords (Turkish)
│   ├── tests/test_core.py            ← 43 unit tests
│   ├── examples/
│   │   ├── run_demo.py
│   │   ├── sample_jd_foreign_trade.txt
│   │   ├── sample_cv.txt
│   │   └── framework_cv.md
│   ├── pyproject.toml                ← pip install -e engine/
│   ├── requirements.txt
│   └── MANIFEST.in
│
├── config/                           ← Configuration (v1.5)
│   └── user_profile.yaml            ← User profile config (scoring prefs, targets)
│
├── docs/                             ← Methodology documentation
│   ├── 00-mimari.md … 14-pipeline-stages.md  (15 main documents)
│   ├── decision_engine.md            ← 5-gate karar motoru mimarisi (v1.5)
│   ├── diagnostic_tree.md            ← 7-dallı ATS tanı ağacı (v1.5)
│   ├── module_status.md              ← 5-seviyeli modül durum matrisi (v1.5)
│   ├── maturity_model.md             ← 4-aşamalı repo olgunluk modeli (v1.5)
│   ├── architecture/                 ← System architecture
│   │   ├── system-overview.md
│   │   └── provenance-and-anti-hallucination.md
│   ├── audits/                       ← Audit reports
│   │   └── ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md
│   ├── migration/                    ← Legacy migration guide
│   │   └── legacy-map.md
│   └── research/                     ← Research notes
│       ├── R1-sistemik-veri-ats-mimarisi.md
│       ├── R2-sentez-once-analiz.md
│       └── R3-seo-ats-sozluk.md
│
├── prompts/                          ← Master Prompt (TR + EN)
│   ├── master-prompt-TR.md           ← Portable Turkish prompt
│   ├── master-prompt-EN.md           ← Portable English prompt
│   ├── output-fields-template.md     ← 6-field output template
│   └── adapters/                     ← AI tool adapters
│       ├── chatgpt.md, claude.md, gemini.md
│       ├── copilot.md, deepseek.md, perplexity.md
│
├── references/                       ← ATS knowledge base
│   └── ats-kb/
│       ├── ats-parser-rules.md       ← ATS parser rules
│       ├── jd-taxonomy.md            ← JD taxonomy (7-layer)
│       └── keyword-ontology.md       ← Keyword classification ontology
│
├── schemas/                          ← JSON output schemas
│   └── scoring_result.schema.json
│
├── skills/                           ← AI skill files
│   ├── ats-cv-architect/             ← Main CV engine skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── references/
│   │   └── scripts/ats_score.py
│   └── synthesis-analysis-research/  ← Research/analysis skill
│       ├── SKILL.md
│       └── references/
│
│   (domain-packs moved → engine/ats_engine/domain_pack_data/, see below;
│    P0-5 packaging fix: data must live inside the installable package)
│
├── templates/                        ← JD/CV templates
│   ├── jd-etiketli-sablon.md
│   └── kanit-bankasi-sablonu.md
│
├── workflows/                        ← Automation pipeline docs
│   ├── automation/ats-cv-pipeline.md
│   └── notion/veritabani-semasi.md
│
├── archive/                          ← Legacy skill files (reference)
│   ├── ats-cv-architect_TUM-SKILL-BIRLESIK.md
│   └── synthesis-analysis-research_FULL.md
│
├── .github/workflows/test.yml        ← CI/CD (pytest + smoke test)
├── .pre-commit-config.yaml           ← ruff + mypy + hooks
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
└── .gitignore
```

## 🚀 Quick Start

### Installation

```bash
# Basic install (zero external dependencies)
pip install -e engine/

# Developer mode (pytest + ruff + mypy included)
pip install -e "engine/[dev]"

# With semantic similarity (optional, SBERT)
pip install -e "engine/[semantic]"
```

### CLI Usage

```bash
# Full JD-CV report (6 fields)
python -m ats_engine.cli report \
    --jd jobs/jd.txt \
    --framework cvs/framework_cv.md \
    --format json

# Score only
python -m ats_engine.cli score \
    --jd jobs/jd.txt \
    --cv cvs/cv.txt \
    --must "letter of credit,incoterms,GTIP"

# JD decomposition (7 layers)
python -m ats_engine.cli parse --jd jobs/jd.txt

# Framework CV → Evidence bank
python -m ats_engine.cli bank --cv cvs/framework_cv.md
```

### Python API

```python
from ats_engine import ats_match_score, parse_jd, build_report

# One-line hybrid score
result = ats_match_score(jd_text, cv_text, ["letter of credit", "incoterms", "GTIP"])
print(f"Score: {result['score_percent']}%")
print(f"Verdict: {result['verdict']}")
print(f"Components: {result['components']}")
print(f"Gaps: {result['gap']}")

# 7-layer JD decomposition
jd = parse_jd(jd_text)
print(jd["must_have"])      # required terms
print(jd["nice_to_have"])   # preferred terms

# Full 6-field report
report = build_report(jd_text, framework_cv_text)

# 3-level scoring
from ats_engine import level1_gate, level2_final, level3_category, lang_gate

l1 = level1_gate(jd_text, cv_text, must_terms)        # L1: single tool gate
l2 = level2_final(jd_text, tool_sections, must_terms)  # L2: 8-part best-of
l3 = level3_category(cv_text, jd_texts, must_terms)    # L3: category robustness
lg = lang_gate(cv_text, jd_text)                       # language consistency gate

# v1.4 modules
from ats_engine import (
    evidence_recall,           # completeness guard
    full_hygiene_check,        # format & metadata hygiene
    detect_locale,             # locale consistency
    quantification_audit,      # quantification scoring
    detect_cliches,            # cliché/buzzword detection
    create_calibration,        # score calibration
)
```

## 📐 Scoring Formula

```
H(CV, JD) = LangGate × ParseGate × clamp(α·Lex + β·Sem + γ·Cov − ζ·Stuff, 0, 1)
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| α | 0.35 | Lexical: TF-IDF cosine (0.70) + BM25 (0.30) |
| β | 0.30 | Semantic: SBERT cosine similarity |
| γ | 0.35 | Coverage: must-have term coverage |
| ζ | 0.20 | Stuffing: keyword stuffing penalty |
| ParseGate | 0–1 | CV format parsability score |
| LangGate | 0–1 | Language consistency gate |

**Target band:** 75%–85% | >90% = stuffing signal | <50% = major improvement needed

If SBERT is not installed, β is automatically redistributed to α+γ (graceful degradation).

## 🔬 3-Level Scoring

| Level | Function | Threshold |
|-------|----------|-----------|
| L1: Tool Gate | Scores a single AI tool's CV against JD | τ = 0.70 |
| L2: 8-Part Best-of | Selects best section score + seam penalty | κ = 0.15 |
| L3: Category Robustness | Tests combined CV against 3+ JDs | σ ≤ 0.10 |

## 🛡️ Tool-Agnostic Principle

This repo is **not dependent on any AI tool**:

- Engine (`engine/`) is pure Python — works independently of any LLM
- Master Prompt can be copied to any LLM (ChatGPT, Claude, Gemini, Copilot, etc.)
- AI tool adapters (`prompts/adapters/`) optimize for each LLM's strengths
- Automation integrates with any platform (n8n, Make, Zapier, etc.)

## 📚 Documentation

### Core Docs (docs/)

| File | Topic |
|------|-------|
| [00-mimari.md](docs/00-mimari.md) | System architecture |
| [01-metodoloji.md](docs/01-metodoloji.md) | Dialectic methodology |
| [02-jd-decomposition.md](docs/02-jd-decomposition.md) | 7-layer JD decomposition |
| [03-skorlama-matematigi.md](docs/03-skorlama-matematigi.md) | Hybrid scoring formulas |
| [04-sentez-kurallari.md](docs/04-sentez-kurallari.md) | XYZ/CAR synthesis rules |
| [05-grammarly-entegrasyonu.md](docs/05-grammarly-entegrasyonu.md) | Grammarly integration |
| [06-denetim-ve-duzeltmeler.md](docs/06-denetim-ve-duzeltmeler.md) | Audit fixes |
| [07-workflow-multitool.md](docs/07-workflow-multitool.md) | Multi-tool workflow |
| [08-kategorizasyon-taksonomisi.md](docs/08-kategorizasyon-taksonomisi.md) | Job posting categorization |
| [09-orkestrasyon-katmanlari.md](docs/09-orkestrasyon-katmanlari.md) | Pipeline orchestration |
| [10-sekiz-parca-skorlama.md](docs/10-sekiz-parca-skorlama.md) | 8-part scoring + QA |
| [11-uc-seviyeli-skorlama.md](docs/11-uc-seviyeli-skorlama.md) | 3-level score math |
| [12-dil-tutarliligi.md](docs/12-dil-tutarliligi.md) | Language consistency + TR morphology |
| [13-grammarly-kapisi.md](docs/13-grammarly-kapisi.md) | Grammarly gate |
| [14-pipeline-stages.md](docs/14-pipeline-stages.md) | Pipeline stages |

### v1.5 New Docs

| File | Content |
|------|---------|
| [docs/decision_engine.md](docs/decision_engine.md) | 5-gate karar motoru mimarisi |
| [docs/diagnostic_tree.md](docs/diagnostic_tree.md) | 7-dallı ATS tanı ağacı |
| [docs/module_status.md](docs/module_status.md) | 5-seviyeli modül durum matrisi |
| [docs/maturity_model.md](docs/maturity_model.md) | 4-aşamalı repo olgunluk modeli |
| [config/user_profile.yaml](config/user_profile.yaml) | Kullanıcı profili konfigürasyonu |

### Additional Docs

| Folder | Content |
|--------|---------|
| [docs/architecture/](docs/architecture/) | System overview + provenance/anti-hallucination |
| [docs/audits/](docs/audits/) | Setup findings and audit report |
| [docs/migration/](docs/migration/) | Legacy migration guide |
| [docs/research/](docs/research/) | ATS architecture, synthesis analysis, SEO glossary |

### Knowledge Base (references/ats-kb/)

| File | Content |
|------|---------|
| [ats-parser-rules.md](references/ats-kb/ats-parser-rules.md) | ATS parser rules, format penalties |
| [jd-taxonomy.md](references/ats-kb/jd-taxonomy.md) | JD 7-layer model details |
| [keyword-ontology.md](references/ats-kb/keyword-ontology.md) | Keyword classification & synonym expansion |

## 🧪 Tests

```bash
# Run tests
cd engine && pip install -e ".[dev]" && pytest tests/ -v
```

43 tests covering: clamp, gate, H1 stopping condition, gap classification, 6-field output, BM25 pipeline, anti-stuffing, parse gate auto-call, empty must_have, SBERT singleton, Jaccard dynamic threshold, domain packs, LangGate trigger, precision independence, completeness guard, format hygiene, locale detection, quantification audit, cliché detection, calibration, acronym-safe tr_lower (P0.1), QA checks wiring (P0.4).

CI/CD: Tests run automatically on Python 3.10, 3.11, 3.12 on every push.

## ⚖️ Ethical Principles

- ❌ Experience, metrics, or certifications are **NEVER fabricated**
- ✅ Every CV bullet is backed by Framework CV (provenance)
- ✅ Keyword stuffing is detected and penalized (ζ = 0.20)
- ✅ 75%–85% target band — over-optimization is flagged
- ✅ LangGate checks language consistency
- ✅ Cliché/buzzword detection warns against generic language

## 📦 Version

Current: **v1.5.1** — see [CHANGELOG.md](CHANGELOG.md) for full history and
[ADR-000](docs/decisions/ADR-000-pre-production-status.md) for the honest pre-production
status statement (this is a research prototype; not validated against real commercial ATS
tenants — see "Dürüst statü" in `docs/03-skorlama-matematigi.md`).

### Version History
| Version | Date | Highlights |
|---------|------|------------|
| v1.5.1 | 2026-08-03 | Canonical P0 hardening: typed error contract, gate boundary validation, mypy in CI, honest product-language pass over score-band docs (see ADR-000) |
| v1.5.0 | 2026-06-15 | P0 critical fixes (5), 6 QA modules wired, 4 new docs, config layer, 43 tests (never tagged as a real release — see ADR-000) |
| v1.4.0 | 2026-06-13 | 6 new modules (calibration, cliché, completeness, format, locale, quantification) |
| v1.3.0 | 2026-06-12 | BM25 pipeline, Jaccard dynamic, domain_packs, LangGate fix, ruff+mypy |
| v1.2.0 | 2026-06-13 | 5 critical bug fixes (ParseGate, must_have, dual engine, data packaging, SBERT cache) |
| v1.1.0 | 2026-06-12 | Initial full engine release |
| v1.0.0 | 2026-06-11 | Repository creation |

## 📄 License

Proprietary — all rights reserved. See [LICENSE](LICENSE) for details.
