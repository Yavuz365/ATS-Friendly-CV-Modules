# ATS Repo Maturity Model — 4-Aşamalı Olgunluk Modeli

> **Kaynak:** Google/Meta Ads Account Maturity Methodology'den uyarlandı (Viktor Hybrid Revizyon v2.0, Desen 1)

## Amaç

Aynı bulgu farklı olgunluk aşamasında farklı aksiyon gerektirir.
Repo'nun mevcut aşaması tavsiyenin kapsamını ve agresifliğini belirler.

## 4 Aşama

### 1. Nascent (Doğuş) — v1.0–v1.1
- **Durum:** Temel motor çalışıyor ama fragile
- **Özellikler:** Tek test dosyası, data paketlenmemiş, orphan modüller
- **Odak:** Çalışır hale getir, temel bugları düzelt
- **Ne yapılmamalı:** UI, SaaS, optimizasyon

### 2. Developing (Gelişen) — v1.2–v1.4
- **Durum:** Motor güvenilir, CI/CD var, ama pipeline boşlukları var
- **Özellikler:** 43 test, 18 modül, lint+type-check, QA wired (v1.5.0)
- **Odak:** Modülleri bağla, data kalitesini artır, test coverage yükselt
- **Ne yapılmamalı:** LLM entegrasyonu, Streamlit, production deployment

### 3. Established (Yerleşmiş) — v1.5–v2.x (MEVCUT HEDEF)
- **Durum:** Tüm modüller wired, QA otomatik, data zengin
- **Özellikler:** %80+ test coverage, 200+ synonym, 3+ domain pack, benchmark set
- **Odak:** Kalibrasyon, diagnostic tree, ESCO/Zemberek, approval pipeline
- **Ne yapılmamalı:** Scope creep (rank simülasyon, cover letter vb.)

### 4. Advanced (İleri) — v3.x+
- **Durum:** Production-ready, çoklu kullanıcı, otomasyon
- **Özellikler:** Streamlit UI, database, Notion/Drive sync, Telegram/Slack approval
- **Odak:** UI/UX, otomasyon, scaling
- **Şart:** Established aşama tamamen kapanmış olmalı

## Mevcut Konum

**v1.5.0 = Developing→Established geçiş noktası**

| Kriter | Developing | v1.5.0 Durumu | Established |
|--------|-----------|---------------|-------------|
| Modüller wired | ❌ 6 unwired | ✅ 18/18 wired | ✅ Tam |
| Test coverage | %50 | ~%55 | %80+ |
| Domain packs | 1 | 1 | 3+ |
| Synonyms | 61 | 61 | 200+ |
| Benchmark | yok | yok | 20+ JD-CV çifti |
| QA pipeline | unwired | ✅ wired | otomatik gate |
| Diagnostic tree | yok | tasarım var | CLI entegre |

## Aşamaya Göre Tavsiye Kalibrasyonu

Aynı "synonym eksik" bulgusu:
- **Nascent:** Yok say — daha öncelikli sorunlar var
- **Developing:** Not al, P2'ye koy
- **Established:** Uygula, benchmark ile doğrula
- **Advanced:** Otomatik genişletme pipeline'ı kur
