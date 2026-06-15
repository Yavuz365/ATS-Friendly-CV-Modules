# Decision Engine — 5-Gate Mimarisi

> **Kaynak:** Viktor Hybrid Revizyon v2.0 (Bölüm V.11)
> **Durum:** Tasarım belgesi — P1 aşamasında uygulanacak

## Genel Bakış

ATS-CV pipeline'ın son aşamasında her CV çıktısını 5 kapıdan geçiren
kalite kontrol motoru. Herhangi bir kapı FAIL verirse pipeline durur ve
kullanıcıya neden + aksiyon bildirilir.

## 5 Gate

```
Gate 1: INPUT QUALITY
  ├─ ParseGate → CV/JD okunabilir mi? (parse_safety_score ≥ 0.7)
  ├─ Format hygiene → karakter/bullet sağlam? (full_hygiene_check)
  └─ FAIL → "CV/JD formatı düzeltilmeli"
         ↓ PASS

Gate 2: EVIDENCE
  ├─ Evidence Recall ≥ 70%? (evidence_recall)
  ├─ Her CV maddesi evidence ID'ye bağlı mı? (provenance_check)
  └─ FAIL → "Kanıt eksik, Framework CV'ye dön"
         ↓ PASS

Gate 3: LANGUAGE & LOCALE
  ├─ JD dili = CV dili? (detect_locale + locale_mismatches)
  ├─ TR/EN karışmış mı? (lang_gate + language_purity)
  ├─ Acronym bozulması var mı? (tr_lower acronym-safe kontrol)
  └─ FAIL → "Dil tutarlılığı düzeltilmeli"
         ↓ PASS

Gate 4: SCORE
  ├─ Total score 75-85 bandında mı?
  ├─ 90+ → overfit audit (anti_stuffing_report)
  ├─ <70 → ciddi eksik (gap_analysis)
  ├─ Cliché ratio < 15%? (detect_cliches)
  ├─ Calibration delta açıklanabilir mi? (suggest_weight_adjustment)
  └─ FAIL → "Skor bandı dışında"
         ↓ PASS

Gate 5: HUMAN APPROVAL
  ├─ Gap analizi sunuldu mu?
  ├─ İnsan "evet" dedi mi?
  └─ FAIL → "İnsan onayı bekleniyor"
         ↓ APPROVED

PRODUCTION EXPORT
  ├─ Final CV → DOCX/PDF
  ├─ Provenance table
  └─ Jobscan/Grammarly checklist
```

## Mevcut Modül Eşlemesi

| Gate | Mevcut Modül(ler) | Durum |
|------|-------------------|-------|
| Gate 1 | cv_parser, format_metadata_hygiene | ✅ Modüller var, P0.3+P0.4 ile wired |
| Gate 2 | evidence_bank, completeness_guard | ✅ Modüller var, P0.4 ile wired |
| Gate 3 | locale_consistency, multilevel (lang_gate) | ✅ Modüller var, P0.4 ile wired |
| Gate 4 | scoring, cliche_tone, calibration | ✅ Modüller var, P0.4 ile wired |
| Gate 5 | — (CLI human checkpoint) | ⚠️ P1 — approval hooks gerekli |

## Notlar

- Mevcut `build_report()` tüm QA modüllerini çalıştırıp `qa_checks` alanına yazar (v1.5.0).
- Decision Engine bu sonuçları gate mantığıyla değerlendiren bir orkestratör katmanı olacak (P1).
- Her gate'in PASS/FAIL sonucu + neden + aksiyon metni üretmesi gerekiyor.
