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

## Field-level evaluation (ING-005)

Document-level status alone is not enough. Field-level evaluation records whether
specific structural and content fields were recovered:

| Field | Measured on | Expected signal |
|-------|-------------|-----------------|
| `full_text` | all fixtures | required text fragments present |
| `table_cells` | DOCX-COMPLEX-001 | table_count ≥ 1 |
| `header_text` | DOCX-COMPLEX-001 | header_part_count ≥ 1 |
| `text_box_text` | DOCX-COMPLEX-001 | text_box_count ≥ 1 |
| `page_evidence` | PDF-TEXT-001 | at least one page with text layer |
| `ocr_required` | PDF-SCAN-001 | ERROR without explicit OCR adapter |

A fixture may be document-level `PASS` only when every required field for that
fixture also passes. Missing structural fields force `REVIEW` or `ERROR`; they
are never silently ignored.

Field-level results are stored alongside the document label in evaluation runs
(see `labels.json` and future evaluation cards). This section is the dataset
contract for ING-005; full metric tables and inter-annotator notes remain future
work.

## Lisans ve gizlilik

Tamamen sentetik içerik. İnsan adı, iletişim bilgisi, işveren veya gerçek başvuru verisi içermez. Corpus yalnız test/evaluation amacıyla kullanılabilir.

## Bilinen sınırlar

Bu corpus ticari ATS davranışını, OCR doğruluğunu, platform sıralamasını veya işe alım sonucunu ölçmez. PDF fixture'ları tek sayfalıdır; çok sütunlu ve karmaşık reading-order değerlendirmesi ayrı dataset sürümü gerektirir. Field-level coverage is currently limited to the structural features listed above.
