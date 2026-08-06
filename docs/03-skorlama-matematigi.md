# 03 — Skorlama Matematiği (denetim-düzeltmeli)

> **Legacy diagnostic (v1.x):** Bu eşik ve formüller ticari ATS geçişi veya hiring outcome değildir.
> v2’de boş açık gereksinim `NOT_EVALUATED`; kanonik karar `DecisionReport` içindedir.

Tam türetim: `skills/ats-cv-architect/references/scoring-formulas.md`. Çalışan kod: `engine/ats_engine/scoring.py` + `bm25.py`.

## Bileşenler ([0,1]'e normalize)
- **Lex** = BM25/TF-IDF kosinüs — TÜM JD terimleri üzerinden dağılımsal benzerlik.
- **Sem** = `max(0, cos(embed(CV), embed(JD)))` — SBERT cümle gömme (eşanlamlı/parafraz). Kuruluysa.
- **Cov** = zorunlu terimlerin ağırlıklı, **eşanlamlı-duyarlı** kapsamı (`w_j = modality × konum`).
- **Stuff** = yoğunluk anomalisi cezası (kelime doldurma).
- **Parse_gate** = biçim okunabilirliği (JD'den bağımsız) — **çarpan/kapı**.

## Birleşik skor (düzeltilmiş)
```
RAW   = α·Lex + β·Sem + γ·Cov − ζ·Stuff
Score = clamp( Parse_gate × RAW , 0 , 1 )
```
Öneri: `α=0.35, β=0.30, γ=0.35`, `ζ=0.20`, `Parse_gate ∈ [0.6, 1.0]`.

## Audit düzeltmeleri (neden bu biçim?)
- **M1 — clamp(0,1):** `−ζ·Stuff` skoru negatife itebiliyordu → alt sınır kıskaçlandı.
- **M2 — Parse çarpan, toplam değil:** Parse "bu ilana uyum" değil "genel okunabilirlik"tir. Toplamak iki ayrı şeyi karıştırır; çarpan yapınca bozuk biçim skoru orantılı çökertir (tablo/2-sütun → ~×0.6).
- **M3 — Lex/Cov bağımlılığı:** ikisi de "terim var mı"yı ödüllendirir; Lex'i *tüm* terimler, Cov'u *yalnızca zorunlu* terimler olarak ayır, ağırlıkları buna göre düşür.
- **SBERT yoksa:** β payı α+γ'ya orantılı dağıtılır (motor bunu otomatik yapar), skor göreli okunur.

## P/R/F1 + gap
`P = |C∩M|/|C|` (ilgililik), `R = |C∩M|/|M|` (zorunlu kapsam), `F1 = 2PR/(P+R)`.
**Gap ikiye ayrılır** (audit M-D): *kapatılabilir* (kanıt bankasında var, CV'ye yansımamış) vs *kapatılamaz* (adayda yok).

## Eşik yorumu
Evrensel hizalanma bandı yoktur. Sayısal eşik yalnız kaynak, tarih, dil, domain ve
comparator sürümü bağlı bir `EvaluationProfile` içinde tanısal deney amacıyla
kullanılabilir; ATS geçişi, mülakat veya işe-alım sonucu değildir.

## Dürüst statü
Skor, bu repository’nin kendi lexical/semantic **araştırma tanısıdır**. Workday,
Greenhouse, iCIMS veya başka bir ticari ATS’nin iç formülünü yaklaşık hesapladığı iddia
edilmez. Evrensel ATS puanı, mülakat veya hiring outcome olasılığı değildir.
