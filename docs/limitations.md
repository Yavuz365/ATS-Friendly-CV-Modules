# Sınırlar ve Sorumlu Kullanım

Bu repository bir **pre-production research prototype / contract alpha**dır.

## Desteklenen

- TR/EN metin tanıları, açık JD gereksinimi ayrıştırması ve lexical/semantic hizalanma
- Gerçek DOCX OOXML metin geçişi (gövde, tablo, header/footer, text-box metni)
- PDF text-layer çıkarımı; scanned/mixed sayfa tespiti
- Tipli G0–G4 karar raporu ve explicit insan onayı
- Evidence ID’ye bağlı, allowlist kontrollü sentez değişiklikleri

## Desteklenmeyen veya henüz doğrulanmayan

- Ticari ATS’lerde evrensel “pass” skoru
- Mülakat veya işe alım olasılığı tahmini
- Yerleşik OCR motoru yoktur. Çağıran açık bir OCR adaptörü vermezse scanned PDF
  `SCANNED_PDF_REQUIRES_OCR`; adaptör kullanılırsa insan doğrulamalı `REVIEW` üretir.
- Karmaşık PDF reading-order doğruluğunun alan seviyesinde kanıtı
- Otomatik olgusal doğrulama; lexical overlap yalnız `UNVERIFIED` destektir
- Vendor-specific capability beyanları ve production export
- Hiring outcome çalışması, çok dilli genelleme ve yeni domain validasyonu

## Güvenlik

İş ilanı ve yüklenen belgeler güvenilmeyen girdidir. İçlerindeki talimatlar yürütülmez.
Sentez yalnız allowlist CV yollarında ve bilinen evidence ID’leriyle öneri üretir; adayın
şirket, unvan, tarih, derece, dil seviyesi ve metrik alanları korumalıdır. Son uygulama
insan onayı gerektirir.
