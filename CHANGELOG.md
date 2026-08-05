# Changelog

Tüm önemli değişiklikler bu dosyada belgelenir.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [2.0.0-alpha.1] — 2026-08-05

### Added

- Kabul edilmiş ADR-001 ve SHA-bağlı v2 baseline manifesti
- 12 tipli Python contract, ortak enum/hata taksonomisi, G0–G4 `DecisionReport`
- Kapalı Draft 2020-12 JSON şemaları ve tüm contract tipleri için golden payload’lar
- Gerçek DOCX OOXML ve PDF text-layer ingestion; scanned/mixed PDF explicit durumları
- Evidence ID + allowlist + protected-fact kontrollü `SynthesisChangeSet`
- CLI `ingest` komutu ve exit `4=blocking/review` sözleşmesi
- Paket manifest snapshot, clean-wheel smoke, schema/golden ve güvenlik CI kapıları

### Changed

- Boş explicit must listesi artık genel skor üretmiyor: `NOT_EVALUATED/REVIEW`
- Geçersiz gate değerleri clamp edilmek yerine tipli `INVALID_INPUT` hatası veriyor
- Gövde becerileri must listesine terfi etmiyor; advisory/nice olarak kalıyor
- Lexical evidence overlap artık “doğrulandı/PASS” değil `UNVERIFIED/REVIEW`
- Runtime kaynakları `importlib.resources` ile yükleniyor; eksik paket verisi sessiz fallback yapmıyor
- LangGate `report.py` akışına bağlandı; JSON/Markdown/CLI ortak karar payload’ı kullanıyor
- Aktif dokümanlar v2 ürün sözleşmesiyle senkronlandı; v1.x metodoloji açıkça legacy işaretlendi

### Verification

- 87 unit/contract/ingestion/regression testi; resmi `REG-001..015` matrisi
- Ruff lint + format, mypy, wheel/sdist, clean install ve schema validation

### Known limits

- OCR adapter, commercial ATS tenant ölçümü, hiring outcome çalışması, production export,
  kalıcı evidence/event store ve UI/otomasyon bu alpha’da yoktur.

## [1.5.1] — 2026-08-03

**Bağlam:** `1.5.0` hiçbir zaman gerçek bir GitHub tag/release olarak yayınlanmamıştı
(`pyproject.toml` sürümü commit geçmişiyle uyumsuzdu — bkz. ADR-000). Bu sürüm, 5 turluk
dış AI denetiminin (ChatGPT+Claude) kanonik P0 listesindeki (A1-A12) tüm kod-seviyesi
maddeleri kapatan **v1.5.1 güven/stabilizasyon** sürümüdür. Bkz. `docs/decisions/ADR-000-pre-production-status.md`.

### Fixed — P0 (PR #4, `fix/p0-stabilization`)
- Boş `must_have` artık sahte `coverage=1.0` üretmiyor (fail-open kapatıldı)
- `matches_semantically()` artık kelime sınırı kullanıyor ("SAP" ≠ "sapphire")
- `action_verbs_by_intent()` artık asla sessizce `[]` dönmüyor
- Motorun kendi skorunu kendisiyle karşılaştıran sahte kalibrasyon kaldırıldı
- Wheel paketi artık runtime verisini (`data/`, `domain-packs/`) içeriyor
- JD gövde-fallback artık anlamsız kısaltmaları ("MM" vb.) zorunlu şart saymıyor
- Dil + seviye (CEFR) eşleştirmesi düzeltildi
- Markdown/JSON rapor alan tutarsızlığı giderildi
- Ruff: 41 bulgu → 0

### Fixed — P1 (bu sürüm, `fix/p1-hardening`)
- **Tipli hata sözleşmesi:** `report.py`/`scoring.py`'deki 7 sessiz `except Exception`
  bloğu artık loglanıyor (`logging.warning`, traceback dahil) ve gerçek hata
  tipi+mesajı rapora ekleniyor (`error_type`, `error_detail`) — eskiden yalnızca
  sabit "hesaplanamadı" metni vardı, gerçek arıza bilgisi kayboluyordu.
- **Sınır doğrulama:** `parse_gate`/`lang_gate` artık [0,1] dışı veya NaN değerleri
  sessizce kabul etmiyor — NaN fail-closed (0.0) olarak ele alınıyor, [0,1] dışı
  değer clamp ediliyor, her ikisi de rapora `warnings` olarak ekleniyor.
- **Tip kontrolü:** `mypy` (zaten `pyproject.toml`'da yapılandırılmıştı ama hiç
  çalıştırılmıyordu) artık CI + `make check`'in bir parçası; 8 tip hatası düzeltildi,
  şu an 0 hata.
- **Ürün dili dürüstlüğü:** "%75-85 mülakata hazır", "ATS'den/ATS'yi geçme" gibi
  garanti ima eden ifadeler 6 docs dosyasında ("hizalanma sinyali, garanti değil"
  çerçevesine) yeniden yazıldı (`03-skorlama-matematigi.md`, `11-uc-seviyeli-skorlama.md`,
  `13-grammarly-kapisi.md`, `architecture/system-overview.md`, `research/R3-seo-ats-sozluk.md`,
  `audits/ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md`).

