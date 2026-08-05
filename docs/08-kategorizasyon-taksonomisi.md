# docs/08 — İlan Kategorizasyon Taksonomisi

> **Legacy taksonomi:** Gövde terimleri açık gereksinim sayılmaz; v2 durum sözleşmesi önceliklidir.

> İş ilanlarını standart bir etiketleme sistemiyle sınıflandırma kuralları.

## 1. Etiket Yapısı

```
{sıra}.{dil}.{alan_kodu}
```

| Alan    | Dil | Kod | Tam Etiket |
|---------|-----|-----|------------|
| Dış Ticaret | EN | FTC | `1.EN.FTC` |
| Dış Ticaret | TR | DTK | `1.TR.DTK` |
| Lojistik    | EN | LGC | `2.EN.LGC` |
| Lojistik    | TR | LTK | `2.TR.LTK` |
| Tedarik Zinciri | EN | SCM | `3.EN.SCM` |
| Tedarik Zinciri | TR | TZY | `3.TR.TZY` |
| Üretim / Planlama | EN | MFG | `4.EN.MFG` |
| Üretim / Planlama | TR | URT | `4.TR.URT` |

## 2. Alt-kategori (Dosya Gruplama)

Aynı kategorideki ilanlar `/1` → `/5` alt-etiketle numaralandırılır:

```
1.EN.FTC-1/5   ← 5 ilandan ilki
1.EN.FTC-2/5   ← ikincisi
```

**Kural:** Bir klasör **en az 3** ilana ulaştığında sentetik/birleştirilmiş ilan oluşturulur (`level3_category()`).

## 3. Dil-Etiket Bağlantısı

Etiket dili (`EN` vs `TR`) CV ve JD'nin dilini belirler:
- `*.EN.*` → İngilizce JD + İngilizce CV beklenir
- `*.TR.*` → Türkçe JD + Türkçe CV beklenir
- `LangGate()` bu etiket bilgisini kullanarak dil saflık kontrolü yapar

## 4. Motor Entegrasyonu

```python
from ats_engine.multilevel import level3_category

# Aynı kategorideki 3+ ilan
jd_texts = [jd1_text, jd2_text, jd3_text]
result = level3_category(cv_text, jd_texts, must_terms=common_terms)
# result["robust"] → True/False (σ ≤ 0.10 → dayanıklı)
```

## 5. Klasör Organizasyonu (Drive/OneDrive)

```
jobs/
├── 1.EN.FTC/
│   ├── 1.EN.FTC-1_Company_Title.docx
│   ├── 1.EN.FTC-2_Company_Title.docx
│   └── ...
├── 1.TR.DTK/
├── 2.EN.LGC/
└── ...
```

Her `.docx` dosyası 3 bölüm içerir:
1. Ham ilan metni
2. AI araçları sentez & analiz çıktısı
3. Master Prompt çıktısı
