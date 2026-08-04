# Module Status Matrix — 5-Seviyeli Durum Tablosu

> **Kaynak:** Viktor Hybrid Revizyon v2.0, Karar K8
> **Son Güncelleme:** v1.5.1 (2026-08-05 — canlı kodla senkronize edildi)

## 5 Seviye

1. **Exists** — Dosya repoda var
2. **Exported** — `__init__.py` `__all__` listesinde
3. **Tested** — `test_core.py` veya ayrı test dosyasında test var
4. **Wired** — `report.py` veya `cli.py` tarafından çağrılıyor
5. **Operational** — Bilinen bug yok, üretimde güvenle kullanılabilir

## Modül Durum Matrisi (v1.5.1)

| Modül | Exists | Exported | Tested | Wired | Operational | Not |
|-------|--------|----------|--------|-------|-------------|-----|
| scoring.py | ✅ | ✅ | ✅ | ✅ | ✅ | Ana motor |
| jd_parser.py | ✅ | ✅ | ✅ | ✅ | ✅ | 7 katmanlı parse |
| evidence_bank.py | ✅ | ✅ | ✅ | ✅ | ⚠️ | Framework CV → kanıt; basit sözcüksel örtüşmeye "doğrulandı" diyor — gerçek olgusal doğrulama değil (2026-08-05 denetiminde bulundu) |
| synthesis.py | ✅ | ✅ | ✅ | ✅ | ✅ | XYZ/CAR/gap/anti-stuffing |
| report.py | ✅ | ✅ | ✅ | ✅ | ✅ | 6+1 alanlık çıktı (qa_checks eklendi) |
| text.py | ✅ | ✅ | ✅ | ✅ | ✅ | P0.1 acronym-safe fix uygulandı |
| bm25.py | ✅ | ✅ | ✅ | ✅ | ✅ | Okapi BM25 — scoring.py üzerinden dolaylı wired |
| lexicons.py | ✅ | ✅ | ✅ | ✅ | ✅ | Fiil + beceri normalizasyonu — scoring/jd_parser/synthesis üzerinden dolaylı wired |
| domain_packs.py | ✅ | ✅ | ✅ | ✅ | ✅ | Tek pack (foreign-trade) |
| multilevel.py | ✅ | ✅ | ✅ | ❌ | ⚠️ | **Düzeltme (2026-08-05):** `report.py` bu modülü hiç import etmiyor/çağırmıyor — `lang_gate()` yalnızca yorum satırlarında kavramsal olarak geçiyor. L1-L3 skorlama örtük kullanılabilir durumda ama pipeline'a bağlı değil. `docs/decision_engine.md` Gate 3 tablosu bunu artık doğru yansıtıyor. |
| cv_parser.py | ✅ | ✅ | ✅ | ✅ | ⚠️ | P0.3 auto ParseGate uygulandı; yalnızca önceden çıkarılmış düz metin işliyor — ikili DOCX/PDF ayrıştırma yok (2026-08-05 denetiminde teyit edildi) |
| cli.py | ✅ | ✅ | ✅ | ✅ | ✅ | CLI arayüzü |
| calibration.py | ✅ | ✅ | ✅ | ❌ | ⚠️ | **Düzeltme (2026-08-05):** Bu satır önceden "P0.4 ile report.py'a bağlandı" diyordu — bu yanlıştı. `report.py` içindeki P0-4 fix yorumu açıkça şunu söylüyor: "create_calibration/suggest_weight_adjustment artık build_report() içinde çağrılmıyor" — gerçek dış referans skoru (ör. Jobscan) olmadan sahte "✅ mükemmel korelasyon" üretmemek için BİLEREK ayrıldı. `qa_checks["calibration_hint"]` yalnızca statik bir "not_available" stub'ı; calibration.py fonksiyonları çağrılmıyor. Ayrı bir kalibrasyon script akışında hâlâ kullanılabilir. |
| cliche_tone.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** (`detect_cliches` import doğrulandı) |
| completeness_guard.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** (`evidence_recall` import doğrulandı) |
| format_metadata_hygiene.py | ✅ | ✅ | ✅ | ✅ | ⚠️ | **P0.4 ile bağlandı** (`full_hygiene_check` import doğrulandı) — isim yanıltıcı (P0.7) |
| locale_consistency.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** (`locale_mismatches` import doğrulandı) |
| quantification_score.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** (`quantification_audit` import doğrulandı) |

## Özet

- **v1.4.0:** 12 operasyonel, 6 unwired (exists+exported+tested ama pipeline'a bağlı değil)
- **v1.5.1:** 18 modülün 15'i tam operasyonel; 3'ü bilinçli/bilinen sınırlarla işaretli:
  `multilevel.py` (lang_gate hiç wired değil), `calibration.py` (P0-4 ile bilerek disconnect
  edildi, "bağlandı" değil), `cv_parser.py` (yalnızca düz metin, ikili DOCX/PDF yok).
- Bu tablo artık `report.py`'nin gerçek import listesi taranarak doğrulandı (2026-08-05),
  varsayım veya eski commit mesajlarına göre değil.

## Güncelleme Politikası

Yeni modül eklendiğinde bu tabloyu güncelleyin:
1. Dosya oluşturuldu → Exists ✅
2. `__init__.py`'ye eklendi → Exported ✅
3. Test yazıldı → Tested ✅
4. `report.py` veya `cli.py`'da import + çağrı → Wired ✅ (gerçek import satırını doğrula, yorum/commit mesajına güvenme)
5. Bilinen bug yok → Operational ✅
