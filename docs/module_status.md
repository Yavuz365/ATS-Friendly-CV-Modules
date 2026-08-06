# Module Status Matrix — 2.0.0-alpha.1

> **Son güncelleme:** 2026-08-05. “Operational” yerine kanıtlanabilir durum kullanılır;
> repository hâlâ pre-production contract alpha’dır.

| Modül | Test | Pipeline | Durum / sınır |
|---|---:|---:|---|
| `contracts.py` | ✅ | ✅ | 12 versioned Python contract + enum |
| `errors.py` | ✅ | ✅ | Stable error code boundary |
| `ingestion.py` | ✅ | CLI/API | DOCX full-story + PDF text layer; OCR uygulaması yok |
| `decision.py` | ✅ | `report.py` | G0–G4 typed DecisionReport |
| `safe_synthesis.py` | ✅ | API | Evidence ID + allowlist; değişiklik uygulama/export yok |
| `scoring.py` | ✅ | ✅ | Legacy diagnostic; empty must → NOT_EVALUATED |
| `jd_parser.py` | ✅ | ✅ | Explicit must; body inference must’a terfi etmez |
| `evidence_bank.py` | ✅ | ✅ | Lexical support; factual verification değil |
| `report.py` | ✅ | CLI/API | JSON/Markdown + decision + typed QA diagnostics |
| `multilevel.py` | ✅ | API/report LangGate | Legacy thresholds diagnostic |
| `cv_parser.py` | ✅ | ✅ | Text format heuristic; binary ingestion ayrı modülde |
| `text.py` / `lexicons.py` | ✅ | ✅ | `importlib.resources`; eksik kaynakta görünür hata |
| `domain_packs.py` | ✅ | API | Tek domain; eksik kaynak sessiz `[]` dönmez |
| `calibration.py` | ✅ | ❌ | Yalnız gerçek dış comparator verisiyle ayrı API |
| QA modülleri | ✅ | `report.py` | Hata `ERROR`; skor/recall olgusal doğrulama değil |

## Henüz yapılmayan

- OCR adaptörü ve alan seviyesinde gerçek belge gold corpus değerlendirmesi
- CandidateFact/Evidence deposunun kalıcı storage/consent/retention katmanı
- Production export, rollback ve uygulama event store
- Commercial ATS tenant ve hiring outcome validasyonu
- UI/Notion/vendor entegrasyonları
