# ATS-Friendly CV Modules

> **İş ilanını çöz → Kariyer verisiyle yeniden bağla → Ölç ve doğrula.**  
> ATS-uyumlu, ilana özel CV üretimi için matematiksel ve algoritmik motor.

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./ats-cv-architect_SKILL.md)
[![Claude Skill](https://img.shields.io/badge/Claude-Native%20Skill-orange)](./ats-cv-architect.skill)
[![LLM: Any](https://img.shields.io/badge/LLM-Gemini%20%7C%20ChatGPT%20%7C%20Claude%20%7C%20DeepSeek-blue)](./ats-cv-architect_MASTER-PROMPT-TR.md)
[![n8n Ready](https://img.shields.io/badge/n8n-Workflow%20Ready-brightgreen)](./ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md)

---

## 🎯 Ne Yapar?

Bu repo, herhangi bir iş ilanını ATS (Applicant Tracking System) filtrelerinden geçirecek,
ilana özel, kanıta dayalı bir CV üretmek için gereken **tüm motor, formül, prompt ve skill
dosyalarını** barındırır.

Sistem **iki katmanlı diyalektik bir motordur:**

```
[İŞ İLANI (JD)] ──► ANALİZ (çöz) ──► 7 katmanlı ayrıştırma + ağırlıklı keyword listesi
                                              │
                         [ADAY FRAMEWORK CV] ─┘
                                              │
                       SENTEZ (yeniden bağla) ──► XYZ başarı cümleleri + semantik kümeler
                                              │
                     SKORLAMA + GAP ANALİZİ ──► Hibrit ATS Match Score + P/R/F1
                                              │
                          [skor < hedef?] ────┘ → sentez döngüsü
                                              │
                              FINAL ATS CV ◄──┘
```

**Hedef skor bandı:** `%75–85` · `>%90` şişirme sinyali · `<%50` ciddi iyileştirme gerekir.

---

## 📁 Dosya Rehberi

### 🔧 Claude Native Skill Paketleri

| Dosya | Açıklama |
|-------|----------|
| [`ats-cv-architect.skill`](./ats-cv-architect.skill) | **Ana skill paketi.** Claude'a yükle → `Settings → Skills → Upload`. JD + Framework CV verince otomatik 5-katman protokolü çalıştırır. |
| [`synthesis-analysis-research.skill`](./synthesis-analysis-research.skill) | **Denetim/araştırma skill'i.** Herhangi bir metni/raporu `synthesis-analysis-research` disipliniyle tarar; hatalar `[DÜZELTME]` etiketiyle işaretlenir. |

> ⚠️ `.skill` dosyaları **yalnızca Claude ekosisteminde** çalışır. Diğer modeller için aşağıdaki Master Prompt'u kullanın.

---

### 📋 Orkestratör & Referans Dosyaları

| Dosya | Açıklama |
|-------|----------|
| [`ats-cv-architect_SKILL.md`](./ats-cv-architect_SKILL.md) | Skill orkestratörü. Katman 0–5 protokolü, mod seçimi (tek ilan / toplu / teşhis), revizyon döngüsü kuralı, kalite & etik korumaları. |
| [`ats-cv-architect_SCORING-FORMULAS.md`](./ats-cv-architect_SCORING-FORMULAS.md) | **Tüm matematik.** TF-IDF, BM25 (Okapi), Kosinüs benzerliği, SBERT semantik katmanı, Hibrit ATS Match Score (denetim-düzeltmeli), P/R/F1, çözümlü örnek. |
| [`ats-cv-architect_TUM-SKILL-BIRLESIK.md`](./ats-cv-architect_TUM-SKILL-BIRLESIK.md) | Skill'in **8 dosyasını tek MD'de** birleştirir. Claude dışı modellere tam bağlamı bir seferde vermek için kullanın (54 KB). |

---

### 🚀 Taşınabilir Prompt (Herhangi Bir LLM)

| Dosya | Açıklama |
|-------|----------|
| [`ats-cv-architect_MASTER-PROMPT-TR.md`](./ats-cv-architect_MASTER-PROMPT-TR.md) | **Kopyala-yapıştır hazır.** Gemini, ChatGPT, DeepSeek, GLM, Qwen, Mistral'a olduğu gibi ver. `<<< >>>` arasını doldur → 6 sabit alan + FINAL CV üretir. |

---

### 📚 Araştırma & Kurulum Belgeleri

| Dosya | Açıklama |
|-------|----------|
| [`ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md`](./ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md) | Denetim raporu (bulunan 10 hata + düzeltmeler), kurulum aşamaları (Hafta 1–4), diyalektik düşünme döngüsü, dürüst sınırlamalar. |
| [`synthesis-analysis-research_FULL.md`](./synthesis-analysis-research_FULL.md) | `synthesis-analysis-research` skill'inin tam dokümantasyonu. Çok dilli kaynak sentezi (13+ dil), akademik referanslar, araştırma metodolojisi. |

---

## ⚙️ Hızlı Başlangıç

### Yol 1 — Claude ile (Tam Otomatik)

```
1. ats-cv-architect.skill dosyasını Claude'a yükle
   → Settings → Capabilities/Skills → Upload

2. Yeni sohbet aç ve yaz:
   "Şu ilanı Framework CV'me göre analiz et ve ATS CV üret:"
   [JD metnini yapıştır]
   [Framework CV'ni yapıştır]

3. Claude otomatik olarak 5 katmanı çalıştırır:
   Katman 0: Alım & Mod seçimi
   Katman 1: Bütünsel kavrama
   Katman 2: 7 katmanlı JD analizi
   Katman 3: Hibrit skor + gap
   Katman 4: Sentez (XYZ cümleleri)
   Katman 5: Doğrulama & teslim
```

### Yol 2 — Herhangi Bir LLM ile (Master Prompt)

```
1. ats-cv-architect_MASTER-PROMPT-TR.md dosyasını aç
2. <<< İŞ İLANI >>> kısmına ilanı yapıştır
3. <<< FRAMEWORK CV >>> kısmına kariyerini yapıştır
4. Tüm prompt'u Gemini / ChatGPT / DeepSeek'e gönder
5. 6 sabit alan alırsın:
   keywords → analysis → summary → synthesis → match_score → gap_analysis
   + FINAL ATS CV + provenans tablosu
```

### Yol 3 — Çok Araçlı Drive Akışı (A.1–A.3 / B.1)

```
A.1 JD'yi Drive'a Word olarak yükle (3 etiketli bölüm):
    [JD-ORİJİNAL] | [ANALİZ] | [SENTEZ-ÖNERİ]

A.2 Gemini ile ANALİZ+SENTEZ → çıktıyı [SENTEZ-ÖNERİ]'ye yapıştır
    ⚠️ JD-ORİJİNAL'e asla karıştırma (kirlenme riski)

A.3 Master Prompt ile 6 alanı üret → Word/Notion'a kaydet

B.1 CV-yazıcı LLM: Drive'dan 6 alan + Framework CV →
    eşleşen+kanıtlı girdileri seç → ATS CV yaz →
    skor hesapla → provenans kontrolü → teslim
```

---

## 🧮 Temel Formüller

```
Hibrit ATS Match Score (denetim-düzeltmeli):

  RAW   = α·Lex + β·Sem + γ·Cov − ζ·Stuffing
  Score = clamp( Parse_gate × RAW , 0 , 1 )

  Önerilen ağırlıklar:
    α = 0.35  (BM25 lexical eşleşme)
    β = 0.30  (SBERT semantik benzerlik)
    γ = 0.35  (zorunlu terim kapsamı)
    ζ = 0.20  (şişirme cezası)
    Parse_gate ∈ [0.6, 1.0]  (biçim kapısı — çarpan, toplam değil)

Gap analizi:
  gap_kapatılabilir  = Framework CV'de kanıtı var, henüz CV'ye yansımamış
  gap_kapatılamaz    = adayda gerçekten yok → asla uydurma
```

> Tam türetim, düzeltmeler ve çözümlü örnek →
> [`ats-cv-architect_SCORING-FORMULAS.md`](./ats-cv-architect_SCORING-FORMULAS.md)

---

## 🛠️ Desteklenen Araçlar

| Araç | Kullanım |
|------|----------|
| **Claude** (claude.ai / Claude Code) | Native `.skill` dosyaları — tam otomatik 5-katman protokol |
| **Gemini** | Master Prompt · Drive entegrasyonu · SEO analiz+sentez |
| **ChatGPT / GPT-4** | Master Prompt · toplu mod · xlsx export |
| **DeepSeek / GLM / Qwen / Mistral** | Master Prompt (taşınabilir) |
| **n8n** | Drive tetikleyici → model çağrısı → 6 alan → Sheet/Notion → Telegram |
| **Google Drive** | Etiketli Word şablonu (JD-ORİJİNAL / ANALİZ / SENTEZ-ÖNERİ) |

---

## ⚖️ Etik & Kalite Kuralları

| Kural | Açıklama |
|-------|----------|
| **Provenans zorunlu** | CV'deki her madde Framework CV'deki bir girdiye izlenebilmeli |
| **Dürüstlük mutlak** | Adayda olmayan beceri/keyword asla eklenmez |
| **Coverage > Density** | Keyword yoğunluğu değil, kapsam ve kanıt birincildir |
| **Parse güvenliği** | Tek sütun · standart başlıklar · tablo/grafik yok · .docx tercih |
| **Skor proxydır** | Workday/Greenhouse/iCIMS iç formülleri tescillidir; bu skor *yaklaşıklamadır* |

---

## 📊 Denetim Özeti

`synthesis-analysis-research` disipliniyle yapılan denetimde sistemde **10 hata** bulunmuş
ve giderilmiştir. Kritik düzeltmeler:

- **H1** Revizyon döngüsü sonsuz döngüye giriyordu → `gap = kapatılabilir` kısıtı eklendi
- **H2** `.skill` taşınabilirlik kırılması → Master Prompt ayrı tutuldu
- **M1** Skor alt sınırı negatife inebiliyordu → `clamp(..., 0, 1)` eklendi
- **M2** Parse toplama yerine çarpan/kapı olarak yeniden tasarlandı
- **M3** Lex/Cov çift sayım problemi → ayrı görevlere ayrıldı

> Tam denetim raporu → [`ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md`](./ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md)

---

## 🗺️ Yol Haritası

- [x] ATS CV Architect skill (Claude native)
- [x] Synthesis & Analysis Research skill
- [x] Taşınabilir Master Prompt (tüm LLM'ler)
- [x] Denetim-düzeltmeli hibrit skorlama formülleri
- [ ] `engine/` — Python deterministik skorlayıcı (`ats_score.py`)
- [ ] `docs/` — Metodoloji & mimari dokümantasyon
- [ ] `templates/` — JD etiketli şablon, kanıt bankası şablonu
- [ ] `workflows/` — n8n pipeline, Notion veritabanı şeması
- [ ] Finans / borsa otomasyon modülleri

---

## 📄 Lisans

Bu repo **proprietary** içerik barındırmaktadır.  
Skill'ler ve prompt'lar kişisel iş akışı için tasarlanmıştır.  
Ticari kullanım veya yeniden dağıtım için repo sahibiyle iletişime geçin.

---

<div align="center">

**Analiz çözer · Sentez bağlar · Skor doğrular**

*Disiplinin kendisi üründür.*

</div>
