# ATS Keyword Ontolojisi

> **Kanonik konum:** `references/ats-kb/keyword-ontology.md`  
> Bu dosya, ATS CV sisteminin keyword sınıflandırma ve eşanlamlı genişletme kurallarını tanımlar.

---

## 1. Modality Seviyeleri

| Seviye | Ağırlık | Tanım | Sinyal |
|--------|---------|-------|--------|
| **Zorunlu (must-have)** | 1.0 | Açıkça "required / şart / aranan" | "must have", "required", "şart" etiketi |
| **Güçlü ima** | 0.7 | Etiketsiz ama ≥2 tekrar veya sorumlulukta merkezi | Tekrar sıklığı, pozisyon ağırlığı |
| **Tercih (nice-to-have)** | 0.3 | "preferred / plus / avantaj" | "preferred", "plus", "avantaj" etiketi |

---

## 2. Konum Ağırlığı

| Bölge | Çarpan |
|-------|--------|
| İlk ~150 kelime / "Aranan Nitelikler" başlangıcı | ×1.2–1.5 |
| Orta gövde | ×1.0 |
| "Artı olarak / Tercih" kuyruğu | ×0.8 |

**İlk 150 kelimede geçen terimler daha ağır ATS puanı taşır.**

---

## 3. Semantik Kümeleme (Örnek Ontolojiler)

### Dış Ticaret / Lojistik
```
Incoterms ↔ teslim koşulları ↔ delivery terms
akreditif ↔ letter of credit ↔ L/C
gümrükleme ↔ customs clearance ↔ gümrük beyannamesi
GTIP ↔ HS kodu ↔ tariff classification
landed cost ↔ toplam ithalat maliyeti
tedarik zinciri ↔ supply chain ↔ lojistik yönetimi
```

### Veri Analizi
```
veri analizi ↔ data analysis ↔ analitik
Excel ↔ spreadsheet ↔ tablo analizi
Python ↔ pandas ↔ veri işleme
raporlama ↔ dashboard ↔ BI ↔ görselleştirme
KPI ↔ performans göstergesi ↔ metrik
```

### Finans / Muhasebe
```
bütçe ↔ budget ↔ finansal planlama
maliyet analizi ↔ cost analysis ↔ gider yönetimi
P&L ↔ kar-zarar ↔ gelir tablosu
```

---

## 4. Genişletme Kuralları

1. Genişletilmiş terimler **yalnızca adayda kanıtı varsa** CV'ye girer.
2. Semantik genişletme, **JD eşleşmesini anlamak** için; CV doldurmak için değil.
3. LSI/eşanlamlı öneri → `[SENTEZ-ÖNERİ]` etiketine; asla `[JD-ORİJİNAL]` etiketine.

---

## 5. Keyword Yoğunluğu Kuralı

| Durum | Açıklama |
|-------|----------|
| Normal | Birincil terim %1–3 (15–25 ilgili terim, metne dağıtılmış) |
| Uyarı | Tek terim tekrarı %5+ → şişirme riski |
| Hedef | Coverage (kapsam) + proof (kanıt) > density (yoğunluk) |

---

## 6. Role-Family Grupları (Örnek)

| Fonksiyon | Zorunlu Terim Kümesi |
|-----------|---------------------|
| Dış Ticaret Uzmanı | Incoterms, akreditif, gümrük, GTIP, ithalat/ihracat |
| Veri Analisti | SQL/Python/Excel, dashboard, KPI, raporlama |
| Proje Yöneticisi | Proje planı, risk yönetimi, paydaş, bütçe |
| İnsan Kaynakları | İşe alım, yetenek yönetimi, IK süreçleri |

Yeni sektör/fonksiyon için bu tabloyu genişlet ve `references/ats-kb/jd-taxonomy.md` ile senkron tut.
