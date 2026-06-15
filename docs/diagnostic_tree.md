# ATS Diagnostic Tree — 7-Dallı Tanı Ağacı

> **Kaynak:** Google Ads 8-dallı tanı ağacından uyarlandı (Viktor Hybrid Revizyon v2.0, Desen 2)
> **Durum:** Tasarım belgesi — P1 aşamasında CLI'a entegre edilecek

## Amaç

Bir CV düşük skor aldığında dalları sırayla kontrol ederek kök nedeni bul.
**Dalların sırası önemli** — üst daldaki sorunu çözmeden alt dalla uğraşma.

## 7 Dal

```
[1] MEASUREMENT (Parse/Format)
    │ ParseGate < 0.7?
    │ Format hatası var mı? (tablo, çift sütun, özel karakter)
    │ → FIX: CV formatını düzelt, .docx kullan
    │
[2] EVIDENCE (Kanıt)
    │ Evidence Recall < 70%?
    │ Framework CV'deki kanıtlar CV'ye aktarılmış mı?
    │ → FIX: Framework CV'ye dön, eksik kanıtları ekle
    │
[3] LANGUAGE (Dil Tutarlılığı)
    │ JD dili ≠ CV dili?
    │ TR/EN karışmış mı? Locale uyumsuzluğu?
    │ → FIX: Dil tutarlılığını sağla, AmE/BrE eşleştir
    │
[4] SCORING (Skor Bileşenleri)
    │ Hangi bileşen düşük? Lex / Sem / Cov?
    │ Cov düşük → must-have terimler eksik
    │ Lex düşük → keyword density yetersiz
    │ Sem düşük → anlamsal uyumsuzluk
    │ → FIX: Düşük bileşene özel aksiyon
    │
[5] CONTENT (İçerik Kalitesi)
    │ Cliché oranı > 15%?
    │ Quantification < 5?
    │ Pasif yapı oranı yüksek mi?
    │ → FIX: Aktif fiiller, somut metrikler ekle
    │
[6] CALIBRATION (Kalibrasyon)
    │ Engine skoru ↔ Jobscan skoru delta > 10?
    │ Ağırlıklar dengesiz mi?
    │ → FIX: calibration tablosu ile kalibre et
    │
[7] EXTERNAL (Dış Faktörler)
    │ JD çok niş mi? (domain pack eksik)
    │ Knockout var mı? (sertifika/deneyim yılı)
    │ → FIX: Domain pack ekle veya knockout'u kabul et
```

## Modül Eşlemesi

| Dal | Kontrol Modülü | Fonksiyon |
|-----|----------------|-----------|
| 1 | cv_parser, format_metadata_hygiene | parse_safety_score(), full_hygiene_check() |
| 2 | completeness_guard, evidence_bank | evidence_recall(), provenance_check() |
| 3 | locale_consistency, multilevel | locale_mismatches(), lang_gate() |
| 4 | scoring | ats_match_score() components |
| 5 | cliche_tone, quantification_score, text | detect_cliches(), quantification_audit(), looks_passive() |
| 6 | calibration | create_calibration(), suggest_weight_adjustment() |
| 7 | domain_packs, jd_parser | detect_domain(), knockouts |

## Kullanım

```bash
# Gelecek: diagnostic komutu (P1)
python -m ats_engine.cli diagnose --jd jd.txt --cv cv.txt --framework framework_cv.md
```

Şu an `build_report()` tüm modülleri çalıştırıyor (`qa_checks`).
P1'de diagnostic tree bu sonuçları sıralı dallarla yorumlayacak.
