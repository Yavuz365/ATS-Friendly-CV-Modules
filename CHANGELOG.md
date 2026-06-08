# Changelog

## v1.1.0 — 2026-06-08

### Yeni Özellikler
- **`multilevel.py`** — 3-seviyeli ATS skorlama: L1 araç kapısı → L2 8-parça en-iyi → L3 kategori robustness
- **`cv_parser.py`** — CV bölüm tespiti + ATS parse güvenlik skoru
- **LangGate** — Dil tutarlılığı kapısı (`scoring.py`'ye entegre)
- **`prompts/master-prompt-EN.md`** — İngilizce Master Prompt
- **`prompts/adapters/`** — 6 AI araç adaptörü (ChatGPT, Claude, Gemini, Copilot, Perplexity, DeepSeek)
- **`domain-packs/foreign-trade-logistics/`** — TR/EN alan-özel terim paketleri
- **`schemas/scoring_result.schema.json`** — Skor çıktı JSON şeması
- **`.github/workflows/test.yml`** — CI/CD (pytest + CLI smoke test, Python 3.10-3.12)
- **docs/08-13** — 6 yeni dokümantasyon dosyası

### İyileştirmeler
- `action_verbs.json`: 117 → 320 fiil (dış ticaret + lojistik + tedarik zinciri kategorileri)
- `skill_synonyms.json`: 15 → 52 kanonikleme girdisi
- Araç-bağımsızlaştırma: tüm Gemini/n8n referansları genelleştirildi
- README tamamen yeniden yazıldı

### Düzeltmeler
- `scoring.py`: `lang_gate` parametresi eklendi (hibrit skor formülüne çarpan olarak)

## v1.0.0 — 2026-06-07

### İlk Sürüm
- Python motoru (engine/): BM25, TF-IDF, SBERT, kapsam, şişirme, 7-katman JD ayrıştırma
- 19 birim testi (tümü geçiyor)
- CLI: report/score/parse/bank komutları
- Kanıt bankası + provenans doğrulama
- Sentez: XYZ/CAR, gap sınıflandırma, anti-stuffing, H1 durma koşulu düzeltmesi
- Dokümantasyon (docs/00-07)
- Skills, templates, workflows, prompts
- Makefile: install/dev/demo/test/score/clean