### Added
- `docs/decisions/ADR-000-pre-production-status.md` — dondurulmuş, dürüst durum beyanı
- 4 yeni regresyon testi (`test_parse_gate_nan_is_fail_closed_with_warning`,
  `test_parse_gate_out_of_range_is_clamped_with_warning`,
  `test_parse_gate_valid_value_unchanged_no_warning`,
  `test_qa_check_failure_surfaces_real_error_not_silent`)
- CI: `ruff check` + `mypy` adımları (önceden yapılandırılmış ama hiç çalıştırılmıyordu)
- `make typecheck` hedefi; `make check` artık lint+typecheck+test çalıştırıyor

### Tests
- **Total: 55/55 tests passing** (was 51)

> **📌 2026-08-04 canlı doğrulama düzeltmesi:** `v1.5.1` tag'inin kendi commit'i
> (`git show v1.5.1:engine/tests/`) fiilen **64 test** içeriyor
> (`test_core.py`: 61, `test_cli.py`: 3) — üstteki "55/55" rakamı, bu satırı yazan
> commit'in (`f3ee0fd`) kendi mesajıyla bile tutarsızdı (o da "61/61" diyordu).
> Taze `git clone` + izole venv'de `pytest engine/tests/ -q` ile doğrulandı: **64 passed**.
> Bu not, geçmiş kaydı silmeden düzeltme şeffaflığı için eklendi.
>
> Ayrıca: yukarıdaki "CI: `ruff check` + `mypy` adımları... artık CI'nin bir parçası"
> maddesi **canlı `.github/workflows/test.yml` ile uyuşmuyor** — o dosya şu an
> yalnızca `pytest` + CLI smoke test çalıştırıyor, ruff/mypy adımı içermiyor. Bu,
> muhtemelen workflow dosyası push'unun GitHub Actions izniyle reddedilmesi
> yüzünden hiç uygulanamamış bir değişiklik (bkz. Viktor'un kullanıcı notları —
> "2 Ruff+mypy YAML satırı bekliyor, önerildi, hiç gönderilmedi"). Lint/typecheck
> hâlâ yalnızca yerelde `make check` ile veya pre-commit hook'uyla çalışıyor, CI'da
> zorunlu değil. Manuel eklenecek YAML parçası ayrıca sunulabilir.

### Kapsam dışı (henüz yapılmadı, ayrı karar/faz gerektiriyor)
- REG-001..015 numaralı resmi regresyon test kimlikleri (yerine yukarıdaki 4 test eklendi,
  ama kanonik dokümanların önerdiği numaralandırma şeması uygulanmadı)
- v2.0 contract-first mimarisi (B serisi, ADR-001+)
- F1 canonical_id eşleme tablosu (Linear/Jira/Asana/Monday'a canlı yazma erişimi yok)
- **CI'ya `ruff check` + `mypy` adımlarının fiilen eklenmesi** (yukarıdaki düzeltme
  notuna bakınız — bu hâlâ açık bir madde, `v1.5.1`'de kapanmadı)

## [1.5.0] — 2026-06-15

### Fixed — P0 Critical (Viktor Hybrid Revizyon v2.0, 8+ AI çapraz-doğrulama)
- **P0.1 tr_lower() acronym-safe** — `I`→`ı` eşlemesi kaldırıldı; `INCOTERMS`→`incoterms` artık doğru (text.py:26)
- **P0.2 Dead assertion** — `assert detected is not None or True` → gerçek tip kontrolü (test_core.py:222)
- **P0.3 ParseGate auto** — `build_report(parse_gate=None)` → `cv_parser.parse_safety_score()` otomatik çağrılır (report.py, cli.py)
- **P0.4 6 QA modülü wired** — completeness_guard, format_metadata_hygiene, locale_consistency, quantification_score, cliche_tone, calibration artık `build_report()` çıktısına bağlı (`qa_checks` alanı)
- **P0.8 CHANGELOG date** — v1.3.0 tarihi 2026-06-14→2026-06-12 düzeltildi (kronolojik sıra)

### Added — New Documentation
- **docs/decision_engine.md** — 5-gate karar motoru mimarisi
- **docs/diagnostic_tree.md** — 7-dallı ATS tanı ağacı (Ads Toolkit'ten uyarlandı)
- **docs/module_status.md** — 5-seviyeli modül durum matrisi
- **docs/maturity_model.md** — 4-aşamalı repo olgunluk modeli
- **config/user_profile.yaml** — Kullanıcı profili konfigürasyonu (Desen 8)

### Changed
- **report.py** — `parse_gate` default `1.0` → `None` (otomatik), QA modülleri entegre
- **cli.py** — `--parse-gate` default `None` (report komutu otomatik, score komutu 1.0)
- **__init__.py** — versiyon 1.4.0 → 1.5.0

### Tests
- Dead assertion düzeltildi (P0.2)
- P0.1 acronym testi eklendi
- **Total: 43/43 tests passing**

---

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

## [1.3.0] — 2026-06-12

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
