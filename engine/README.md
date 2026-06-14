# ats_engine — ATS CV Engine (v1.4.0)

Synthesis-first, audit-corrected ATS-CV engine. **Core runs on standard library only** (zero required dependencies). SBERT is optional; if not installed, the engine gracefully redistributes β weight to α+γ.

## Installation
```bash
cd engine
pip install -e .              # basic (no external deps)
pip install -e ".[semantic]"  # with SBERT (sentence-transformers)
pip install -e ".[dev]"       # tests (pytest) + linting (ruff, mypy)
```

## Quick Usage (CLI)
```bash
python -m ats_engine.cli report --jd examples/sample_jd_foreign_trade.txt \
    --framework examples/framework_cv.md --cv examples/sample_cv.txt --no-sbert --format md
python -m ats_engine.cli score  --jd jd.txt --cv cv.txt --must "SAP,Incoterms,Customs Clearance"
python -m ats_engine.cli parse  --jd jd.txt
python -m ats_engine.cli bank   --framework framework.md
```

## Demo + Tests
```bash
python examples/run_demo.py
pytest -q          # 41 tests
```

## Python API
```python
from ats_engine import build_report, to_markdown
rep = build_report(jd_text, framework_cv_text, cv_text, use_sbert=False)
print(to_markdown(rep))   # 6 fields: keywords/analysis/summary/synthesis/match_score/gap_analysis

# v1.4 quality modules
from ats_engine import (
    detect_cliches,         # buzzword/cliché detection
    quantification_audit,   # metrics counting
    full_hygiene_check,     # format & metadata check
    evidence_recall,        # completeness guard
    detect_locale,          # language consistency
    create_calibration,     # score calibration
)
```

## 18 Modules
**Core:** `text` · `bm25` · `lexicons` · `scoring` · `jd_parser` · `evidence_bank` · `synthesis` · `report` · `cli` · `multilevel` · `cv_parser` · `domain_packs`
**Quality (v1.4):** `calibration` · `cliche_tone` · `completeness_guard` · `format_metadata_hygiene` · `locale_consistency` · `quantification_score`

## Data
- `data/action_verbs.json` — 260+ verbs (TR/EN, 13 categories, cliche_risk tags)
- `data/skill_synonyms.json` — 61 canonicalization entries (LSI/normalize)
- `data/stopwords_tr_en.txt` — Stopwords (TR + EN)
