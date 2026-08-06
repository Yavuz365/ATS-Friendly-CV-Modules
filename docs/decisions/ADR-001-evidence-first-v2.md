# ADR-001 — Evidence-First v2.0 Ürün Sözleşmesi

**Tarih:** 2026-08-05

**Durum:** Kabul edildi
**Karar sahibi:** Repository Product Owner

## Karar

Product Owner’ın 5 Ağustos 2026 tarihli açık talebiyle feature freeze kaldırıldı ve
evidence-first v2 sözleşmesi onaylandı. `v1.5.x` davranışı Legacy Diagnostic Engine
olarak korunur; yeni kanonik çıktı tek bir “ATS geçiş” skoru değil, bağımsız kanıt,
uygunluk, belge ayrıştırma, gereksinim kapsamı, terminoloji ve insan onayı sonuçlarıdır.

Bu karar yeniden yazım değildir. Paketleme, CLI iskeleti, BM25/TF-IDF tanıları,
TR/EN normalizasyonu, domain pack’ler, evidence-bank fikri ve tarihsel kayıt korunur.

## Değişmez kurallar

1. Lexical/semantic değerler tanıdır; ticari ATS geçişi, mülakat veya işe alım
   olasılığı değildir.
2. `UNKNOWN`, `NOT_COLLECTED`, `ERROR` ve `NOT_RUN` hiçbir sayısal fallback ile
   `PASS` veya `1.0` olamaz.
3. Final CV’ye önerilen her yeni iddia evidence ID taşır. Sözcüksel örtüşme
   `VERIFIED` sayılmaz.
4. Eligibility, evidence integrity ve document-parse kapıları fail-closed çalışır.
5. DOCX/PDF ingestion sonucu düz metin heuristiğinden ayrı raporlanır; scanned PDF
   OCR yoksa açık hata, mixed PDF ise `REVIEW` üretir.
6. Korunan aday olguları (şirket, unvan, tarih, derece, dil seviyesi, metrik) sentez
   katmanında değiştirilemez.
7. Production export için G0–G4 sonuçları ve açık insan onayı gerekir.
8. Ticari ATS davranışı, hiring outcome, vendor capability ve yeni dil/domain
   genellemeleri ancak sürümlü ampirik veriyle iddia edilir.

## Uygulama sözleşmesi

- Python sınırı: `engine/ats_engine/contracts.py`
- JSON sınırı: Draft 2020-12, kapalı nesneler, `schemas/v2/`
- Durumlar: `KNOWN/UNKNOWN/NOT_COLLECTED/NOT_APPLICABLE/CONFLICTED`,
  `VERIFIED/PARTIAL/UNVERIFIED/REJECTED`,
  `PASS/FAIL/REVIEW/WARN/ERROR/NOT_RUN`
- Kapılar: G0 Input/Integrity, G1 Eligibility, G2 Evidence/Truth,
  G3 Parse/Language/Consistency, G4 Human Approval
- Legacy skor: yalnız `legacy_diagnostic_percent` olarak açıklamalı geçiş alanı;
  boş açık gereksinimde kanonik `score_percent=null` ve `NOT_EVALUATED`.

## Sonuçlar

- `2.0.0-alpha.1` bir sözleşme/araştırma alfa sürümüdür; production-ready değildir.
- UI, otomasyon ve vendor-specific entegrasyonlar bu ADR ile otomatik onaylanmaz.
- Taslak PR #7 bu kabul edilmiş ADR ve uygulama PR’ı tarafından supersede edilir.

## Kaynak izi

- Birleşik sentez/yol haritası, 4 Ağustos 2026
- 72 maddelik kanonik backlog, 2 Ağustos 2026
- ADR-000 pre-production kararı
- Product Owner’ın Main Repo’da tüm gerekli revizyonları uygulama talebi, 5 Ağustos 2026
