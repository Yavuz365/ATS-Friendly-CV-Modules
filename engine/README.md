# ats_engine — Çalışan ATS Motoru

Sentez-önce, audit-düzeltmeli ATS-CV motoru. **Çekirdek yalnızca standart kütüphane** ile çalışır (zorunlu bağımlılık yok). SBERT opsiyoneldir; kurulu değilse motor zarifçe SBERT'siz çalışır (β payını α+γ'ya dağıtır).

## Kurulum
```bash
cd engine
pip install -e .            # opsiyonel; ya da doğrudan çalıştır
pip install -e ".[semantic]"  # SBERT (sentence-transformers) ile
pip install -e ".[dev]"       # testler (pytest)
```

## Hızlı kullanım (CLI)
```bash
python -m ats_engine.cli report --jd examples/sample_jd_foreign_trade.txt \
    --framework examples/framework_cv.md --cv examples/sample_cv.txt --no-sbert --format md
python -m ats_engine.cli score  --jd jd.txt --cv cv.txt --must "SAP,Incoterms,Customs Clearance"
python -m ats_engine.cli parse  --jd jd.txt
python -m ats_engine.cli bank   --framework framework.md
```

## Demo + test
```bash
python examples/run_demo.py
pytest -q          # 19 test
```

## Python API
```python
from ats_engine import build_report, to_markdown
rep = build_report(jd_text, framework_cv_text, cv_text, use_sbert=False)
print(to_markdown(rep))   # 6 alan: keywords/analysis/summary/synthesis/match_score/gap_analysis
```

## Modüller
`text` (tokenizer/n-gram/quantification) · `bm25` (Okapi) · `lexicons` (action_verbs + synonyms/LSI + jaccard) · `scoring` (TF-IDF kosinüs, SBERT, kapsama, hibrit skor) · `jd_parser` (7 katman) · `evidence_bank` (provenans) · `synthesis` (küme/XYZ/gap/durma) · `report` (6 alan) · `cli`.

## Veri
`data/action_verbs.json` (Grammarly-türevi), `data/skill_synonyms.json` (LSI/normalize), `data/stopwords_tr_en.txt`.
