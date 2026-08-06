# 04 — Sentez Kuralları (SENTEZ)

> **Legacy metodoloji (v1.x):** v2 sentez değişiklikleri evidence ID, allowlist ve insan onayı gerektirir.

Tam mekanik: `skills/ats-cv-architect/references/synthesis-rules.md`. Kod: `engine/ats_engine/synthesis.py`.

## 1. Kümeleme
Becerileri anlamlı kümelere topla (LSI/ontoloji ile, şişirmeden). `cluster_skills()` + `data/skill_synonyms.json`.

## 2. XYZ / CAR cümle mimarisi
> "[Z yöntemiyle] yaparak, [Y ölçüsüyle ölçülen] [X sonucunu] başardım."
Her cümlede ≥1 sayı, başında güçlü aktif fiil. Örnek (dış ticaret):
> "Gümrük süreçlerinde YYS/AEO standartlarını optimize ederek ithalat gümrükleme sürelerini 2 gün kısalttım ve navlun maliyetinde %15 tasarruf sağladım."

## 3. Provenans (dürüstlük omurgası) — MUTLAK
Çıktı CV'sindeki **her madde** kanıt bankasındaki bir Input-ID'ye bağlanmalı. Bağlanamayan madde **çıkar**. `evidence_bank.provenance_check()`.

## 4. Anti-stuffing
Coverage > density. Önemli terim 2–3 kez, farklı bölümlerde (Beceriler'de iddia, Deneyim'de kanıt). Yoğunluk eşiği aşılırsa uyarı. `anti_stuffing_report()`.

## 5. Revizyon döngüsü — durma kuralı (H1 düzeltmesi) ⚠
Yaygın hata: `gap = boş` koşulunu sonlandırma şartı yapmak. Dürüst CV'de adayda olmayan zorunlu beceriler hep kalır → sonsuz döngü.
**Doğru kural (kodda `stopping_condition`):**
```
DUR  ⟺  (skor ≥ hedef)  VEYA  (kapatılabilir gap kalmadı)
```
Yalnızca kapatılabilir gap üzerinde dönülür; kapatılamaz gap dürüstçe kabul edilir.

## 6. Parse güvenliği
Tek sütun, standart başlıklar, tablo/grafik/metin-kutusu yok, iletişim ana gövdede, .docx tercih, akronim hem açık hem kısa ("Dış Ticaret (Foreign Trade)").
