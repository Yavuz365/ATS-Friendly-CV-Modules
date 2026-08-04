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

> **Düzeltme (2026-08-05):** Aşağıdaki tablo önceden Gate 3 ve Gate 4'ü tam "wired" olarak
> gösteriyordu. `report.py`'nin gerçek import satırları taranarak kontrol edildi; iki hücre
> yanlıştı ve düzeltildi (bkz. notlar). Detay: `docs/module_status.md`.

| Gate | Mevcut Modül(ler) | Durum |
|------|-------------------|-------|
| Gate 1 | cv_parser, format_metadata_hygiene | ✅ Modüller var, P0.3+P0.4 ile wired |
| Gate 2 | evidence_bank, completeness_guard | ✅ Modüller var, P0.4 ile wired |
| Gate 3 | locale_consistency ✅ wired; multilevel (lang_gate) ❌ **wired değil** | ⚠️ **Düzeltildi:** `report.py` yalnızca `locale_consistency.locale_mismatches` çağırıyor. `multilevel.lang_gate()` hiç import/çağrı edilmiyor — "lang_gate" ismi kodda yalnızca yorum satırlarında kavramsal olarak geçiyor. Gate 3 şu an yalnızca locale kontrolü yapıyor, TR/EN karışıklığı (lang_gate) kontrolü YOK. |
| Gate 4 | scoring, cliche_tone ✅ wired; calibration ❌ **wired değil (bilerek)** | ⚠️ **Düzeltildi:** `calibration.py` fonksiyonları (`create_calibration`/`suggest_weight_adjustment`) P0-4 fix ile BİLEREK build_report()'tan çıkarıldı (gerçek dış referans olmadan sahte "mükemmel korelasyon" üretmesin diye). `qa_checks["calibration_hint"]` yalnızca statik "not_available" stub'ı döndürüyor — calibration.py çağrılmıyor. |
| Gate 5 | — (CLI human checkpoint) | ⚠️ P1 — approval hooks gerekli |

## Notlar

- Mevcut `build_report()` tüm QA modüllerini çalıştırıp `qa_checks` alanına yazar (v1.5.0'dan beri).
- Decision Engine bu sonuçları gate mantığıyla değerlendiren bir orkestratör katmanı olacak (P1) —
  bu belge bir tasarım/hedef durumu tarif ediyor, mevcut kod bunu henüz uygulamıyor (bkz. üstteki
  "Durum" satırı — bu kendi içinde zaten dürüstçe işaretlenmişti).
- G0–G4/5 gate orkestratörü, PASS/FAIL/REVIEW/WARN/ERROR/NOT_RUN durum modeli ve `diagnose` CLI
  komutu henüz yok — bunlar STAB-005/012/013 ve C-001 (ADR-001, PR #7) kapsamındaki v2.0 işleri.
- Her gate'in PASS/FAIL sonucu + neden + aksiyon metni üretmesi gerekiyor.
