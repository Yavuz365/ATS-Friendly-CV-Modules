# 02 — JD Ayrıştırma: 7 Katmanlı Şema (ANALİZ)

Her iş ilanı düz metin değil, 7 semantik katmana bozunur. (`engine/ats_engine/jd_parser.py` bunu deterministik yapar.)

| # | Katman | İçerik | Ağırlık |
|---|---|---|---|
| 1 | **Kimlik** | unvan, kıdem, sektör, lokasyon, çalışma biçimi, dil | — |
| 2 | **Zorunlu (must-have)** | sert beceri/araç, sertifika, deneyim yılı, eğitim, yasal/knockout | **1.0** |
| 3 | **Tercih (nice-to-have)** | "preferred / artı değer / avantaj" | **0.3** |
| 4 | **Sorumluluk/eylem** | "yönetir, koordine eder, denetler, optimize eder, raporlar" → XYZ hammaddesi | — |
| 5 | **Niyet/alt-metin** | "Bu rol esasen ___ arıyor" (ör. memur değil **denetçi**) | — |
| 6 | **Semantik/LSI** | her terimin eşanlamlı/akraba kümesi (eşleşmeyi *anlamak* için) | — |
| 7 | **Ağırlık metası** | modality (1.0 / 0.7 güçlü-ima / 0.3) + konum (ilk ~150 kelime ağır) + sıklık | — |

## Modality 3 kademe (audit M4)
İkili {1.0, 0.3} fazla kabaydı; etiketsiz ama tekrarlı/merkezî terimler kaçıyordu. Çözüm: **1.0** (açık zorunlu) / **0.7** (güçlü ima) / **0.3** (tercih) + sıklık katkısı.

## Konum ağırlığı
İlk ~150 kelimede veya başlık/özet bölümünde geçen terim logaritmik olarak daha değerli. Motorda `positional_weight` (örn. ×1.3) olarak taşınır.
