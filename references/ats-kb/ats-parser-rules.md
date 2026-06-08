# ATS Ayrıştırıcı Kuralları

> **Kanonik konum:** `references/ats-kb/ats-parser-rules.md`  
> ATS sistemlerinin CV formatını nasıl ayrıştırdığını ve hangi format hatalarının skoru düşürdüğünü belgeler.

---

## 1. Biçim Cezalandırma Tablosu

| Format Hatası | Ayrıştırma Riski | Parse_gate Etkisi |
|--------------|-----------------|-------------------|
| İki sütunlu düzen | ATS sütunları birleştirir, anlamlı kelimeler karışır | ~0.6 |
| Tablo içinde metin | Tablo hücreleri okunmayabilir | ~0.7 |
| Metin kutusu (text box) | Çoğu ATS metin kutusunu görmez | ~0.6 |
| Header/Footer'da iletişim | Bazı ATS header/footer'ı okumaz | ~0.8 |
| Grafik/logo/ikon | Tamamen görmezden gelinir | Bilgi kaybı |
| Görüntü PDF / taranmış CV | OCR gerektiren içerik reddedilir | ~0.5 |
| Standart dışı başlık | "İş Deneyimlerim" → ATS "Experience" göremez | Bölüm kaybı |

**Önerilen:** tek sütun, standart başlıklar, .docx formatı.

---

## 2. Standart Bölüm Başlıkları (ATS-güvenli)

| Türkçe | İngilizce karşılığı |
|--------|-------------------|
| Özet / Profil | Summary / Profile |
| Deneyim | Experience / Work Experience |
| Beceriler | Skills |
| Eğitim | Education |
| Sertifikalar | Certifications |
| Diller | Languages |
| Referanslar | References |

**Yaratıcı başlıklar** ("Kariyer Yolculuğum", "Süper Güçlerim") kullanma — ATS tanımaz.

---

## 3. Akronim Kuralı

Her teknik akronimin ilk kullanımında açık halini ver:

```
"Akreditif (Letter of Credit / L/C)"
"Arama Motoru Optimizasyonu (SEO)"
"İnsan Kaynakları (HR / Human Resources)"
```

Sonraki kullanımlarda kısa hali yeterli. Bu, hem ATS eşleşmesini hem insan okuyucuyu kapsar.

---

## 4. Dosya Formatı Tercihleri

| Format | ATS Uyumu | Açıklama |
|--------|-----------|----------|
| .docx | ✅ En iyi | Çoğu ATS (Workday/Greenhouse/iCIMS) doğrudan okur |
| .pdf (metin) | ✅ İyi | Modern ATS metin PDF okur; eski sistemler sıkıntılı |
| .pdf (görüntü) | ❌ Kötü | OCR hatalı; kullanma |
| .doc (eski) | ⚠️ Riskli | Eski format; .docx tercih et |
| .txt | ⚠️ Sınırlı | Biçim bilgisi yok; yalnızca içerik |

---

## 5. İçerik Yapısı

- **Kronoloji:** ters kronolojik (en yeni önce) veya hibrit
- **Tarih formatı:** `Ay YYYY – Ay YYYY` ya da `YYYY – YYYY` tutarlı kullan
- **İletişim bilgisi:** CV'nin gövdesinde (header/footer'da değil)
- **URL'ler:** LinkedIn profili ve GitHub gibi linkleri ekle; ATS çoğu zaman ayrıştırır
- **Sayfa uzunluğu:** 1–2 sayfa (kıdemli için 2–3 kabul edilebilir)

---

## 6. Parse_gate Hesaplama Rehberi

```
Parse_gate = 1.0  → tek sütun + standart başlıklar + .docx + iletişim gövdede
Parse_gate = 0.9  → küçük format sorunu (ör. bir grafik var ama kritik değil)
Parse_gate = 0.8  → orta sorun (ör. header'da iletişim)
Parse_gate = 0.7  → ciddi sorun (ör. bazı tablo kullanımı)
Parse_gate = 0.6  → iki sütun veya metin kutusu dominant
Parse_gate < 0.6  → ayrıştırma başarısız sayılır; CV yeniden yapılandırılmalı
```

Parse_gate çarpan olarak uygulanır: `Score = clamp(Parse_gate × RAW, 0, 1)`
