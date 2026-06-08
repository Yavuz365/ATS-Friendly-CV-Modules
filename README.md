# ATS-Friendly-CV-Modules

> **Evidence-based, AI-agnostic ATS CV Engine**

Deterministik bir Python motoru ile iş ilanı (JD) ve CV arasındaki uyumu ölçen, kanıt-bazlı CV üretimini yönlendiren açık kaynak araç seti.

[![CI](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions/workflows/test.yml/badge.svg)](https://github.com/Yavuz365/ATS-Friendly-CV-Modules/actions)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
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
├── engine/                    ← Python motoru (çekirdek)
│   ├── ats_engine/
│   │   ├── scoring.py         ← Hibrit ATS Match Score
│   │   ├── multilevel.py      ← 3-seviyeli skorlama + LangGate
│   │   ├── cv_parser.py       ← CV bölüm tespiti + parse güvenlik skoru
│   │   ├── jd_parser.py       ← 7-katman JD ayrıştırma
│   │   ├── bm25.py            ← Okapi BM25
│   │   ├── evidence_bank.py   ← Kanıt bankası + provenans
│   │   ├── synthesis.py       ← XYZ/CAR, gap sınıflandırma, anti-stuffing
│   │   ├── lexicons.py        ← Beceri normalizasyonu, eşanlamlı eşleşme
│   │   ├── text.py            ← Tokenizasyon, n-gram, stopwords
│   │   ├── report.py          ← 6-alan çıktı (JSON + Markdown)
│   │   └── cli.py             ← Komut satırı arayüzü
│   ├── data/                  ← Veri dosyaları
│   │   ├── action_verbs.json  ← 320 aksiyon fiili (TR/EN, 3 seviye)
│   │   ├── skill_synonyms.json← 52 kanonikleme girdisi
│   │   └── stopwords_tr_en.txt← Durak kelimeler (TR + EN)
│   ├── tests/                 ← 19+ birim testi
│   ├── examples/              ← Örnek JD, CV, demo scripti
│   └── pyproject.toml         ← pip install ats-engine
├── docs/                      ← Metodoloji dokümantasyonu (00-13)
├── prompts/                   ← Master Prompt (TR + EN)
│   └── adapters/              ← AI araç adaptörleri (ChatGPT, Claude, vb.)
├── schemas/                   ← JSON çıktı şemaları
├── skills/                    ← AI skill dosyaları
├── templates/                 ← JD/CV şablonları
├── domain-packs/              ← Alan-özel terim paketleri
│   └── foreign-trade-logistics/
├── workflows/                 ← Otomasyon pipeline dokümantasyonu
└── .github/workflows/         ← CI/CD (pytest + smoke test)
```

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
# Temel kurulum (sıfır bağımlılık)
pip install -e engine/

# Semantik benzerlik ile (opsiyonel)
pip install -e "engine/[semantic]"
```

### CLI Kullanımı

```bash
# JD-CV uyum raporu
python -m ats_engine.cli report \
    --jd jobs/foreign_trade_analyst.txt \
    --cv cvs/master_cv.md \
    --format json

# Sadece skor
python -m ats_engine.cli score \
    --jd jobs/jd.txt --cv cvs/cv.txt --must "akreditif,incoterms,GTIP"

# JD ayrıştırma
python -m ats_engine.cli parse --jd jobs/jd.txt

# Kanıt bankası
python -m ats_engine.cli bank --cv cvs/framework_cv.md
```

### Python API

```python
from ats_engine import ats_match_score, parse_jd, build_report

# Tek satırda skor
result = ats_match_score(jd_text, cv_text, ["akreditif", "incoterms", "GTIP"])
print(f"Skor: %{result['score_percent']}")
print(f"Sonuç: {result['verdict']}")
print(f"Eksikler: {result['gap']}")

# 3-seviyeli skorlama
from ats_engine import level1_gate, level2_final, level3_category, lang_gate

l1 = level1_gate(jd_text, cv_text, must_terms)
lg = lang_gate(cv_text, jd_text)
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
| ParseGate | 0-1 | Biçim ayrıştırılabilirliği |
| LangGate | 0-1 | Dil tutarlılığı kapısı |

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

- Motor (engine/) saf Python — herhangi bir LLM'den bağımsız çalışır
- Master Prompt herhangi bir LLM'e kopyalanabilir (ChatGPT, Claude, Gemini, Copilot, vb.)
- AI araç adaptörleri (`prompts/adapters/`) her LLM'in güçlü yanına göre optimize eder
- Otomasyon herhangi bir platformla entegre edilebilir

## 📚 Dokümantasyon

| Dosya | Konu |
|-------|------|
| [docs/00-mimari.md](docs/00-mimari.md) | Genel mimari |
| [docs/01-metodoloji.md](docs/01-metodoloji.md) | Diyalektik metodoloji |
| [docs/02-jd-decomposition.md](docs/02-jd-decomposition.md) | 7-katman JD ayrıştırma |
| [docs/03-skorlama-matematigi.md](docs/03-skorlama-matematigi.md) | Hibrit skor formülleri |
| [docs/04-sentez-kurallari.md](docs/04-sentez-kurallari.md) | XYZ/CAR sentez kuralları |
| [docs/05-grammarly-entegrasyonu.md](docs/05-grammarly-entegrasyonu.md) | Grammarly entegrasyonu |
| [docs/06-denetim-ve-duzeltmeler.md](docs/06-denetim-ve-duzeltmeler.md) | Denetim düzeltmeleri |
| [docs/08-kategorizasyon-taksonomisi.md](docs/08-kategorizasyon-taksonomisi.md) | İlan kategorizasyon sistemi |
| [docs/09-orkestrasyon-katmanlari.md](docs/09-orkestrasyon-katmanlari.md) | Pipeline orkestrasyon |
| [docs/10-sekiz-parca-skorlama.md](docs/10-sekiz-parca-skorlama.md) | 8-parça skorlama + QA |
| [docs/11-uc-seviyeli-skorlama.md](docs/11-uc-seviyeli-skorlama.md) | 3-seviyeli skor matematiği |
| [docs/12-dil-tutarliligi.md](docs/12-dil-tutarliligi.md) | Dil tutarlılığı + TR morfoloji |
| [docs/13-grammarly-kapisi.md](docs/13-grammarly-kapisi.md) | Grammarly kapısı |

## 🧪 Testler

```bash
cd engine && pytest tests/ -v
```

19+ test: clamp, gate, H1 durma koşulu, gap sınıflandırma, 6-alan çıktı, ve daha fazlası.

## ⚖️ Etik İlkeler

- ❌ Deneyim, metrik veya sertifika UYDURULMAZ
- ✅ Her CV maddesi Framework CV'ye dayalıdır (provenans)
- ✅ Keyword stuffing tespit edilir ve cezalandırılır
- ✅ %75-85 hedef bandı — aşırı optimizasyon uyarılır

## 📄 Lisans

Proprietary — tüm hakları saklıdır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
