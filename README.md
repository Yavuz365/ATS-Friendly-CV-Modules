# ATS-Friendly-CV-Modules

> **Evidence-based, AI-agnostic ATS CV Engine**

Deterministik bir Python motoru ile iş ilanı (JD) ve CV arasındaki uyumu ölçen, kanıt-bazlı CV üretimini yönlendiren açık kaynak araç seti.

[![CI](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions/workflows/test.yml/badge.svg)](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![License](https://img.shields.io/badge/license-Proprietary-red)

---

## 🎯 Ne Yapar?

```
İş İlanı (JD)  ──→  7-Katman Ayrıştırma  ──→  Hibrit ATS Skoru  ──→  Gap Analizi
                         │                          │                       │
Framework CV  ──→  Kanıt Bankası  ──→  Provenans Kontrolü  ──→  Revizyon Döngüsü
```

1. **JD'yi 7 katmana ayırır** — zorunlu terimler, beceriler, niyet, ağırlıklar
2. **Hibrit skor hesaplar** — BM25 + TF-IDF + SBERT + Kapsam − Şişirme cezası
3. **Gap analizi yapar** — kapatılabilir vs kapatılamaz boşluklar
4. **Provenans doğrular** — her CV maddesi Framework CV'ye bağlanır, uydurma engellenir
5. **3-seviyeli skorlama** — Araç kapısı → 8-parça en-iyi → Kategori robustness

## 🏗️ Repo Yapısı

```
ATS-Friendly-CV-Modules/
├── engine/                        ← Python motoru (çekirdek)
│   ├── ats_engine/
│   │   ├── __init__.py            ← Tüm API export'ları (v1.1.0)
│   │   ├── scoring.py             ← Hibrit ATS Match Score
│   │   ├── multilevel.py          ← 3-seviyeli skorlama + LangGate
│   │   ├── cv_parser.py           ← CV bölüm tespiti + parse güvenlik skoru
│   │   ├── jd_parser.py           ← 7-katman JD ayrıştırma
│   │   ├── bm25.py                ← Okapi BM25
│   │   ├── evidence_bank.py       ← Kanıt bankası + provenans
│   │   ├── synthesis.py           ← XYZ/CAR, gap sınıflandırma, anti-stuffing
│   │   ├── lexicons.py            ← Beceri normalizasyonu, eşanlamlı eşleşme
│   │   ├── text.py                ← Tokenizasyon, n-gram, stopwords
│   │   ├── report.py              ← 6-alan çıktı (JSON + Markdown)
│   │   └── cli.py                 ← Komut satırı arayüzü
│   ├── data/                      ← Veri dosyaları
│   │   ├── action_verbs.json      ← 260+ aksiyon fiili (TR/EN, 13 kategori)
│   │   ├── skill_synonyms.json    ← 53 kanonikleme girdisi
│   │   └── stopwords_tr_en.txt    ← Durak kelimeler (TR + EN)
│   ├── tests/test_core.py         ← 19 birim testi
│   ├── examples/                  ← Örnek JD, CV, demo scripti
│   │   ├── run_demo.py
│   │   ├── sample_jd_foreign_trade.txt
│   │   ├── sample_cv.txt
│   │   └── framework_cv.md
│   ├── pyproject.toml             ← pip install -e engine/
│   └── requirements.txt
│
├── docs/                          ← Metodoloji dokümantasyonu
│   ├── 00-mimari.md … 13-grammarly-kapisi.md  (14 ana doküman)
│   ├── architecture/              ← Sistem mimarisi
│   │   ├── system-overview.md
│   │   └── provenance-and-anti-hallucination.md
│   ├── audits/                    ← Denetim raporları
│   │   └── ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md
│   ├── migration/                 ← Eski yapıdan geçiş rehberi
│   │   └── legacy-map.md
│   └── research/                  ← Araştırma notları
│       ├── R1-sistemik-veri-ats-mimarisi.md
│       ├── R2-sentez-once-analiz.md
│       └── R3-seo-ats-sozluk.md
│
├── prompts/                       ← Master Prompt (TR + EN)
│   ├── master-prompt-TR.md        ← Taşınabilir Türkçe prompt
│   ├── master-prompt-EN.md        ← Taşınabilir İngilizce prompt
│   ├── output-fields-template.md  ← 6-alan çıktı şablonu
│   └── adapters/                  ← AI araç adaptörleri
│       ├── chatgpt.md
│       ├── claude.md
│       ├── gemini.md
│       ├── copilot.md
│       ├── deepseek.md
│       └── perplexity.md
│
├── references/                    ← ATS bilgi bankası
│   └── ats-kb/
│       ├── ats-parser-rules.md    ← ATS ayrıştırıcı kuralları
│       ├── jd-taxonomy.md         ← JD taksonomisi (7-katman)
│       └── keyword-ontology.md    ← Keyword sınıflandırma ontolojisi
│
├── schemas/                       ← JSON çıktı şemaları
│   └── scoring_result.schema.json
│
├── skills/                        ← AI skill dosyaları
│   ├── ats-cv-architect/          ← Ana CV motoru skill'i
│   │   ├── SKILL.md
│   │   ├── assets/                ← master-prompt-TR.md, output-fields-template.md
│   │   ├── references/            ← jd-decomposition, scoring, synthesis, workflow
│   │   └── scripts/ats_score.py
│   └── synthesis-analysis-research/  ← Araştırma/analiz skill'i
│       ├── SKILL.md
│       └── references/
│
├── domain-packs/                  ← Alan-özel terim paketleri
│   └── foreign-trade-logistics/
│       ├── keywords_en.json       ← 65 keyword (İngilizce)
│       └── keywords_tr.json       ← 73 keyword (Türkçe)
│
├── templates/                     ← JD/CV şablonları
│   ├── jd-etiketli-sablon.md      ← 3-bölümlü JD Word şablonu
│   └── kanit-bankasi-sablonu.md   ← Framework CV → kanıt bankası
│
├── workflows/                     ← Otomasyon pipeline dokümantasyonu
│   ├── automation/ats-cv-pipeline.md
│   └── notion/veritabani-semasi.md
│
├── archive/                       ← Eski birleşik skill dosyaları (referans)
│   ├── ats-cv-architect_TUM-SKILL-BIRLESIK.md
│   └── synthesis-analysis-research_FULL.md
│
├── .github/workflows/test.yml     ← CI/CD (pytest + smoke test)
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
└── .gitignore
```

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
# Temel kurulum (sıfır harici bağımlılık)
pip install -e engine/

# Geliştirici modu (pytest dahil)
pip install -e "engine/[dev]"

# Semantik benzerlik ile (opsiyonel, SBERT)
pip install -e "engine/[semantic]"
```

### CLI Kullanımı

```bash
# JD-CV tam rapor (6 alan)
python -m ats_engine.cli report \
    --jd jobs/jd.txt \
    --framework cvs/framework_cv.md \
    --format json

# Sadece skor
python -m ats_engine.cli score \
    --jd jobs/jd.txt \
    --cv cvs/cv.txt \
    --must "akreditif,incoterms,GTIP"

# JD ayrıştırma (7 katman)
python -m ats_engine.cli parse --jd jobs/jd.txt

# Framework CV → Kanıt bankası
python -m ats_engine.cli bank --cv cvs/framework_cv.md
```

### Python API

```python
from ats_engine import ats_match_score, parse_jd, build_report

# Tek satırda hibrit skor
result = ats_match_score(jd_text, cv_text, ["akreditif", "incoterms", "GTIP"])
print(f"Skor: %{result['score_percent']}")
print(f"Sonuç: {result['verdict']}")
print(f"Bileşenler: {result['components']}")
print(f"Eksikler: {result['gap']}")

# 7-katman JD ayrıştırma
jd = parse_jd(jd_text)
print(jd["must_have"])      # zorunlu terimler
print(jd["nice_to_have"])   # tercih edilen

# 6-alan tam rapor
rapor = build_report(jd_text, framework_cv_text)

# 3-seviyeli skorlama
from ats_engine import level1_gate, level2_final, level3_category, lang_gate

l1 = level1_gate(jd_text, cv_text, must_terms)        # L1: tek araç kapısı
l2 = level2_final(jd_text, tool_sections, must_terms)  # L2: 8-parça en-iyi
l3 = level3_category(cv_text, jd_texts, must_terms)    # L3: kategori robustness
lg = lang_gate(cv_text, jd_text)                       # dil tutarlılığı kapısı
```

## 📐 Skorlama Formülü

```
H(CV, JD) = LangGate × ParseGate × clamp(α·Lex + β·Sem + γ·Cov − ζ·Stuff, 0, 1)
```

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| α | 0.35 | TF-IDF kosinüs (leksikal benzerlik) |
| β | 0.30 | SBERT kosinüs (semantik benzerlik) |
| γ | 0.35 | Zorunlu terim kapsamı |
| ζ | 0.20 | Şişirme (keyword stuffing) cezası |
| ParseGate | 0–1 | Biçim ayrıştırılabilirliği |
| LangGate | 0–1 | Dil tutarlılığı kapısı |

**Hedef bant:** %75–85 | >%90 = şişirme sinyali | <%50 = ciddi iyileştirme gerekli

SBERT kurulu değilse β otomatik olarak α+γ'ya dağılır (graceful degradation).

## 🔬 3-Seviyeli Skorlama

| Seviye | İşlev | Eşik |
|--------|-------|------|
| L1: Araç Kapısı | Tek AI aracının CV'sini JD'ye karşı skorlar | τ = 0.70 |
| L2: 8-Parça En-İyi | Her bölüm için en yüksek skoru seçer + dikiş cezası | κ = 0.15 |
| L3: Kategori Robustness | Birleşik CV'yi 3+ ilana test eder | σ ≤ 0.10 |

## 🛡️ Araç-Bağımsızlık İlkesi

Bu repo **hiçbir AI aracına bağımlı değildir**:

- Motor (`engine/`) saf Python — herhangi bir LLM'den bağımsız çalışır
- Master Prompt herhangi bir LLM'e kopyalanabilir (ChatGPT, Claude, Gemini, Copilot, vb.)
- AI araç adaptörleri (`prompts/adapters/`) her LLM'in güçlü yanına göre optimize eder
- Otomasyon herhangi bir platformla entegre edilebilir (n8n, Make, Zapier vb.)

## 📚 Dokümantasyon

### Ana Dokümanlar (docs/)

| Dosya | Konu |
|-------|------|
| [00-mimari.md](docs/00-mimari.md) | Genel mimari |
| [01-metodoloji.md](docs/01-metodoloji.md) | Diyalektik metodoloji |
| [02-jd-decomposition.md](docs/02-jd-decomposition.md) | 7-katman JD ayrıştırma |
| [03-skorlama-matematigi.md](docs/03-skorlama-matematigi.md) | Hibrit skor formülleri |
| [04-sentez-kurallari.md](docs/04-sentez-kurallari.md) | XYZ/CAR sentez kuralları |
| [05-grammarly-entegrasyonu.md](docs/05-grammarly-entegrasyonu.md) | Grammarly entegrasyonu |
| [06-denetim-ve-duzeltmeler.md](docs/06-denetim-ve-duzeltmeler.md) | Denetim düzeltmeleri |
| [07-workflow-multitool.md](docs/07-workflow-multitool.md) | Çok-araçlı iş akışı |
| [08-kategorizasyon-taksonomisi.md](docs/08-kategorizasyon-taksonomisi.md) | İlan kategorizasyon sistemi |
| [09-orkestrasyon-katmanlari.md](docs/09-orkestrasyon-katmanlari.md) | Pipeline orkestrasyon |
| [10-sekiz-parca-skorlama.md](docs/10-sekiz-parca-skorlama.md) | 8-parça skorlama + QA |
| [11-uc-seviyeli-skorlama.md](docs/11-uc-seviyeli-skorlama.md) | 3-seviyeli skor matematiği |
| [12-dil-tutarliligi.md](docs/12-dil-tutarliligi.md) | Dil tutarlılığı + TR morfoloji |
| [13-grammarly-kapisi.md](docs/13-grammarly-kapisi.md) | Grammarly kapısı |

### Ek Dokümanlar

| Klasör | İçerik |
|--------|--------|
| [docs/architecture/](docs/architecture/) | Sistem mimarisi + provenans/anti-halüsinasyon |
| [docs/audits/](docs/audits/) | Kurulum bulguları ve denetim raporu |
| [docs/migration/](docs/migration/) | Eski yapıdan geçiş rehberi |
| [docs/research/](docs/research/) | ATS mimarisi, sentez analizi, SEO sözlük araştırmaları |

### Bilgi Bankası (references/ats-kb/)

| Dosya | İçerik |
|-------|--------|
| [ats-parser-rules.md](references/ats-kb/ats-parser-rules.md) | ATS parser kuralları, format cezaları |
| [jd-taxonomy.md](references/ats-kb/jd-taxonomy.md) | JD 7-katman modeli detayları |
| [keyword-ontology.md](references/ats-kb/keyword-ontology.md) | Keyword sınıflandırma ve eşanlamlı genişletme |

## 🧪 Testler

```bash
# Testleri çalıştır
cd engine && pip install -e ".[dev]" && pytest tests/ -v
```

19 test: clamp, gate, H1 durma koşulu, gap sınıflandırma, 6-alan çıktı, BM25, anti-stuffing ve daha fazlası.

CI/CD: Her push'ta otomatik olarak Python 3.10, 3.11, 3.12 üzerinde test çalışır.

## ⚖️ Etik İlkeler

- ❌ Deneyim, metrik veya sertifika **UYDURULMAZ**
- ✅ Her CV maddesi Framework CV'ye dayalıdır (provenans)
- ✅ Keyword stuffing tespit edilir ve cezalandırılır (ζ = 0.20)
- ✅ %75–85 hedef bandı — aşırı optimizasyon uyarılır
- ✅ LangGate dil tutarlılığını kontrol eder

## 📦 Versiyon

Güncel: **v1.1.0** — [CHANGELOG.md](CHANGELOG.md)

## 📄 Lisans

Proprietary — tüm hakları saklıdır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
