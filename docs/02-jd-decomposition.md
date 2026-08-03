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

## Bilinen sınır — OR-grup gereksinimler (GAP-D, v1.5.1)

`jd_parser.py`, "İşletme **veya** İktisat mezunu olmak" gibi **alternatif-grup**
(OR-grup) gereksinimleri **modellemiyor**. Motorun must-have çıkarımı bilinen bir
beceri/araç sözlüğüne (lexicon) dayandığı için, serbest metindeki bu tür bir eğitim
gereksinimi bir terim olarak hiç tanınmıyor ve sessizce `must_have` listesine hiç
girmiyor (yanlış/kısmi ayrıştırma değil, **tamamen atlanıyor** — `engine/tests/test_core.py::test_or_group_education_requirement_is_currently_not_extracted`
bu davranışı kilitler).

Bu bilinçli bir v1.5.1 kararıdır (kanonik ID: GAP-D → `JOB-002` eki): OR-grup
matematiği (requirement modality için "alternative-group requirements") v2.0
contract-first `JobRequirement` şemasının parçası olarak ele alınacak, v1.5.1'de
uygulanmayacak. Bu bölümdeki test, ileride bu davranış (kasıtsızca) değişirse
regresyonu yakalamak için var — davranışı "doğru" ilan etmez.
