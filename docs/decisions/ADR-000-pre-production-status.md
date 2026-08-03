# ADR-000 — Pre-Production Durum Beyanı ve Baseline Dondurma

**Tarih:** 2026-08-03
**Durum:** Kabul edildi
**Bağlam:** 5 turluk dış AI denetiminin (ChatGPT+Claude, Claude Science araştırma paketi,
28 referans repo taraması) kanonik kapanış kararı (A12 maddesi).

## Karar

`ATS-Friendly-CV-Modules`, bu ADR'nin yazıldığı tarih itibarıyla **araştırma prototipidir
(research prototype); production-ready DEĞİLDİR.** Bu, motorun işe yaramadığı anlamına
gelmez — deterministik, test edilmiş ve yararlı bir teşhis aracıdır. Ama şu iddialar
**henüz doğrulanmamıştır** ve kanonik olarak kabul edilmemelidir:

- Gerçek ticari ATS (Workday/Greenhouse/iCIMS/Taleo vb.) tenant'ında canlı test edilmedi.
- İşe alım *sonucu* (mülakat çağrısı, teklif) ile motor skoru arasında ölçülmüş bir
  korelasyon yoktur.
- "%75-85 = mülakata hazır" gibi ifadeler bir **hizalanma sinyali**dir, garanti değildir
  (bkz. `docs/03-skorlama-matematigi.md` "Dürüst statü" ve CHANGELOG `[1.5.1]`).

## Dondurulmuş baseline

- **Pre-`v1.5.1` baseline commit:** `3b6cce1e4c2919146752590f7bece4ae2812a8f5` (2026-06-15,
  `v1.5.0` olarak `pyproject.toml`'da adlandırılmıştı ama **hiçbir zaman gerçek bir GitHub
  tag/release olarak yayınlanmadı** — bu ADR'nin doğrudan tetikleyicisi budur).
- **`v1.5.1`** (bu ADR'nin dahil olduğu sürüm): PR #4 (`fix/p0-stabilization`, kanonik A1-A8
  maddeleri) + PR #5 (`fix/p1-hardening`, kanonik A9-A11 maddeleri + bu ADR) birleşimidir.
  Bu, gerçek anlamda etiketlenen/yayınlanan **ilk sürümdür**.

## Neden "v1.5.0"u gerçek bir sürüm olarak yayınlamıyoruz

`v1.5.0` adı altında yapılan çalışma gerçekti (43 test, P0.1-P0.4 düzeltmeleri) ama:
1. Hiçbir zaman bir git tag'ine bağlanmadı — "sürüm" yalnızca `pyproject.toml` metniydi.
2. Kendi döneminde bilinmeyen, sonradan bu denetim zincirinde bulunan ciddi P0 hataları
   içeriyordu (boş must_have fail-open, sahte kalibrasyon, paketleme hatası, vb.).
3. Şimdi geriye dönük "v1.5.0 production-ready idi" demek, kanonik denetimin bulduğu
   gerçek hataları gizlemiş olurdu (dürüstlük ilkesiyle çelişir — bkz. `CONTRIBUTING.md`).

Bu yüzden `v1.5.0` bir git tag'i olarak **hiç oluşturulmayacak**; sürüm numaralandırması
doğrudan `v1.5.1`'den (bu ADR ile birlikte) başlıyor.

## Feature freeze

`v1.5.1` kapsamındaki değişiklikler yalnızca **stabilizasyon** (bug fix, hardening, dürüstlük
düzeltmesi) idi — yeni özellik eklenmedi. Yeni özellik geliştirmesi (B serisi / v2.0
contract-first mimarisi, yeni domain pack, yeni entegrasyon vb.) şu ana kadar **başlatılmadı**
ve şu koşul sağlanana kadar başlamamalıdır:

> Kanonik A1-A12 listesindeki tüm P0 maddeleri kapatılmış ve `main`'e merge edilmiş olmalı.

Bu ADR'nin kabulüyle (A1-A11 tamamlandı) bu koşul karşılanmıştır; A12'nin geri kalan parçası
(bu ADR + sürüm etiketleme) da bu PR ile tamamlanmaktadır. **v2.0 contract-first çalışmasının
ne zaman başlayacağı ayrı bir insan kararıdır**, bu ADR onu otomatik olarak başlatmaz.

## Sonuç

- Bu ADR'den sonraki her PR, önce hangi kanonik maddeye (A/B/C/... serisi) karşılık geldiğini
  commit mesajında/PR açıklamasında belirtmelidir.
- "Done"/tamamlandı statüsü yalnızca canlı kabul testi (pytest + ruff + mypy + clean-room
  kurulum) geçtiğinde verilir — bkz. `CHANGELOG.md [1.5.1]` "N-05" bulgusu (Notion/Linear/Jira
  "Done" kayıtlarının kabul kanıtı olmadan güvenilmemesi gerektiği).
