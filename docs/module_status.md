# Module Status Matrix — 5-Seviyeli Durum Tablosu

> **Kaynak:** Viktor Hybrid Revizyon v2.0, Karar K8
> **Son Güncelleme:** v1.5.0 (15 Haziran 2026)

## 5 Seviye

1. **Exists** — Dosya repoda var
2. **Exported** — `__init__.py` `__all__` listesinde
3. **Tested** — `test_core.py` veya ayrı test dosyasında test var
4. **Wired** — `report.py` veya `cli.py` tarafından çağrılıyor
5. **Operational** — Bilinen bug yok, üretimde güvenle kullanılabilir

## Modül Durum Matrisi (v1.5.0)

| Modül | Exists | Exported | Tested | Wired | Operational | Not |
|-------|--------|----------|--------|-------|-------------|-----|
| scoring.py | ✅ | ✅ | ✅ | ✅ | ✅ | Ana motor |
| jd_parser.py | ✅ | ✅ | ✅ | ✅ | ✅ | 7 katmanlı parse |
| evidence_bank.py | ✅ | ✅ | ✅ | ✅ | ✅ | Framework CV → kanıt |
| synthesis.py | ✅ | ✅ | ✅ | ✅ | ✅ | XYZ/CAR/gap/anti-stuffing |
| report.py | ✅ | ✅ | ✅ | ✅ | ✅ | 6+1 alanlık çıktı (qa_checks eklendi) |
| text.py | ✅ | ✅ | ✅ | ✅ | ✅ | P0.1 acronym-safe fix uygulandı |
| bm25.py | ✅ | ✅ | ✅ | ✅ | ✅ | Okapi BM25 |
| lexicons.py | ✅ | ✅ | ✅ | ✅ | ✅ | Fiil + beceri normalizasyonu |
| domain_packs.py | ✅ | ✅ | ✅ | ✅ | ✅ | Tek pack (foreign-trade) |
| multilevel.py | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | L1-L3 + LangGate örtük kullanım |
| cv_parser.py | ✅ | ✅ | ✅ | ✅ | ✅ | P0.3 auto ParseGate uygulandı |
| cli.py | ✅ | ✅ | ✅ | ✅ | ✅ | CLI arayüzü |
| calibration.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** |
| cliche_tone.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** |
| completeness_guard.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** |
| format_metadata_hygiene.py | ✅ | ✅ | ✅ | ✅ | ⚠️ | **P0.4 ile bağlandı** — isim yanıltıcı (P0.7) |
| locale_consistency.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** |
| quantification_score.py | ✅ | ✅ | ✅ | ✅ | ✅ | **P0.4 ile report.py'a bağlandı** |

## Özet

- **v1.4.0:** 12 operasyonel, 6 unwired (exists+exported+tested ama pipeline'a bağlı değil)
- **v1.5.0:** 18 modülün 17'si tam operasyonel, 1 uyarılı (format_metadata_hygiene isim)
- **multilevel.py:** L1-L3 seviyeli skorlama örtük olarak kullanılabiliyor ama `build_report()` tarafından doğrudan çağrılmıyor — report sadece L1 seviyesinde çalışıyor

## Güncelleme Politikası

Yeni modül eklendiğinde bu tabloyu güncelleyin:
1. Dosya oluşturuldu → Exists ✅
2. `__init__.py`'ye eklendi → Exported ✅
3. Test yazıldı → Tested ✅
4. `report.py` veya `cli.py`'da import + çağrı → Wired ✅
5. Bilinen bug yok → Operational ✅
