# ATS-CV Pipeline — 7 Aşamalı Referans Dokümanı

> **Legacy pipeline:** Güncel kanonik akış ingestion → contracts → G0–G4 → explicit human approval’dır.

> Y36-14: Tüm pipeline aşamalarını tek bir referans dokümanında birleştir.

## Genel Bakış

```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
  JD        JD        Prompt     Engine     Sentez     CV         Doğru-
 alımı    analizi   yapılandır  skorlama   + kanıt   üretimi     lama
```

---

## Stage 0: JD Alımı ve Kayıt

**Girdi:** Ham iş ilanı (URL / metin)
**Çıktı:** `jd_raw.txt` → Drive'a kaydedilir

- İlanı düz metin olarak kopyala
- Başlık, şirket, konum, dil bilgilerini not al
- Drive → `ATS-CV-Pipeline/01-JD-Collection/` klasörüne kaydet

---

## Stage 1: JD Analizi (7 Katmanlı Ayrıştırma)

**Modül:** `jd_parser.parse_jd(jd_text)`
**Çıktı:** 7 alanlı yapılandırılmış analiz

| Katman | Alan | Açıklama |
|--------|------|----------|
| 1 | `identity` | Rol kimliği: unvan, kıdem, çalışma modeli, dil |
| 2 | `must_have` | Zorunlu beceriler (frekans + pozisyon ağırlıklı) |
| 3 | `nice_to_have` | Tercih edilen beceriler |
| 4 | `responsibilities` | Sorumluluk fiilleri |
| 5 | `knockouts` | Eleyici kriterler (lisans, sertifika vb.) |
| 6 | `lsi` | Latent Semantic Indexing genişletmeleri |
| 7 | `intent` | Rolün özü (tek cümle) |

---

## Stage 2: Master Prompt Yapılandırması

**Araç:** Notion Master Prompt template'i
**Çıktı:** AI'lara verilecek yapılandırılmış prompt

- Stage 1 çıktısını Master Prompt'a yerleştir
- Hedef ATS skoru, section haritası, anahtar kelime yoğunluğu tanımla
- domain-pack seçimi (ör. `foreign-trade-logistics`)
- Anti-stuffing limitleri belirle

---

## Stage 3: Engine Skorlama (Deterministik)

**Modül:** `scoring.ats_match_score(...)`
**Çıktı:** Skor yüzdesi + bileşenler + gap listesi

Formül:
```
Final = w_lex × Lex + w_sem × Sem + w_cov × Cov
Lex   = 0.70 × TF-IDF_cos + 0.30 × BM25_norm
Parse_gate ve Stuffing düzeltmeleri uygulanır
```

**Alt bileşenler:**
- `Lex` — Leksikal benzerlik (TF-IDF + BM25)
- `Sem` — Semantik benzerlik (SBERT)
- `Cov` — Zorunlu terim kapsamı (must_have coverage)
- `Parse_gate` — CV ayrıştırılabilirlik güvenliği
- `Stuffing` — Anahtar kelime şişirme cezası

---

## Stage 4: Sentez + Kanıt Eşleştirme

**Modüller:** `synthesis.py` + `evidence_bank.py`
**Çıktı:** Gap analizi + XYZ cümle şablonları

- `classify_gaps()` — Kapatılabilir vs kapatılamaz gap
- `anti_stuffing_report()` — Şişirme tespiti
- `cluster_skills()` — Semantik kümeleme
- `evidence_bank.parse_bank()` — Kanıt bankasını yükle

---

## Stage 5: CV Üretimi / Revizyonu

**Araçlar:** 5 AI (Layer 1) → Frankenstein birleştirme (Layer 2)
**Çıktı:** ATS-optimize edilmiş CV taslağı

1. Her AI aracına Stage 2 promptunu ver
2. Her birinden tam CV al
3. 8 bölümü (summary, experience ×4, skills, education, diğer) ayrı ayrı karşılaştır
4. En iyi bölümleri birleştir (Frankenstein CV)
5. Grammarly AI-detection kontrolü
6. İnsani düzenleme katmanı

---

## Stage 6: Doğrulama ve Kalibrasyon

**Modüller:** `report.build_report()` + Jobscan
**Çıktı:** Final skor + doğrulama raporu

1. Engine ile final skoru hesapla
2. Jobscan'e yükle → ATS skor karşılaştırması
3. Engine vs Jobscan farkını analiz et
4. Gerekirse Stage 5'e dön (revizyon döngüsü)
5. `stopping_condition()` sağlandığında teslim et

---

## Hızlı Referans: Modül → Stage Eşlemesi

| Modül | Stage | Rol |
|-------|-------|-----|
| `jd_parser.py` | 1 | JD'yi 7 katmana ayrıştır |
| `text.py` | 1,3 | Tokenizasyon, n-gram, dil kalitesi |
| `bm25.py` | 3 | BM25 relevance skoru |
| `scoring.py` | 3 | Ana skorlama motoru |
| `lexicons.py` | 3 | Sinonim eşleştirme |
| `cv_parser.py` | 3 | CV güvenlik skoru |
| `synthesis.py` | 4 | Gap analizi, XYZ sentezi |
| `evidence_bank.py` | 4 | Kanıt eşleştirme |
| `domain_packs.py` | 2,3 | Alan-özel keyword paketleri |
| `multilevel.py` | 3 | L1/L2/L3 + LangGate |
| `report.py` | 6 | 6 alanlı birleştirici rapor |
