# 03 — Skorlama Matematiği (denetim-düzeltmeli)

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
%75–85 hedef (mülakata hazır) · >%90 şişirme sinyali · <%50 ciddi iyileştirme.

## Dürüst statü
Skor, tescilli ATS iç formüllerinin (Workday/Greenhouse/iCIMS) **yaklaşıklamasıdır** (proxy) — mutlak gerçek değil, göreli pusula.
