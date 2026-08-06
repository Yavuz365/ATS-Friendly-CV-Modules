# ATS Binary Gold Corpus v1.0.0

## Amaç

DOCX/PDF ingestion davranışını gerçek ikili dosyalar üzerinde, kişisel veri kullanmadan doğrulayan sürümlü değerlendirme corpus'u.

## Kapsam

- `DOCX-COMPLEX-001`: paragraf, tablo, header ve textbox içeren OOXML belge.
- `PDF-TEXT-001`: seçilebilir metin içeren tek sayfalı PDF.
- `PDF-SCAN-001`: metinsiz/scan-benzeri PDF; OCR zorunluluğu beklenir.

Binary dosyalar `generate_corpus.py` ile deterministik test çalışma alanında üretilir. Kaynak generator, manifest ve beklenen JSON çıktıları repository'de sürümlenir. Böylece repoya gerçek kişisel CV veya yeniden tanımlanabilir veri eklenmez.

## Etiket politikası

Her fixture için tek bir `expected_status`, `extraction_method`, zorunlu metin parçaları ve yapısal beklentiler vardır. `PASS`, `REVIEW` ve `ERROR` birbirine dönüştürülemez. Metinsiz PDF, OCR adaptörü verilmeden başarı olarak etiketlenemez.

## Lisans ve gizlilik

Tamamen sentetik içerik. İnsan adı, iletişim bilgisi, işveren veya gerçek başvuru verisi içermez. Corpus yalnız test/evaluation amacıyla kullanılabilir.

## Bilinen sınırlar

Bu corpus ticari ATS davranışını, OCR doğruluğunu, platform sıralamasını veya işe alım sonucunu ölçmez. PDF fixture'ları tek sayfalıdır; çok sütunlu ve karmaşık reading-order değerlendirmesi ayrı dataset sürümü gerektirir.
