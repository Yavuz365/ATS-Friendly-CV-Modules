# ATS-Friendly-CV-Modules

> Evidence-first CV analysis research engine. **Pre-production contract alpha; not a
> commercial ATS pass, interview, or hiring-outcome predictor.**

[![CI](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions/workflows/test.yml/badge.svg)](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Version](https://img.shields.io/badge/version-2.0.0--alpha.2-orange)
![License](https://img.shields.io/badge/license-Proprietary-red)

## Ne yapar?

- Açık JD gereksinimlerini ayırır; açık must bölümü yoksa must uydurmaz ve `REVIEW` verir.
- Lexical/semantic hizalanmayı tanı olarak hesaplar. Must listesi boşsa genel skor
  üretmez: `score_percent=null`, `NOT_EVALUATED`.
- DOCX’in OOXML metnini (gövde, tablo, header/footer, text-box) ve PDF text layer’ını okur.
  Scanned PDF OCR yoksa açık hata; mixed PDF `REVIEW` üretir.
- Sözcüksel evidence desteğini `UNVERIFIED` olarak işaretler; olgusal doğrulama iddiası yapmaz.
- G0–G4 kapıları ve insan onayını tek, tipli `DecisionReport` içinde birleştirir.
- Sentez önerilerini allowlist CV yolları ve bilinen evidence ID’leriyle sınırlar;
  şirket/unvan/tarih/derece/dil seviyesi/metrik gibi aday olgularını korur.

## Hızlı başlangıç

```bash
pip install -e engine/

# Gerçek belge ingestion
ats-engine ingest --document cv.docx
ats-engine ingest --document cv.pdf

# JD ayrıştırma
ats-engine parse --jd job.txt

# Evidence-first rapor (REVIEW durumunda CLI exit 4 döner)
ats-engine report --jd job.txt --framework framework_cv.md --cv cv.txt --format json --no-sbert

# Yalnız tipli G0-G4 karar raporu
ats-engine diagnose --jd job.txt --cv cv.txt --framework framework_cv.md --no-sbert

# Legacy lexical diagnostic; açık must listesi zorunludur
ats-engine score --jd job.txt --cv cv.txt --must "incoterms,customs clearance" --no-sbert
```

CLI exit sözleşmesi: `0=başarılı`, `2=geçersiz girdi`, `3=beklenmeyen iç hata`,
`4=blocking/review gerekli`.

## Python API

```python
from ats_engine import build_report, parse_document

parsed = parse_document("cv.docx")
report = build_report(jd_text, framework_cv_text, cv_text=parsed.text, use_sbert=False)

print(report["match_score"]["evaluation_status"])
print(report["decision_report"]["overall_status"])
print(report["decision_report"]["gates"])
```

## Kanonik sözleşmeler

- Python dataclass/enum sınırı: [`engine/ats_engine/contracts.py`](engine/ats_engine/contracts.py)
- Draft 2020-12 JSON şemaları ve 14 golden örnek: [`schemas/v2/`](schemas/v2/)
- Kabul edilmiş ürün kararı: [`ADR-001`](docs/decisions/ADR-001-evidence-first-v2.md)
- Baseline ve kaynak izi: [`v2 baseline manifesti`](docs/baseline/2026-08-05-v2-baseline.md)
- Doğrulanmamış alanlar: [`Sınırlar ve Sorumlu Kullanım`](docs/limitations.md)

Durum sözleşmeleri:

- Veri: `KNOWN`, `UNKNOWN`, `NOT_COLLECTED`, `NOT_APPLICABLE`, `CONFLICTED`
- Doğrulama: `VERIFIED`, `PARTIAL`, `UNVERIFIED`, `REJECTED`
- Süreç: `PASS`, `FAIL`, `REVIEW`, `WARN`, `ERROR`, `NOT_RUN`

`UNKNOWN`, `NOT_COLLECTED`, `ERROR` ve `NOT_RUN` sayısal fallback ile `PASS` olamaz.

## Mimari

```text
engine/ats_engine/
  contracts.py        versioned public contracts
  ingestion.py        DOCX/PDF/TXT/MD ingestion
  jd_parser.py        explicit requirement extraction
  evidence_bank.py    lexical support + provenance candidates
  scoring.py          legacy alignment diagnostics
  legacy_adapter.py   explicit uncalibrated compatibility boundary
  matching.py         shared explainable term matcher
  configuration.py    versioned gate/evaluation policies
  decision.py         G0-G4 orchestration
  safe_synthesis.py   evidence-bound change sets
  report.py           JSON/Markdown adapter
  cli.py              command boundary

schemas/v2/           closed Draft 2020-12 schemas + golden examples
docs/decisions/       architecture decisions
docs/baseline/        immutable source/code baselines
```

`archive/`, eski prompt/skill dosyaları ve `docs/00–14` metodoloji serisi tarihsel/legacy
bağlamı korur. Kanonik runtime davranışı için yukarıdaki v2 sözleşmeleri ve testler esas alınır.

## Geliştirme ve doğrulama

```bash
pip install -e "engine/[dev]"
make check
make package-check
```

CI şu kapıları çalıştırır: Ruff lint/format, mypy, Python 3.10–3.12 test matrisi,
Draft 2020-12 schema/golden doğrulaması, wheel+sdist build, paket manifest snapshot,
clean-wheel import/CLI smoke ve dependency audit. GitHub Actions bağımlılıkları tam commit
SHA’larına pinlidir.

## Kanıt sınırı

Bu repo ticari ATS tenant’larında veya hiring outcomes üzerinde doğrulanmadı. Mevcut
araştırma iki dil ve sınırlı belge örnekleriyle `PARTIAL — REMAINING SOURCES` statüsündedir.
`parsing_results_long.csv`, çözümlenemeyen başlangıç promptu, ticari tenant ölçümleri ve
prospective outcome çalışması hâlâ eksiktir.

## Sürüm

Current: **2.0.0-alpha.2** — contract/CLI hardening alpha. Production release değildir.
Tarihsel değişiklikler için [`CHANGELOG.md`](CHANGELOG.md) dosyasına bakın.

## License

Proprietary — all rights reserved. See [`LICENSE`](LICENSE).
