# Changelog

Tüm önemli değişiklikler bu dosyada belgelenir.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [1.4.0] — 2026-06-13

### Added — New Modules (Phase 0 + Phase 1)
- **calibration.py** — Score calibration module: `create_calibration()`, `suggest_weight_adjustment()`
- **cliche_tone.py** — Buzzword/cliché detector: `detect_cliches()` with severity levels
- **completeness_guard.py** — Section completeness check: `evidence_recall()` measures CV section coverage
- **format_metadata_hygiene.py** — Format & metadata hygiene: `full_hygiene_check()` validates structure
- **locale_consistency.py** — Language consistency check: `detect_locale()`, `locale_mismatches()`
- **quantification_score.py** — Quantification scoring: `quantification_audit()` counts metrics per bullet

### Improved — Phase 0 Enhancements
- **_SPECIAL_CHARS regex** expanded — now catches `·`, `—`, `""`, `''` and more ATS-problematic chars
- **action_verbs.json** — added `cliche_risk` field to flag overused verbs (spearheaded, orchestrated, etc.)
- **report.py** — new Skill|JD|Resume count table in output
- **skill_synonyms.json** — expanded from 52 to 61 canonicalization entries
- **text.py** — `tr_lower()` function for proper Turkish İ/ı/Ş/ş case folding
- **docs/14-pipeline-stages.md** — new pipeline stages documentation
- **sample_cv.txt** — cleaned special characters

### Tests
- 13 new tests added (Phase 0 + Phase 1)
- **Total: 41/41 tests passing**

---

## [1.3.0] — 2026-06-14

### Added — Yeni Özellikler
- **domain_packs.py** modülü — Alan-özel anahtar kelime paketi yükleyici (ATSE-8)
  - `load_pack()`, `list_packs()`, `all_keywords()`, `keywords_by_category()`
  - `enrich_must_terms()` — zorunlu terimleri alan paketiyle zenginleştirir
  - `detect_domain()` — JD metninden otomatik alan tespiti
  - `__init__.py`'ye tam export
- **ruff + mypy + pre-commit** yapılandırması (ATSE-13)
  - `pyproject.toml`'a ruff lint/format, mypy strict, pytest config eklendi
  - `.pre-commit-config.yaml` — ruff, mypy, trailing-whitespace, check-json hooks

### Fixed — Düzeltmeler
- **BM25 entegrasyonu** — `BM25.score()` artık scoring pipeline'da aktif (ATSE-5)
  - `Lex = 0.70 × TF-IDF_cosünüs + 0.30 × BM25_normalize`
  - Components çıktısına `Lex_tfidf` ve `Lex_bm25` eklendi
- **Jaccard dinamik eşik** — Kısa terimlerde false positive önlendi (ATSE-7)
  - 1 kelime → 0.80 eşik, 2 kelime → 0.50, 3+ kelime → 0.34
- **LangGate düzeltmesi** — Karışık dilli CV'lerde artık gerçekten tetikleniyor (ATSE-9)
  - Bilinmeyen kelimeler 0.5 ağırlıkla sayılıyor (eski: 1.0 → purity şişiyordu)
- **Precision/Recall bağımsızlığı** — P artık R'nin proxy'si değil (ATSE-11)
  - CV'den otomatik unigram tokenize → gerçek precision hesaplanıyor

### Removed — Kaldırılan
- 3 stale branch silindi (ATSE-12)
- PR #1 ve Issue #2 kapatıldı (ATSE-10)

### Tests
- 7 yeni test eklendi (Sprint 2): BM25 components, Jaccard dynamic, domain_packs, LangGate, precision
- **Toplam: 28/28 test geçiyor**

---

## [1.2.0] — 2026-06-13

### Fixed — Sprint 1 "Temel Onarım" (5 CRITICAL/HIGH bug)
- **cv_parser orphan** — ParseGate `None` → otomatik `parse_safety_score()` çağrısı (ATSE-1)
- **must_have boş → skor çökmesi** — `coverage()` early return `1.0, []` (ATSE-2)
- **Dual scoring engine drift** — `ats_score.py` thin wrapper olarak refactor (ATSE-3)
- **Data dosyaları paketlenmiyordu** — `pyproject.toml` + `MANIFEST.in` düzeltmesi (ATSE-4)
- **SBERT her çağrıda yeniden yüklüyordu** — `_get_sbert_model()` singleton (ATSE-6)

### Tests
- 3 yeni test eklendi (Sprint 1): parse_gate auto, empty must_have, SBERT singleton
- **Toplam: 29/29 test geçiyor** (o dönem)

---

## [1.1.0] — 2026-06-12

### Added
- İlk tam motor sürümü: text, bm25, scoring, lexicons, jd_parser, evidence_bank, synthesis, report, multilevel, cv_parser
- 7 katmanlı JD ayrıştırıcı
- 3 seviyeli ATS skorlama (L1 gate, L2 best-of-8, L3 category robustness)
- LangGate dil tutarlılığı kapısı
- XYZ/CAR cümle sentezi + anti-stuffing
- domain-packs/foreign-trade-logistics (EN + TR)
- CI/CD (GitHub Actions)
- 18 çekirdek test

---

## [1.0.0] — 2026-06-11

### Added
- İlk repo oluşturma ve temel yapı
