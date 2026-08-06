# docs/12 — Dil Tutarlılığı + Türkçe Morfoloji

> **Legacy diagnostic:** Dil sinyali G3 tanısıdır; tek başına product PASS üretmez.

> Tek-dilli CV zorunluluğu, dil tespiti, lemma-bazlı eşleşme ve Türkçe'ye özgü işlemler.

## 1. Neden Dil Tutarlılığı Kritik?

ATS sistemleri CV'yi tek-dilli metin olarak parse eder. Karışık dil:
- Keyword matching'i bozar ("ihracat" ve "export" ayrı terimler sayılır)
- Parser dil modeli seçemez → her iki dilde de düşük skor
- Profesyonellik algısını zedeler

## 2. LangGate Mekanizması

```python
from ats_engine.multilevel import lang_gate

# JD İngilizce, CV İngilizce → LangGate ≈ 1.0
lg = lang_gate(cv_en, jd_en)

# JD İngilizce, CV Türkçe-karışık → LangGate < 1.0 → skor cezası
lg = lang_gate(cv_mixed, jd_en)
```

### Algoritma

1. `detect_language(JD)` → baskın dili tespit et (`"tr"` veya `"en"`)
2. `language_purity(CV, jd_lang)` → CV'nin o dile sadakat oranı `[0, 1]`
3. `LangGate = min(1.0, purity / p₀)` (`p₀ = 0.85`)

### Dil Tespiti Heuristik

- **Türkçe sinyalleri:** `çÇğĞıİöÖşŞüÜ` karakterleri + Türkçe durak kelimeler
- **İngilizce sinyalleri:** `the, and, of, in, to, for, with, ...` kelime frekansı
- TR karakter sayısı × 2 + TR kelime sayısı > EN kelime sayısı → Türkçe

## 3. Türkçe Morfoloji Sorunu

Türkçe sonekli (eklemeli) bir dil. Aynı kavram farklı biçimlerde görünür:

| JD terimi | CV'deki olası biçimler |
|-----------|------------------------|
| ihracat | ihracatı, ihracatta, ihracatçı, ihracatla |
| gümrükleme | gümrüklemesi, gümrüklemede, gümrüklemeyi |
| lojistik | lojistiği, lojistikte, lojistikçi |
| tedarik | tedariği, tedarikte, tedarikçi |

### Mevcut Çözüm: Eşanlamlı Normalizasyon

`lexicons.normalize_skill()` ve `skill_synonyms.json` ile:

```json
{
    "canonical": "ihracat",
    "variants": ["ihracatı", "ihracatta", "ihracatçı", "export", "exporting"]
}
```

### Gelecek: Lemmatizer Entegrasyonu

`pyproject.toml` → `[project.optional-dependencies]` → `turkish = ["zemberek-python"]`

```python
# Gelecekte:
from zemberek import TurkishMorphology
morphology = TurkishMorphology.create_with_defaults()
result = morphology.analyze("ihracatçılarımızdan")
# → kök: "ihracat"
```

## 4. Stopwords

`engine/data/stopwords_tr_en.txt` dosyası 103 durak kelime içerir (TR + EN).

**Kullanım alanları:**
- BM25 / TF-IDF hesaplamalarında gürültü eleme
- Coverage hesabında gereksiz eşleşme önleme
- Stuffing penalty'de durak kelimeler sayılmaz

## 5. Pratik Kurallar

| Kural | Açıklama |
|-------|----------|
| Tek-dilli CV | JD dili = CV dili. Karışma yasak. |
| Teknik terimler | "SAP", "ERP", "KPI" gibi evrensel kısaltmalar ceza almaz |
| Şirket adları | İngilizce şirket adı Türkçe CV'de kabul edilir |
| Sertifika adları | "CILT", "Six Sigma" gibi uluslararası adlar ceza almaz |
| İş unvanları | JD dilinde yazılmalı ("Supply Chain Manager" vs "Tedarik Zinciri Müdürü") |
