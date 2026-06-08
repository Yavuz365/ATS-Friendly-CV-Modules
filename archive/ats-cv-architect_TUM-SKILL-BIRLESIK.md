> ⚠️ **ARŞİV DOSYASI — DÜZENLEME YAPMA.**  
> Bu dosya kanonik kaynak **değildir**. Yalnızca tarihsel referans için saklanmaktadır.  
> Kanonik dosyalar: `skills/ats-cv-architect/` ve `references/ats-kb/` altındadır.  
> Bkz. `docs/migration/legacy-map.md`

---

# ATS CV ARCHITECT — Tüm Skill, Tek Dosyada (Birleşik MD)

> Bu belge, `ats-cv-architect` skill'inin **sekiz dosyasının tamamını** hiçbir şey eksiltmeden tek bir markdown dosyasında birleştirir. Markdown dosyaları olduğu gibi (render edilebilir) gömülmüştür; Python betiği kod bloğu içindedir. Her bölüm `━━━ DOSYA n/8 ━━━` bandıyla ayrılır.
>
> Üretim tarihi: 2026-06-06 · Toplam dosya: 8 · Kaynak: paketlenmiş `ats-cv-architect.skill`

---

## Skill yapısı (dosya ağacı)

```
ats-cv-architect/
├── SKILL.md                          (orkestratör — her tetiklenmede yüklenir)
├── references/
│   ├── jd-decomposition.md           (ANALİZ şeması: JD'nin 7 katmanı)
│   ├── scoring-formulas.md           (matematik: TF-IDF/BM25/kosinüs/hibrit skor)
│   ├── synthesis-rules.md            (SENTEZ: kümeleme/XYZ/E-E-A-T/anti-stuffing/provenans)
│   └── workflow-drive-multitool.md   (Drive + Gemini + çok-LLM akışı)
├── assets/
│   ├── master-prompt-TR.md           (taşınabilir Master Prompt — her LLM için)
│   └── output-fields-template.md     (6 alanlık çıktı şablonu)
└── scripts/
    └── ats_score.py                  (deterministik skorlayıcı — Yol 2 çekirdeği)
```

## İçindekiler

1. **`SKILL.md`** — *Orkestratör*. Her tetiklenmede yüklenen ana dosya: ne işe yarar, mod seçimi, Katman 0-5 protokolü, döngü, çıktı, kalite kuralları.
2. **`references/jd-decomposition.md`** — *Referans*. ANALİZ şeması: bir iş ilanı hangi 7 parçaya ayrılır, modality ve ağırlıklandırma.
3. **`references/scoring-formulas.md`** — *Referans*. Tüm matematik: TF-IDF, BM25, kosinüs, hibrit ATS skoru (denetim-düzeltmeli), P/R/F1, çözümlü örnek.
4. **`references/synthesis-rules.md`** — *Referans*. SENTEZ mekaniği: kümeleme, LSI genişletme, XYZ/CAR, E-E-A-T, anti-stuffing, parse, provenans.
5. **`references/workflow-drive-multitool.md`** — *Referans*. Drive + Gemini + çok-LLM iş akışının kurulumu ve denetimi (A.1-A.3 / B.1).
6. **`assets/master-prompt-TR.md`** — *Varlık*. Herhangi bir LLM'e taşınabilir Master Prompt (Gemini/ChatGPT/DeepSeek/GLM/Qwen/Mistral).
7. **`assets/output-fields-template.md`** — *Varlık*. 6 alanlık çıktı şablonu (JSON + markdown).
8. **`scripts/ats_score.py`** — *Betik (Python)*. Deterministik TF-IDF/BM25/kosinüs/hibrit skorlayıcı (Yol 2 çekirdeği).

---



**━━━━━━━━━━ DOSYA 1/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/SKILL.md`  
**Tür:** Orkestratör  
**Açıklama:** Her tetiklenmede yüklenen ana dosya: ne işe yarar, mod seçimi, Katman 0-5 protokolü, döngü, çıktı, kalite kuralları.


---
name: ats-cv-architect
description: Build ATS-optimized, tailored CVs by decomposing a job posting (ANALYSIS) and recombining it against the candidate's master/framework CV (SYNTHESIS), then scoring the fit. Use this WHENEVER the user wants to tailor a CV/résumé to a specific job posting or job description (JD), optimize a CV for ATS / applicant tracking systems, compute an ATS match score, run keyword or gap analysis between a JD and a CV, or push a job posting through an "analysis + synthesis" / SEO pass to produce CV-ready material — even if they only say "make my CV fit this job", "is my CV ATS-friendly", "tailor my resume to this posting", "analyze this job ad for my CV", or simply paste a JD and a CV together. Also fires when the user mentions match score, keyword coverage, gap analysis, or a Drive/Word workflow that feeds job postings to AI tools. Defaults to Turkish output; switches language on request.
license: Proprietary. Built for Ahmet's analyst/job-search workflow.
---

# ATS CV Architect

## Ne işe yarar (core mantra)
Bir iş ilanını **çöz** (ANALİZ), adayın gerçek kariyer verisiyle **yeniden bağla** (SENTEZ), sonra **ölç ve doğrula** (SKOR + GAP). Tek bir ATS-uyumlu, ilana özel CV ve onun arkasındaki 6 yapılandırılmış veri alanını üretir. Bu skill, "önce çöz, sonra bağla, sonra kontrol et, gerekirse yeniden bağla" diyalektik döngüsünü iş ilanı → CV problemine uygular.

Bu skill yalnızca "anahtar kelime sayma" aracı değildir. Sentez katmanı (kanıta dayalı başarı cümleleri, dürüstlük kontrolü, anlatısal tutarlılık) en az analiz katmanı kadar önemlidir. İki katman da uygulanmadan iş bitmiş sayılmaz.

## Önce dürüst bir uyarı (taşınabilirlik)
Bu bir Claude skill'idir ve yalnızca Claude ekosisteminde (claude.ai, Claude Code, Cowork) çalışır. Kullanıcının iş akışı çok-araçlıdır (Gemini, ChatGPT, DeepSeek, GLM, Qwen, Mistral). **Diğer modeller bu .skill dosyasını çalıştıramaz.** Onlar için `assets/master-prompt-TR.md` içindeki taşınabilir Master Prompt'u kullan — aynı mantığı herhangi bir LLM'e kopyala-yapıştır ile taşır. İş akışını kurarken bu ayrımı kullanıcıya açıkça söyle.

## Girdiler
1. **İş ilanı (JD):** ham metin, yapıştırılmış pano, ya da Drive/Word/PDF dosyası.
2. **Framework/Master CV:** adayın tüm kariyerini içeren büyük belge (ör. 20 sayfa). Bu, sentez için "cevher ocağı"dır — çıktı CV'sindeki her iddia buradan gelmek zorundadır.
3. (Opsiyonel) **Corpus:** aynı sektörden 50–100 ilan; TF-IDF/BM25'in "nadir vs. sıradan kelime" ayrımı için kıyas kütlesi. Yoksa makul varsayımla ilerle ve bunu bir sınırlama olarak işaretle.

## Mod seçimi
Eldeki girdiye göre modu belirle ve başlamadan tek satırla bildir:
- **Tek ilan modu:** bir JD + Framework CV → bir ilana özel ATS CV. (En sık.)
- **Toplu mod (batch):** çok sayıda ilan → her biri için 6 veri alanı + skor; karşılaştırmalı bir tablo (hangi ilan adaya en uygun). Kullanıcının "100 ilan" / "data mining" / "Drive'a yüklüyorum" demesi bu moddur.
- **Sadece teşhis modu:** mevcut bir CV + bir JD → skor + gap analizi (yeni CV üretmeden). "CV'm ATS'e uygun mu" bu moddur.

## Protokol (Katman 0–5) — bu omurgadır, sırayla yürü

Her katmanın derin mekaniği referans dosyalarındadır. İlgili katmana gelmeden o dosyayı oku; hepsini baştan yükleme.

- **Katman 0 — Alım & Mod.** Tüm kaynakları sırala: JD nerede (yapıştırma / `/mnt/user-data/uploads` / Drive — Drive ise `tool_search` ile bağlan), Framework CV nerede, corpus var mı. Çıktı dilini sapta (varsayılan Türkçe). Modu seç ve bildir. **Provenans Defteri** başlat: çıktı CV'sine girecek her iddianın Framework CV'deki hangi girdiye dayandığını izleyen tablo. Bu, halüsinasyon/şişirme önleyici omurgadır (synthesis-analysis-research skill'indeki Source Registry'nin CV'ye uygulanmış hali). **Her CV maddesi bu deftere bağlanamıyorsa CV'ye giremez.**
- **Katman 1 — Bütünsel Kavrama (ön-sentez).** Ayrıştırmadan önce JD'yi bir bütün olarak oku: rolün özü ne, hangi tek cümle bu işi anlatır, görünür/gizli niyet ne (ör. "memur değil denetçi arıyorlar"). Kısa bir "rolün özü" notu yaz. Aynı şekilde Framework CV'yi bir bütün olarak tara.
- **Katman 2 — ANALİZ (çöz).** JD'yi ögelerine ayır: `references/jd-decomposition.md`'deki 7 katmanlı şemayı uygula (kimlik, zorunlu, tercih, sorumluluk/eylem, niyet/alt-metin, semantik/LSI, ağırlık metası). Terimleri çıkar, modality (zorunlu/tercih) ve konum ağırlığını ata, anlamlı n-gram'ları bütün olarak yakala.
- **Katman 3 — SKORLAMA & GAP.** Adayın mevcut malzemesini JD'ye karşı ölç: `references/scoring-formulas.md`'deki hibrit **ATS Match Score** ile (Lex/BM25 + Sem/kosinüs + Cov + Parse − Stuffing, denetim-düzeltmeli haliyle). Eksik zorunlu terimleri (gap) ve precision/recall/F1'i çıkar. Gap listesi sentez için talimattır.
- **Katman 4 — SENTEZ (yeniden bağla).** `references/synthesis-rules.md`'yi uygula: becerileri kümele, LSI/ontoloji ile (şişirmeden) genişlet, her deneyim maddesini XYZ/CAR formülüyle ve **yalnızca Framework CV'de kanıtı olan** içerikle yaz, üst özeti kur, parse-güvenli biçim kurallarına uy. Dürüstlük sınırı mutlaktır.
- **Katman 5 — Doğrulama & Teslim.** Provenans kontrolü yap (her madde Framework CV'ye bağlı mı), skoru yeniden hesapla, hedefe (%75–85) ulaşıldıysa ve *kapatılabilir* gap kalmadıysa dur. Sonra çıktıyı teslim et ve istenirse docx/pdf export'a (docx/pdf skill) devret.

## Revizyon döngüsü — sonlandırma kuralı (DİKKAT: yaygın hata)
`skor < hedef` İSE sentez katmanına dön, **yalnızca kapatılabilir gap'leri** (adayın Framework CV'sinde kanıtı olup henüz CV'ye yansımamış olanlar) tamamla, yeniden skorla. **`gap = boş` koşulunu sonlandırma şartı YAPMA.** Dürüst bir CV'de adayda olmayan zorunlu beceriler hep kalır → gap asla boşalmaz → sonsuz döngü olur. Doğru durma koşulu: `skor ≥ hedef VE kapatılabilir gap kalmadı`. Kalan (kapatılamaz) gap'ler dürüstçe kabul edilir, döngüye sokulmaz.

## Çıktı formatı — her ilan için 6 sabit alan
Her ilandan TAM OLARAK şu altı alanı üret (toplu modda her ilan bir satır olur). Şablon: `assets/output-fields-template.md`.

1. **keywords** — ağırlıklı liste: `{term, modality(must/nice), positional_weight, freq}`
2. **analysis** — gereksinim ayrıştırması + varlıklar (skill/araç/sertifika/kıdem/eğitim) + must/nice ayrımı + rolün niyeti
3. **summary** — rolün özü (1–2 cümle) + CV üst-özet taslağı (ilk 100–150 kelime ağırlıklı)
4. **synthesis** — semantik kümeler + LSI genişletmeler + XYZ/CAR başarı cümleleri (her biri Framework CV girdi-id'sine bağlı) + section_map
5. **match_score** — hibrit skor + bileşenler (Lex, Sem, Cov, Parse, Stuffing) + yorum (%75–85 hedef)
6. **gap_analysis** — kapatılabilir vs. kapatılamaz eksik zorunlu terimler + precision/recall/F1 + somut öneriler

## Kullanıcının Drive + çok-araçlı iş akışı (A.1–A.3 / B.1)
Kullanıcının somut akışını kurarken `references/workflow-drive-multitool.md`'yi oku. Özet ve kritik düzeltmeler:
- **A.1** JD'yi Drive'a Word olarak yükle. **Word içinde etiketli bölümler kullan:** `[JD-ORİJİNAL]`, `[ANALİZ]`, `[SENTEZ-ÖNERİ]`. Karıştırma.
- **A.2** JD'yi Gemini ile SEO analiz+sentez'den geçir, çıktıyı **`[SENTEZ-ÖNERİ]` bölümüne** ekle — asla JD-orijinalin içine değil. (Neden: enjekte edilen LSI/eşanlamlı terimler, adayda *olmayan* beceriler olabilir; bunları sonradan CV-yazıcı "adayın özelliği" sanmamalı.)
- **A.3** Master Prompt ile tüm gözlemleri stratejik yapıya oturt → 6 alan.
- **B.1** CV-yazıcı, Drive'dan JD verisini + Framework CV'yi alır, **yalnızca eşleşen ve kanıtı olan** bölümleri seçer, ATS CV yazar. Framework CV 20 sayfaysa: önce onu **etiketli kanıt bankasına** (her başarı bir girdi, beceri+metrik etiketli) çevir; her seferinde 20 sayfayı ham yapıştırma.

## Kalite ve etik korumaları (sert kurallar)
- **Provenans zorunlu.** Çıktı CV'sindeki her madde Framework CV'deki bir girdiye izlenebilmeli. İzlenemiyorsa madde çıkar veya işaretle. Bu, dürüstlüğün operasyonel garantisidir.
- **Dürüstlük mutlaktır.** Adayda olmayan beceri/anahtar kelime asla eklenmez. E-E-A-T'nin en önemli ayağı Trust'tır; sahte terim ATS'i geçse bile mülakatta çöker.
- **Coverage > density.** Kapsam ve kanıt birincildir; anahtar kelime yoğunluğu (density) birincil metrik değildir. Önemli her terim 2–3 kez, farklı bölümlerde (Beceriler'de iddia, Deneyim'de kanıt).
- **Aşırı optimizasyon geri teper.** Skor %90+ ise bu genelde şişirme işaretidir; hedef %75–85.
- **Parse güvenliği.** Tek sütun, standart başlıklar, tablo/grafik/metin kutusu yok, iletişim ana gövdede, .docx tercih. Akronimleri hem açık hem kısa ver ("Dış Ticaret (Foreign Trade)").
- **Skorun statüsü.** Hibrit skor, ATS'lerin (Workday/Greenhouse/iCIMS) gerçek iç formüllerinin *yaklaşıklamasıdır* (proxy), birebir kopyası değil — iç mekanizmalar tescillidir. Skoru mutlak gerçek değil, göreli pusula olarak sun.

## Tool eşlemesi (Claude-native)
- **JD/CV dosyaları:** uploads `/mnt/user-data/uploads`; metin/CSV `view`/`bash_tool`; PDF→**pdf** skill, Word→**docx** skill. Drive/Notion için önce `tool_search` ile connector yükle.
- **Gerçek matematik (Yol 2):** `scripts/ats_score.py` — TF-IDF/BM25/kosinüs/hibrit skoru deterministik hesaplar. LLM tahmini yerine gerçek sayı isteniyorsa bunu çalıştır.
- **Export:** docx/pdf skill (CV teslimi), xlsx skill (toplu mod karşılaştırma tablosu).
- **Görsel:** süreç/pipeline diyagramı gerekiyorsa Visualizer (SVG/HTML).

## Referans dosyaları
- `references/jd-decomposition.md` — ANALİZ şeması: bir JD hangi 7 parçaya ayrılır, modality ve ağırlıklandırma nasıl yapılır.
- `references/scoring-formulas.md` — tüm matematik: TF-IDF, BM25, kosinüs, hibrit ATS Match Score (denetim-düzeltmeli), P/R/F1, normalizasyon, çözümlü örnek.
- `references/synthesis-rules.md` — SENTEZ mekaniği: kümeleme, LSI genişletme, XYZ/CAR, E-E-A-T, anti-stuffing, parse kuralları, anlatı.
- `references/workflow-drive-multitool.md` — Drive + Gemini + çok-LLM iş akışının kurulumu ve denetimi.
- `assets/master-prompt-TR.md` — herhangi bir LLM'e taşınabilir Master Prompt (Gemini/ChatGPT/DeepSeek/GLM/Qwen/Mistral).
- `assets/output-fields-template.md` — 6 alanlık çıktı şablonu.

Protokolü her çalıştırmada kısa yol kullanmadan yürüt. Disiplinin kendisi üründür.


---



**━━━━━━━━━━ DOSYA 2/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/references/jd-decomposition.md`  
**Tür:** Referans  
**Açıklama:** ANALİZ şeması: bir iş ilanı hangi 7 parçaya ayrılır, modality ve ağırlıklandırma.


# JD Ayrıştırma Şeması (ANALİZ Katmanı)

Bir iş ilanını ATS-CV amacıyla **7 katmana** ayır. Bu, "düğümü çözme" adımıdır: ilanı anlamak için onu temel ögelerine, ilişkilerine ve gizli niyetine ayrıştırırsın. Sektör bağımsızdır — kimya, lojistik, yazılım fark etmez, iskelet aynıdır.

## İçindekiler
1. Kimlik katmanı
2. Zorunlu gereksinimler (must-have)
3. Tercih edilen gereksinimler (nice-to-have)
4. Sorumluluk / eylem katmanı
5. Niyet / alt-metin katmanı
6. Semantik / LSI katmanı
7. Ağırlık metası
+ Modality & konum ağırlığı kuralları
+ Çıktı şeması

---

## 1. Kimlik katmanı
İlanın "künyesi". Çıkar: **unvan, kıdem (junior/mid/senior/lead), sektör, lokasyon, şirket, çalışma biçimi (ofis/uzak/hibrit), dil gereksinimi.** Bunlar CV'nin üst kısmını ve standart unvan hizalamasını belirler. Kıdem, ileride tüm ağırlıkları kalibre eder (senior ilanında "5–7 yıl" zorunlu bir knockout olabilir).

## 2. Zorunlu gereksinimler (must-have) — omurga
"must / required / gerekli / şart / aranan nitelikler" başlıkları altındaki ve dilbilgisel olarak zorunluluk bildiren her şey. Türleri:
- **Sert beceriler / araçlar / teknolojiler** (Incoterms, SAP, REACH, Python, akreditif).
- **Sertifika / lisans** (CPA, PMP, B sınıfı ehliyet).
- **Deneyim yılı** ("5–7 yıl").
- **Eğitim** (lisans/yüksek lisans, alan).
- **Yasal / knockout** (çalışma izni, askerlik durumu, lokasyon) — bunlar ikili eler; sağlanmıyorsa skor ne olursa olsun otomatik ret.
Zorunlu bir terimi kaçırmak, on tercih terimi kaçırmaktan çok daha pahalıdır. Modality ağırlığı = **1.0**.

## 3. Tercih edilen gereksinimler (nice-to-have)
"preferred / plus / avantaj / tercihen / nice to have" altındakiler. CV'de yeri varsa eklenir ama kapsam hesabında düşük ağırlık taşır. Modality ağırlığı ≈ **0.3**.

## 4. Sorumluluk / eylem katmanı
İlanın "ne yapacaksın" kısmı — fiiller ve görevler ("denetler", "koordine eder", "raporlar", "optimize eder"). Bu katman CV'nin **başarı cümlelerine** (XYZ/CAR) hammadde verir: ilandaki eylem fiilini al, Framework CV'deki gerçek bir başarıyla eşleştir. Eylem fiillerini POS filtresiyle (yalnızca fiiller) ayıkla.

## 5. Niyet / alt-metin katmanı
İlanın açıkça yazmadığı ama ima ettiği şey — **rolün gerçek özü.** Örnek: "ithalat maliyetlerini raporlar + Finans birimiyle çalışır" ifadesi, ATS niyetinin "basit lojistik memuru değil, landed cost hesaplayan stratejik denetçi" olduğunu söyler. Bu katman, hangi anahtar kelimelerin gerçekten önemli olduğunu ve üst özetin hangi konumlandırmayı vurgulayacağını belirler. Niyeti tek cümleyle yaz: "Bu rol esasen ___ arıyor."

## 6. Semantik / LSI katmanı
Her zorunlu/önemli terim için **eşanlamlı ve akraba terim kümesi** çıkar (LSI = Latent Semantic Indexing mantığı): "supply chain ↔ tedarik zinciri ↔ lojistik ↔ operasyon". Kaynak: ESCO/O*NET ontolojisi veya embedding komşuluğu. **Kritik:** bu genişletme *eşleşmeyi anlamak* içindir (CV'de "müşteri sadakati" yazıyorsa JD'deki "user retention"ı yakalamak için), CV'ye terim *doldurmak* için DEĞİL. Genişletilmiş terimler ancak adayda gerçekten varsa CV'ye girer.

## 7. Ağırlık metası
Her terime üç sayı bağla:
- **modality** (1.0 zorunlu / ~0.3 tercih; bkz. graded varyant aşağıda),
- **positional_weight** (ilanın ilk 100–150 kelimesinde geçen terimler daha ağır; modern ATS "azalan ilgililik" mantığı kullanır),
- **freq** (ilanda kaç kez geçtiği; tekrar, gizli zorunluluk sinyalidir).
Bir terimin nihai analiz ağırlığı ≈ `bm25(term) × modality × positional_weight`.

---

## Modality & konum ağırlığı — kurallar

**Graded modality (denetim-iyileştirmesi; 2 değer yerine 3+):**
- `1.0` — açıkça zorunlu ("required/must/şart").
- `0.7` — güçlü ima / tekrarlı: "required" etiketi yok ama terim ≥2–3 kez geçiyor ya da sorumluluk katmanında merkezî. Saf 1.0/0.3 ikilisi bu gizli zorunlulukları kaçırır.
- `0.3` — açıkça tercih ("preferred/plus/avantaj").

**Konum ağırlığı:**
- İlk ~150 kelime / "aranan nitelikler"in ilk maddeleri: ×1.2–1.5.
- Orta gövde: ×1.0.
- "ek olarak / artı" kuyruğu: ×0.8.

---

## Çıktı şeması (bu katmanın ürünü)
```json
{
  "identity": {"title","seniority","sector","location","company","work_mode","language_req"},
  "must_have":  [{"term","type(skill|tool|cert|years|education|legal)","modality":1.0,"positional_weight","freq"}],
  "nice_to_have":[{"term","type","modality":0.3,"positional_weight","freq"}],
  "responsibilities":[{"action_verb","object"}],
  "intent":"Bu rol esasen ___ arıyor.",
  "lsi":{"<term>":["eşanlamlı1","akraba2"]},
  "knockouts":["çalışma izni","lokasyon", ...]
}
```
Bu obje, sentez katmanının ve skorlama katmanının doğrudan girdisidir.


---



**━━━━━━━━━━ DOSYA 3/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/references/scoring-formulas.md`  
**Tür:** Referans  
**Açıklama:** Tüm matematik: TF-IDF, BM25, kosinüs, hibrit ATS skoru (denetim-düzeltmeli), P/R/F1, çözümlü örnek.


# Skorlama Formülleri (SKOR Katmanı) — Denetim-Düzeltmeli

Tüm matematik burada. Bu skill, türetildiği özgün spesifikasyonun denetiminden geçti; bulunan hatalar **[DÜZELTME]** etiketiyle bu dosyada giderilmiştir, dolayısıyla buradaki formüller spesifikasyondakinden daha doğrudur.

## İçindekiler
1. TF-IDF
2. BM25 (Okapi)
3. Kosinüs benzerliği
4. Semantik katman (LSA/SVD, SBERT)
5. Hibrit ATS Match Score (düzeltilmiş)
6. Precision / Recall / F1 + gap
7. Normalizasyon
8. Çözümlü örnek
9. Ağırlık ayarı

---

## 1. TF-IDF (çekirdek 1)
```
tf(t,d)  = f(t,d) / Σ_t' f(t',d)
idf(t)   = log( N / df_t )           # yumuşatılmış: log( N / (1 + df_t) )
w(t,d)   = tf(t,d) × idf(t)
```
Terim ağırlığı belge-içi sıklıkla artar, corpus yaygınlığıyla azalır. N = corpus'taki ilan sayısı; df_t = terimi içeren ilan sayısı. "Kubernetes" yüksek, "team player" düşük ağırlık alır.

## 2. BM25 / Okapi BM25 (çekirdek 2)
```
BM25(D,Q) = Σ_i  IDF(q_i) ·  [ f(q_i,D) · (k1 + 1) ]
                            ─────────────────────────────────────────
                            [ f(q_i,D) + k1 · (1 − b + b · |D|/avgdl) ]
```
- **k1 (doyum):** TF katkısının doyma hızı; tipik **1.2–2.0** (varsayılan 1.5; Lucene 1.2). Doyum fonksiyonu, kelime doldurmayı matematiksel cezalandırır — tekrar arttıkça katkı asimptotik `k1+1`'e yaklaşır, sonsuza gitmez.
- **b (uzunluk normalizasyonu), 0–1:** varsayılan **0.75**. Aynı terimi 3 kez geçiren iki belgeden kısa olanı daha yüksek puanlar → öz CV ödüllenir.
- TF-IDF'ten üstün: doyum + uzunluk normalizasyonu. Elasticsearch/Lucene fiili standardı.

## 3. Kosinüs benzerliği (çekirdek 3)
```
cos(A,B) = (A · B) / (||A|| · ||B||) = Σ A_i B_i / ( sqrt(Σ A_i²) · sqrt(Σ B_i²) )
```
TF-IDF vektörlerinde [0,1]; embedding'de [−1,1]; 1 = özdeş yön. CV ile JD vektörleri arasındaki örtüşmeyi ölçer.

## 4. Semantik katman
**[DÜZELTME — tek çekirdek seç.]** Özgün spesifikasyon LSA/SVD ve SBERT'i paralel iki "çekirdek" olarak sunuyordu; bu, uygulayıcıyı ikisini birden kurmaya itebilir. Doğrusu:
- **Birincil: SBERT (Sentence-BERT).** Hazır çok dilli model; cümleyi 384/768-boyut vektöre gömer, kosinüsle karşılaştırılır. Eşanlamlı/parafraz yakalar ("müşteri sadakati" ↔ "user retention"). Çok dilli roller için domain'e ince-ayar idealdir.
- **İkincil/kavramsal ata: LSA/LSI + SVD.** `A = U Σ Vᵀ`, truncated SVD ile m terimden r latent kavrama indirger. Hafif, eski, doğrusal (doğrusal-olmayan örüntüleri kaçırır), büyük veride pahalı. SBERT yoksa hafif yedek olarak düşün; ana hat değil.

## 5. Hibrit ATS Match Score (düzeltilmiş)

### Bileşenler ([0,1]'e normalize)
```
Lex   = BM25(D_CV, Q_JD) / BM25_max(Q_JD)              # birebir kelime eşleşmesi
Sem   = max(0, cos( embed(CV), embed(JD) ))            # anlam eşleşmesi (madde düzeyinde max-over-chunks olabilir)
Cov   = Σ_{j∈M} w_j · 1[j ∈ CV] / Σ_{j∈M} w_j          # zorunlu terim kapsamı (w_j = modality × positional)
Parse = parse_checklist_score(CV)                       # biçim ayrıştırılabilirliği
Stuff = density_anomaly(CV, JD)                          # şişirme cezası [0,1]
```

### Birleşik skor — düzeltilmiş biçim
```
RAW   = α·Lex + β·Sem + γ·Cov − ζ·Stuff
Score = clamp( Parse_gate × RAW , 0 , 1 )
```
**[DÜZELTME 1 — alt sınır kıskaçlama.]** Özgün formül `α+β+γ+δ=1` ile pozitif kısmı [0,1]'de tutuyordu ama `−ζ·Stuff` skoru negatife itebiliyordu. `clamp(...,0,1)` eklendi.

**[DÜZELTME 2 — Parse çarpan/kapı, toplam değil.]** Özgün formül Parse'ı toplama eklerdi; oysa Parse *bu ilana uyum* değil, *genel ATS-okunabilirliği*dir (JD'den bağımsız). Bunu toplama katmak "işe uygunluk" ile "biçim sağlığı"nı karıştırır. Düzeltme: Parse'ı **kapı/çarpan** yap (ör. tablo/iki sütun varsa `Parse_gate ≈ 0.6`, temizse `1.0`). Böylece bozuk biçim tüm skoru orantılı düşürür, sahte yükseltmez.

**Önerilen ağırlıklar:** `α=0.35, β=0.30, γ=0.35` (toplam 1), `ζ=0.20` ceza, `Parse_gate ∈ [0.6, 1.0]`.

**[DÜZELTME 3 — Lex/Cov bağımlılığı.]** Lex (BM25) ve Cov ikisi de "terim var mı"yı ödüllendirir → bağımlıdırlar, bağımsızmış gibi toplanırsa kapsam fazla ağırlık alır. Bilinçli tasarım: Lex'i *tüm terimler üzerinden dağılımsal* benzerlik, Cov'u *yalnızca zorunlu terimlerin ikili* kapsamı olarak ayır ve ağırlıkları buna göre düşür (yukarıdaki α,γ bunu varsayar). Alternatif: Lex+Cov yerine tek bir "kapsam-ağırlıklı BM25" kullan.

**Alternatif füzyon — RRF (ölçek uyumsuzluğuna karşı):**
```
RRF(d) = Σ_s  1 / (k + rank_s(d))     # tipik k = 60
```
Lex ve Sem'i ham skor yerine *sıra* üzerinden birleştirir; ölçekleri farklıysa daha sağlamdır. Üretimde ilk ~20 adayı bir cross-encoder/LLM reranker ile yeniden sırala.

### Eşik yorumu
- **%75–85 = mülakata hazır** (hedef bant).
- **>%90 = aşırı optimizasyon / şişirme sinyali** — geri tepebilir.
- **<%50 = ciddi iyileştirme gerekir.**

## 6. Precision / Recall / F1 + gap
M = JD zorunlu terimleri, C = CV terimleri:
```
P  = |C ∩ M| / |C|          # CV terimlerinin ne kadarı ilgili (düşük = alakasız/şişirme)
R  = |C ∩ M| / |M|          # zorunluların ne kadarı kapsandı (eksik must-have = gap → R düşer)
F1 = 2PR / (P + R)
gap = M \ C                  # eksik zorunlu terimler
```
**[DÜZELTME 4 — gap'i ikiye ayır.]** `gap_kapatılabilir` = aday Framework CV'sinde kanıtı var ama CV'ye yansımamış (→ sentez döngüsüne gider). `gap_kapatılamaz` = adayda gerçekten yok (→ dürüstçe kabul edilir, döngüye SOKULMAZ). Revizyon döngüsü yalnızca kapatılabilir gap üzerinde döner; aksi halde sonsuz döngü olur.

## 7. Normalizasyon
```
min-max:  x' = (x − min) / (max − min)        # [0,1]'e
z-score:  z  = (x − μ) / σ                     # aday havuzunda göreli sıralama
```
Bileşenleri toplamadan önce hepsini aynı ölçeğe getir; yoksa elma+armut toplarsın.

## 8. Çözümlü örnek
10 zorunlu terim; `Lex=0.74, Sem=0.69, Cov=0.82, Stuff=0.10, Parse_gate=1.0` (temiz biçim):
```
RAW   = 0.35·0.74 + 0.30·0.69 + 0.35·0.82 − 0.20·0.10
      = 0.2590 + 0.2070 + 0.2870 − 0.0200 = 0.7330
Score = clamp(1.0 × 0.7330, 0, 1) = 0.733 ≈ %73  →  hedefin hemen altında, sentez turu önerilir
```
Aynı CV iki sütunlu/tablolu olsaydı `Parse_gate=0.6` → `Score≈0.44` — biçim hatasının skoru nasıl orantılı çökerttiğine dikkat. (Özgün spesifikasyondaki örnek Parse'ı toplama eklediği için ~%77 çıkıyordu; düzeltilmiş kapı-modeli daha gerçekçidir.)

## 9. Ağırlık ayarı
- **Kalibrasyon:** geri-çağrı (callback) verisi varsa `(α,β,γ,ζ)` ve `(k1,b)`'yi grid-search ile nDCG@k / F1 maksimize edecek şekilde ayarla.
- **Dinamik α:** nadir-terimli (çok teknik) JD'lerde lexical ağırlığı (α) yükselt.
- **Sektör/dil:** çok dilli, çapraz-terminolojili rollerde semantik ağırlığı (β) ve ontoloji genişletmesini güçlendir.
- Önerilen defaultlar başlangıç noktasıdır, evrensel-optimal değildir.


---



**━━━━━━━━━━ DOSYA 4/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/references/synthesis-rules.md`  
**Tür:** Referans  
**Açıklama:** SENTEZ mekaniği: kümeleme, LSI genişletme, XYZ/CAR, E-E-A-T, anti-stuffing, parse, provenans.


# Sentez Kuralları (SENTEZ Katmanı) — "Düğümü Bağlama"

Analizden çıkan dağınık, ağırlıklı parçaları alıp ilana özel, güçlü, dürüst bir CV'ye dokuma katmanı. Sentez en az analiz kadar titizlik ister: amaç parçaları yan yana dizmek değil, parçaların toplamından *fazla* bir bütün (rolün özüne tam oturan bir anlatı) üretmektir.

## İçindekiler
1. Semantik kümeleme
2. LSI / ontoloji genişletme (şişirmesiz)
3. Başarı cümlesi formülleri (XYZ / CAR / STAR)
4. E-E-A-T ve dürüstlük
5. Üst özet ve anlatısal tutarlılık
6. Parse-güvenli biçim kuralları
7. Provenans kontrolü (çıkıştan önce zorunlu)

---

## 1. Semantik kümeleme
Analizden gelen anahtar kelimeleri anlamlı gruplara topla (embedding üzerinde k-means/hiyerarşik, ya da elle): ör. **"Dış Ticaret Operasyonları: Incoterms, akreditif, gümrük mevzuatı, GTIP."** Kümeler hem ATS'in "Beceriler" bölümünü düzgün ayrıştırmasını sağlar hem insan gözüne düzen verir. İsteğe bağlı: LDA ile JD'nin gizli temalarını çıkarıp CV alt-başlıklarına eşle.

## 2. LSI / ontoloji genişletme — ŞİŞİRMESİZ
ESCO/O*NET veya embedding komşuluğundan kontrollü eşanlamlı/akraba terim getir. **Sert kısıt:** tekrar değil, *varyasyonla semantik derinlik*. Aynı bağlam penceresine üç kez tıkmak yerine, önemli bir terimi 2–3 kez **farklı bölümlerde** geçir — bir kez "Beceriler"de iddia, bir kez "Deneyim"de kanıt olarak. **Yoğunluk:** ~1–3% birincil terim normaldir; >%5 şişirmedir. Ama en güçlü modern kaynakların ortak hükmü: *density yanlış birincil metriktir; coverage + proof doğrudur.* Pratik hedef: 15–25 ilgili terim, metne dağıtılmış. **Genişletilmiş hiçbir terim, aday onu gerçekten karşılamıyorsa CV'ye giremez.**

## 3. Başarı cümlesi formülleri — sentezin can damarı
**Google XYZ (Laszlo Bock):** "Accomplished **[X]** as measured by **[Y]**, by doing **[Z]**" → "[Z yöntemiyle] yaparak, [Y ölçüsüyle ölçülen] [X sonucunu] başardım."
- Örnek: "Gümrük müşavirlik süreçlerini KPI'larla denetleyerek (Z), gümrükleme süresini %30 kısalttım (X, ölçü Y)."
- Sihir: JD'nin eylem katmanından bir fiil + Framework CV'den gerçek bir başarı + bir sayı. Böylece anahtar kelime "iddia" olmaktan çıkıp "kanıt" olur.

**CAR (Context–Action–Result)** ve **STAR (Situation–Task–Action–Result):** CAR kısa CV maddesi için, STAR mülakat anlatısı için. Her ikisi de sonuç-odaklıdır.

**Niceleme (zorunlu):** her başarı cümlesinde ≥1 sayı. "Önemli ölçüde artırdım" değil, "%45 artırdım". Madde uzunluğu ≤1–2 satır. Cümle başına güçlü eylem fiili (yönetti/kurdu/optimize etti/müzakere etti/azalttı).

## 4. E-E-A-T ve dürüstlük
Google'ın E-E-A-T çerçevesi (rater kılavuzu; doğrudan sıralama faktörü değil ama kalite pusulası):
- **Experience** — birinci elden gerçek deneyim.
- **Expertise** — kanıtlanabilir bilgi/sertifika.
- **Authoritativeness** — tanınma, liderlik kapsamı.
- **Trustworthiness** — **en önemli ayak.** Google: "güvenilmez sayfalar ne kadar Deneyimli/Uzman/Otoriter görünse de düşük E-E-A-T'ye sahiptir."
CV'de Trust = doğruluk, abartısızlık, savunulabilir metrikler. **Sahte beceri/anahtar kelime yok** — ATS'i geçse bile mülakatta çöker. Bu, skill'in mutlak sınırıdır.

## 5. Üst özet ve anlatısal tutarlılık
- **Üst özet:** CV'nin ilk 3–5 cümlesi (en yüksek konum ağırlıklı bölge) rolün özünü + en kritik zorunlu anahtar kelimeleri yansıtmalı (ilk 100–150 kelime ATS'te yüksek ağırlık taşır).
- **Tutarlılık:** CV ↔ LinkedIn ↔ kapak mektubu aynı standart unvanları kullanmalı; dahili/yaratıcı unvanları sektör-standardına çevir.
- **"Robot + insan" testi:** çıktı hem anahtar kelime skorunu geçmeli HEM 6 saniyede taranıp değer iletmeli. Biri olmadan diğeri yetmez.

## 6. Parse-güvenli biçim kuralları
- **Dosya:** .docx en güvenilir; modern ATS metin-PDF de okur; format belirsizse .docx. Görüntü/taranmış PDF'ten kaçın.
- **Düzen:** tek sütun; standart başlıklar (Özet, Deneyim, Beceriler, Eğitim, Sertifikalar); **tablo/grafik/metin kutusu/header-footer'da kritik bilgi yok**; iletişim ana gövdede.
- **Kronoloji:** ters kronolojik veya hibrit.
- **Akronim:** hem açık hem kısa — "Dış Ticaret (Foreign Trade)", "Arama Motoru Optimizasyonu (SEO)".

## 7. Provenans kontrolü — çıkıştan ÖNCE zorunlu
Teslimden önce her CV maddesini Framework CV'deki bir girdiye (id) bağla. **Eşlenemeyen madde = uydurma riski → çıkar veya işaretle.** Bu, dürüstlüğün operasyonel garantisidir; synthesis-analysis-research skill'indeki "Source Registry"nin CV'ye uygulanmış halidir. Çıktıya kısa bir provenans tablosu ekle:

```
| CV maddesi | Framework CV girdi-id | JD'de karşılığı | durum |
|------------|------------------------|------------------|-------|
| "...%30 kısalttım" | EXP-07 | "gümrükleme/KPI" | doğrulandı |
```

Madde bu tabloya giremiyorsa CV'ye de giremez.


---



**━━━━━━━━━━ DOSYA 5/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/references/workflow-drive-multitool.md`  
**Tür:** Referans  
**Açıklama:** Drive + Gemini + çok-LLM iş akışının kurulumu ve denetimi (A.1-A.3 / B.1).


# Drive + Çok-LLM İş Akışı (A.1–A.3 / B.1) — Kurulum ve Denetim

Kullanıcının somut akışı: iş ilanını Drive'a Word olarak koy, Gemini ile SEO analiz+sentez geçir, Master Prompt ile stratejik yapıya oturt, sonra (Claude/ChatGPT/DeepSeek/GLM/Qwen/Mistral'dan biriyle) Drive'dan veri çekip Framework CV ile eşleştirerek ATS CV yazdır. Bu dosya akışı adım adım kurar ve denetimde bulunan riskleri düzeltir.

## Akış (düzeltilmiş)

### A.1 — JD'yi Drive'a Word olarak yükle, ETİKETLİ
Word belgesini üç etiketli bölümle aç:
```
[JD-ORİJİNAL]      ← ilanın ham, değiştirilmemiş metni. Asla kirletme.
[ANALİZ]           ← 7 katmanlı ayrıştırma çıktısı (jd-decomposition.md)
[SENTEZ-ÖNERİ]     ← Gemini'nin SEO genişletmeleri, LSI terimleri, öneriler
```
**[DENETİM-DÜZELTME C2 — kirlenme riski.]** JD'yi ve Gemini'nin SEO çıktısını aynı bölüme karıştırma. Enjekte edilen LSI/eşanlamlı terimler adayda *olmayan* beceriler olabilir; karışırsa CV-yazıcı bunları sonradan "JD gerçeği" veya "aday özelliği" sanır → şişirme + dürüstlük ihlali. Etiketli bölümler bunu önler.

### A.2 — Gemini ile SEO analiz + sentez
Gemini'ye `assets/master-prompt-TR.md`'nin ANALİZ+SENTEZ kısmını ver; çıktıyı **yalnızca `[SENTEZ-ÖNERİ]` bölümüne** yapıştır. Gemini'ye açıkça söyle: ürettiğin genişletilmiş terimler *aday-tarafı hedeflerdir; yalnızca aday gerçekten karşılıyorsa kullanılacaktır*, JD hakkında ya da aday hakkında olgu değildir.

### A.3 — Master Prompt ile stratejik yapı
Tüm gözlemleri (A.1 + A.2) Master Prompt'un tamamına ver → 6 sabit alan (`output-fields-template.md`): keywords, analysis, summary, synthesis, match_score, gap_analysis. Bunları Word'e ya da bağlı bir tabloya yaz.

### B.1 — ATS CV yazdırma
CV-yazıcı LLM:
1. Drive'dan JD verisini (6 alan) + Framework CV'yi çeker.
2. **Framework CV'yi etiketli kanıt bankası olarak okur** (aşağı bak).
3. JD'nin zorunlu+önemli terimleriyle **eşleşen ve kanıtı olan** girdileri seçer.
4. synthesis-rules.md kurallarıyla ATS CV'yi yazar.
5. scoring-formulas.md ile skoru + gap'i hesaplar, hedefe ulaşana dek (kapatılabilir gap üzerinde) revize eder.
6. Provenans kontrolünü geçirip teslim eder.

## Framework CV → Kanıt Bankası dönüşümü
**[DENETİM-DÜZELTME C3 — 20 sayfa ham yapıştırma kötüdür.]** 20 sayfalık CV'yi her seferinde ham vermek bağlamı boğar ve eşleşmeyi gürültüyle zayıflatır. Bir kez şu yapıya çevir: **her başarı = bir girdi**, etiketli:
```
EXP-07 | Dış Ticaret | beceriler: [gümrükleme, KPI denetimi, landed cost] | metrik: süre −%30 | dönem: 2019–2022 | kanıt-cümlesi: "..."
```
CV-yazıcı her ilanda 20 sayfa yerine yalnızca eşleşen girdileri (ör. EXP-07, EXP-12, SKILL-03) çeker. Bu, "Master CV = cevher ocağı" fikrinin uygulanabilir halidir.

## Araç eşlemesi (hangi iş hangi modelde)
- **ANALİZ (ayrıştırma, ağırlık):** herhangi bir güçlü LLM; gerçek BM25/kosinüs sayısı isteniyorsa Claude + `scripts/ats_score.py`.
- **SENTEZ (cümle yazımı, kümeleme):** Claude/GPT/Gemini — yaratıcı-akıl katmanı.
- **Skor/gerçek matematik:** kod (scripts/ats_score.py). LLM "tahmini skor" verir; tutarlılık için koda taşı.
- **Otomasyon:** n8n — Drive tetikleyici → model çağrısı → 6 alanı tabloya yaz → Telegram/Slack bildirimi.

## Taşınabilirlik uyarısı (tekrar)
**[DENETİM-DÜZELTME C1.]** Bu .skill yalnızca Claude'da çalışır. Gemini/ChatGPT/DeepSeek/GLM/Qwen/Mistral için `assets/master-prompt-TR.md`'yi kullan — aynı mantığı taşınabilir prompt olarak taşır. Çok-araçlı akışın bel kemiği bu prompttur, skill değil.

## Toplu mod (100 ilan / data mining)
Her ilan bir satır olacak şekilde bir Google Sheet/Notion tablosu kur; sütunlar = 6 alan + final skor. n8n akışı her yeni ilanda pipeline'ı çalıştırıp satırı doldurur. Sonra skora göre sırala → "bana en uygun ilanlar" listesi. İstenirse xlsx skill ile karşılaştırma tablosu/grafiği üret.


---



**━━━━━━━━━━ DOSYA 6/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/assets/master-prompt-TR.md`  
**Tür:** Varlık  
**Açıklama:** Herhangi bir LLM'e taşınabilir Master Prompt (Gemini/ChatGPT/DeepSeek/GLM/Qwen/Mistral).


# MASTER PROMPT — ATS CV (Taşınabilir / Herhangi Bir LLM)

> Bunu Gemini, ChatGPT, DeepSeek, GLM, Qwen, Mistral veya Claude'a olduğu gibi kopyala. `<<< >>>` arasını doldur. Çıktı dili: Türkçe (aksi belirtilmedikçe).

---

## SİSTEM / ROL
Sen kıdemli bir ATS-CV mimarısın. Görevin: bir iş ilanını **ANALİZ** edip (parçalara ayır), adayın gerçek kariyer verisiyle **SENTEZ** edip (yeniden bağla) ATS-uyumlu, ilana özel bir CV ve onun 6 yapılandırılmış veri alanını üretmek. Diyalektik döngü: **önce çöz → bağla → ölç → gerekirse yeniden bağla.**

**Mutlak kurallar:**
1. **Dürüstlük:** Adayda olmayan hiçbir beceri/anahtar kelime eklenmez. Çıktı CV'sindeki HER madde, aşağıdaki Framework CV'de kanıtı olan bir şeye dayanmalıdır. Kanıtı yoksa o madde yazılmaz.
2. **Coverage > density:** Anahtar kelime doldurma yapma. Önemli terimi 2–3 kez, farklı bölümlerde (Beceriler'de iddia, Deneyim'de kanıt) geçir. Hedef skor %75–85; %90+ şişirme demektir, ondan kaçın.
3. **Parse güvenliği:** Tek sütun, standart başlıklar, tablo/grafik yok, iletişim ana gövdede.

## GİRDİLER
```
[İŞ İLANI]
<<< ilanın tam metnini buraya yapıştır >>>

[FRAMEWORK CV — kariyer kanıt bankası]
<<< adayın tüm kariyerini içeren CV; mümkünse her başarı bir satır,
    beceri + metrik etiketli. Örn: EXP-07 | Dış Ticaret | [gümrükleme, KPI] | süre −%30 >>>

[HEDEF DİL] = Türkçe
[HEDEF SKOR] = %75–85
```

---

## ADIM 1 — ANALİZ (iş ilanını 7 parçaya ayır)
İlanı şu 7 katmana çöz:
1. **Kimlik:** unvan, kıdem, sektör, lokasyon, şirket, çalışma biçimi, dil.
2. **Zorunlu (must-have):** sert beceri/araç, sertifika, deneyim yılı, eğitim, yasal/knockout. (ağırlık 1.0)
3. **Tercih (nice-to-have):** "preferred/plus/avantaj" olanlar. (ağırlık 0.3)
4. **Sorumluluk/eylem:** "ne yapacaksın" fiilleri (denetler, koordine eder, raporlar...).
5. **Niyet/alt-metin:** "Bu rol esasen ___ arıyor." (ör. memur değil denetçi)
6. **Semantik/LSI:** her önemli terimin eşanlamlı/akraba kümesi (yalnızca eşleşmeyi anlamak için).
7. **Ağırlık metası:** her terime modality (1.0/0.7/0.3) + konum ağırlığı (ilk 150 kelime ağır) + sıklık.

## ADIM 2 — SKOR & GAP (adayın mevcut hali ne kadar uyuyor)
Framework CV'yi JD'ye karşı değerlendir:
- **Lex** (birebir kelime eşleşmesi), **Sem** (anlam eşleşmesi), **Cov** (zorunlu terimlerin yüzde kaçı kanıtlı şekilde mevcut).
- **Hibrit skor** ≈ `0.35·Lex + 0.30·Sem + 0.35·Cov − 0.20·Şişirme`, biçim bozuksa orantılı düşür, 0–1'e kıskaçla.
- **Gap'i ikiye ayır:** *kapatılabilir* (adayda kanıtı var ama CV'ye yansımamış) ve *kapatılamaz* (adayda gerçekten yok). Yalnızca kapatılabilir gap üzerinde çalış.
- precision / recall / F1 ver.
(LLM olarak sayıları tahmin ediyorsun; gerçek hesap için kullanıcı kodu çalıştırabilir.)

## ADIM 3 — SENTEZ (ilana özel CV'yi yeniden bağla)
- Becerileri anlamlı kümelere topla.
- Her deneyim maddesini **XYZ** formülüyle yaz: "[Z yöntemiyle] yaparak, [Y ölçüsüyle ölçülen] [X sonucunu] başardım." Her cümlede ≥1 sayı, başında güçlü fiil.
- Her maddeyi bir Framework CV girdi-id'sine bağla (provenans).
- Üst özet (ilk 3–5 cümle): rolün özü + en kritik zorunlu terimler.
- Kapatılabilir gap'leri (yalnızca kanıtı olanlarla) doldur, yeniden değerlendir.

## ADIM 4 — DOĞRULAMA
Teslimden önce: her CV maddesi Framework CV'ye bağlı mı? Bağlı değilse çıkar. Skor hedefte mi? Biçim parse-güvenli mi?

---

## ÇIKTI — TAM OLARAK ŞU 6 ALAN + CV
Sırayla ver:

### 1) keywords
Ağırlıklı terim listesi: `terim — modality(zorunlu/tercih) — konum ağırlığı — sıklık`.

### 2) analysis
7 katmanlı ayrıştırma özeti + zorunlu/tercih ayrımı + rolün niyeti (tek cümle).

### 3) summary
Rolün özü (1–2 cümle) + CV üst-özet taslağı (ilk 100–150 kelime).

### 4) synthesis
Semantik kümeler + LSI genişletmeler + XYZ başarı cümleleri (her biri girdi-id'li) + bölüm haritası (Özet/Deneyim/Beceriler/Eğitim/Sertifikalar).

### 5) match_score
Hibrit skor + bileşenler (Lex, Sem, Cov, biçim, şişirme) + yorum (hedef %75–85).

### 6) gap_analysis
Kapatılabilir vs. kapatılamaz eksik zorunlu terimler + precision/recall/F1 + somut öneriler.

### + FINAL CV
Yukarıdakilerin sentezi: tek sütun, parse-güvenli, dürüst, ilana hizalı ATS CV. Sonuna kısa **provenans tablosu** ekle (CV maddesi → Framework girdi-id → JD karşılığı).

---

### Notlar
- Çok-araçlı akışta: ANALİZ+SENTEZ kısmını Gemini'de çalıştırıp çıktıyı Word'ün `[SENTEZ-ÖNERİ]` bölümüne koyabilirsin; FINAL CV'yi ayrı bir modelde Framework CV ile yazdırabilirsin.
- Genişletilmiş/önerilen terimler **aday-tarafı hedeflerdir**; yalnızca aday gerçekten karşılıyorsa CV'ye girer.


---



**━━━━━━━━━━ DOSYA 7/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/assets/output-fields-template.md`  
**Tür:** Varlık  
**Açıklama:** 6 alanlık çıktı şablonu (JSON + markdown).


# Çıktı Şablonu — 6 Sabit Alan (her ilan için)

Her iş ilanı bu altı alanı üretir. Toplu modda her ilan tabloda bir satır olur; tek-ilan modunda tam form + FINAL CV verilir.

```json
{
  "ilan_id": "JD-001",
  "keywords": [
    {"term": "akreditif (letter of credit)", "modality": "zorunlu", "positional_weight": 1.3, "freq": 2}
  ],
  "analysis": {
    "identity": {"title": "", "seniority": "", "sector": "", "location": "", "company": "", "work_mode": "", "language_req": ""},
    "must_have": [{"term": "", "type": "skill|tool|cert|years|education|legal", "modality": 1.0}],
    "nice_to_have": [{"term": "", "type": "", "modality": 0.3}],
    "responsibilities": [{"action_verb": "", "object": ""}],
    "knockouts": [],
    "intent": "Bu rol esasen ___ arıyor."
  },
  "summary": {
    "role_essence": "1-2 cümle",
    "cv_top_summary_draft": "ilk 100-150 kelime, en kritik zorunlu terimler + konumlandırma"
  },
  "synthesis": {
    "semantic_clusters": [{"cluster_label": "", "member_skills": []}],
    "lsi_expansions": {"<term>": ["varyant1", "varyant2"]},
    "achievement_bullets": [
      {"verb": "", "X_result": "", "Y_metric": "", "Z_method": "", "framework_cv_id": "EXP-07"}
    ],
    "section_map": ["Özet", "Deneyim", "Beceriler", "Eğitim", "Sertifikalar"]
  },
  "match_score": {
    "score_percent": 0,
    "components": {"Lex": 0.0, "Sem": 0.0, "Cov": 0.0, "Parse_gate": 1.0, "Stuffing": 0.0},
    "interpretation": "hedef %75-85; >%90 şişirme; <%50 ciddi iyileştirme"
  },
  "gap_analysis": {
    "closable_gaps": [],
    "uncloseable_gaps": [],
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0,
    "recommendations": []
  },
  "provenance_check": [
    {"cv_bullet": "", "framework_cv_id": "", "jd_match": "", "status": "doğrulandı|işaretli"}
  ]
}
```

## Markdown (insan-okur) varyant
Aynı altı alanı başlıklarla ver:
```
## 1. keywords        (ağırlıklı liste)
## 2. analysis        (7 katman + niyet)
## 3. summary         (rolün özü + üst-özet taslağı)
## 4. synthesis       (kümeler + LSI + XYZ cümleleri + bölüm haritası)
## 5. match_score     (skor + bileşenler + yorum)
## 6. gap_analysis    (kapatılabilir/kapatılamaz + P/R/F1 + öneriler)
## + FINAL CV         (+ provenans tablosu)
```


---



**━━━━━━━━━━ DOSYA 8/8 ━━━━━━━━━━**

**Yol:** `ats-cv-architect/scripts/ats_score.py`  
**Tür:** Betik (Python)  
**Açıklama:** Deterministik TF-IDF/BM25/kosinüs/hibrit skorlayıcı (Yol 2 çekirdeği).


```python
#!/usr/bin/env python3
"""
ats_score.py — ATS CV Architect skorlama çekirdeği (Yol 2).

Bir iş ilanı (JD) ile bir CV arasındaki hibrit ATS Match Score'unu DETERMINISTIK
olarak hesaplar. LLM "tahmini skor" yerine gerçek sayı üretir.

Hesaplananlar:
  - TF-IDF kosinüs benzerliği
  - BM25 (Okapi) bazlı lexical eşleşme  (Lex)
  - Zorunlu terim kapsamı               (Cov)   [graded modality destekli]
  - Şişirme (keyword stuffing) cezası   (Stuff)
  - (opsiyonel) SBERT semantik benzerlik (Sem)  [sentence-transformers varsa]
  - Hibrit skor (denetim-düzeltmeli: parse KAPI olarak, 0-1'e kıskaçlı)
  - precision / recall / F1 + gap (kapatılabilir/kapatılamaz ayrımı çağıran tarafa)

Bağımlılık: yalnızca standart kütüphane zorunlu. numpy/scikit-learn/sentence-transformers
varsa kullanılır; yoksa saf-python yedeğe düşer.

Kullanım:
  python ats_score.py --jd jd.txt --cv cv.txt \
      --must "akreditif,incoterms,gtip,landed cost,kpi" \
      --corpus corpus_dir/   # opsiyonel; yoksa sadece JD+CV ile idf kabası

  # ya da modül olarak:
  from ats_score import ats_match_score
"""

import argparse
import math
import os
import re
from collections import Counter

# ----------------------------- metin işleme -----------------------------

_TOKEN = re.compile(r"[a-zA-ZçÇğĞıİöÖşŞüÜ0-9]+")

# küçük çok-dilli stop-word seti (genişletilebilir)
STOP = set("""
ve veya ile için bir bu şu da de ki mi mu çok daha en gibi olarak the a an and or for to of in on with as is are be by at from that this
""".split())


def tokenize(text, ngram_max=3):
    """küçük harf + token + 1..n gram. Çok kelimeli kavramları (n-gram) bütün yakalar."""
    words = [w.lower() for w in _TOKEN.findall(text or "")]
    words = [w for w in words if w not in STOP]
    grams = list(words)
    for n in range(2, ngram_max + 1):
        for i in range(len(words) - n + 1):
            grams.append(" ".join(words[i:i + n]))
    return grams


# ----------------------------- BM25 -----------------------------

class BM25:
    """Okapi BM25. corpus = list[list[token]]."""

    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.corpus = corpus
        self.N = len(corpus)
        self.avgdl = sum(len(d) for d in corpus) / max(1, self.N)
        self.df = Counter()
        for d in corpus:
            for t in set(d):
                self.df[t] += 1
        self.tf = [Counter(d) for d in corpus]

    def idf(self, term):
        # yumuşatılmış idf (negatif olmaz)
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query_tokens, doc_index):
        tf = self.tf[doc_index]
        dl = len(self.corpus[doc_index])
        s = 0.0
        for q in set(query_tokens):
            f = tf.get(q, 0)
            if f == 0:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += self.idf(q) * (f * (self.k1 + 1)) / denom
        return s

    def max_self_score(self, query_tokens):
        """Q'nun kendisini belge sayarak alabileceği teorik tavan (normalizasyon için)."""
        q = list(query_tokens)
        tmp = BM25([q], k1=self.k1, b=self.b)
        # idf'leri ana corpustan al ki ölçek tutarlı olsun
        tmp.idf = self.idf  # type: ignore
        return tmp.score(q, 0)


# ----------------------------- TF-IDF kosinüs -----------------------------

def tfidf_cosine(jd_tokens, cv_tokens, idf_fn):
    def vec(tokens):
        tf = Counter(tokens)
        return {t: (c / len(tokens)) * idf_fn(t) for t, c in tf.items()} if tokens else {}
    a, b = vec(jd_tokens), vec(cv_tokens)
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


# ----------------------------- semantik (opsiyonel) -----------------------------

def sbert_cosine(jd_text, cv_text):
    """sentence-transformers varsa SBERT kosinüsü; yoksa None döner."""
    try:
        from sentence_transformers import SentenceTransformer, util  # type: ignore
    except Exception:
        return None
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    emb = model.encode([jd_text, cv_text], convert_to_tensor=True, normalize_embeddings=True)
    return float(util.cos_sim(emb[0], emb[1]).item())


# ----------------------------- kapsam & şişirme -----------------------------

def coverage(must_have, cv_tokens, weights=None):
    """
    must_have: list[str]  (zorunlu terimler; çok kelimeli olabilir)
    weights:   dict term->float (modality*positional). Yoksa hepsi 1.0.
    CV'de geçen zorunlu terimlerin ağırlıklı oranı + gap listesi.
    """
    cv_set = set(cv_tokens)
    cv_text = " ".join(cv_tokens)
    weights = weights or {}
    num = den = 0.0
    gap = []
    for term in must_have:
        t = term.lower().strip()
        w = weights.get(t, 1.0)
        den += w
        present = (t in cv_set) or (t in cv_text)
        if present:
            num += w
        else:
            gap.append(term)
    cov = num / den if den else 0.0
    return cov, gap


def stuffing_penalty(cv_tokens, max_density=0.05):
    """En sık içerik teriminin yoğunluğu eşiği aşarsa orantılı ceza [0,1]."""
    if not cv_tokens:
        return 0.0
    c = Counter(cv_tokens)
    top, freq = c.most_common(1)[0]
    density = freq / len(cv_tokens)
    if density <= max_density:
        return 0.0
    return min(1.0, (density - max_density) / max_density)


# ----------------------------- precision / recall / f1 -----------------------------

def prf(cv_tokens, must_have):
    cv_set = set(cv_tokens)
    cv_text = " ".join(cv_tokens)
    M = set(m.lower().strip() for m in must_have)
    hit = set(m for m in M if (m in cv_set) or (m in cv_text))
    # precision: CV terimlerinin ne kadarı M ile ilgili (kaba: hit / benzersiz cv terim örtüşmesi)
    P = len(hit) / max(1, len(cv_set & M)) if (cv_set & M) else (len(hit) / max(1, len(M)))
    R = len(hit) / max(1, len(M))
    F1 = (2 * P * R / (P + R)) if (P + R) else 0.0
    return round(P, 3), round(R, 3), round(F1, 3)


# ----------------------------- hibrit skor -----------------------------

def ats_match_score(jd_text, cv_text, must_have, corpus_texts=None,
                    weights=None, parse_gate=1.0,
                    alpha=0.35, beta=0.30, gamma=0.35, zeta=0.20,
                    k1=1.5, b=0.75, use_sbert=True):
    """
    Denetim-düzeltmeli hibrit ATS Match Score.
      RAW   = alpha*Lex + beta*Sem + gamma*Cov - zeta*Stuff
      Score = clamp(parse_gate * RAW, 0, 1)
    Sem yoksa (SBERT yok) beta ağırlığı alpha+gamma'ya orantılı dağıtılır.
    """
    jd_tok = tokenize(jd_text)
    cv_tok = tokenize(cv_text)

    docs = [jd_tok, cv_tok]
    if corpus_texts:
        docs += [tokenize(t) for t in corpus_texts]
    bm = BM25(docs, k1=k1, b=b)

    # Lex: JD ile CV arasında TF-IDF KOSINÜS benzerliği (unigram) — standart, doğal [0,1].
    # NOT: idf gerçek bir corpus ister; corpus YOKSA (sadece JD+CV) idf dejenere olur ve
    # Lex muhafazakâr/düşük çıkar. Bu durumda skoru MUTLAK değil GÖRELİ oku (güçlü vs zayıf
    # ayrımı geçerlidir). Gerçek kalibrasyon için 50-100 ilanlık corpus + SBERT (Sem) gerekir.
    jd_uni, cv_uni = tokenize(jd_text, ngram_max=1), tokenize(cv_text, ngram_max=1)
    Lex = max(0.0, min(1.0, tfidf_cosine(jd_uni, cv_uni, bm.idf)))

    # Sem
    Sem = sbert_cosine(jd_text, cv_text) if use_sbert else None
    if Sem is not None:
        Sem = max(0.0, Sem)

    # Cov
    Cov, gap = coverage(must_have, cv_tok, weights)

    # Stuffing
    Stuff = stuffing_penalty(cv_tok)

    # ağırlıklar (Sem yoksa beta'yı yeniden dağıt)
    a, bb, g = alpha, beta, gamma
    if Sem is None:
        total = a + g
        a, g = a / total, g / total
        bb = 0.0
        sem_term = 0.0
    else:
        sem_term = bb * Sem

    RAW = a * Lex + sem_term + g * Cov - zeta * Stuff
    Score = max(0.0, min(1.0, parse_gate * RAW))

    P, R, F1 = prf(cv_tok, must_have)
    return {
        "score_percent": round(Score * 100, 1),
        "components": {
            "Lex": round(Lex, 3),
            "Sem": (round(Sem, 3) if Sem is not None else "yok (SBERT kurulu değil)"),
            "Cov": round(Cov, 3),
            "Parse_gate": parse_gate,
            "Stuffing": round(Stuff, 3),
        },
        "weights_used": {"alpha": round(a, 3), "beta": round(bb, 3), "gamma": round(g, 3), "zeta": zeta},
        "gap": gap,
        "precision": P, "recall": R, "f1": F1,
        "interpretation": ("hedef %75-85 | >%90 şişirme sinyali | <%50 ciddi iyileştirme"),
    }


# ----------------------------- CLI -----------------------------

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="ATS hibrit match score (denetim-düzeltmeli)")
    ap.add_argument("--jd", required=True, help="iş ilanı metin dosyası")
    ap.add_argument("--cv", required=True, help="CV metin dosyası")
    ap.add_argument("--must", default="", help="zorunlu terimler, virgülle ayrık")
    ap.add_argument("--corpus", default=None, help="opsiyonel corpus klasörü (.txt'ler)")
    ap.add_argument("--parse-gate", type=float, default=1.0, help="biçim kapısı 0.6-1.0")
    ap.add_argument("--no-sbert", action="store_true", help="semantik katmanı atla")
    args = ap.parse_args()

    corpus = None
    if args.corpus and os.path.isdir(args.corpus):
        corpus = [_read(os.path.join(args.corpus, f))
                  for f in os.listdir(args.corpus) if f.endswith(".txt")]

    must = [m.strip() for m in args.must.split(",") if m.strip()]
    res = ats_match_score(_read(args.jd), _read(args.cv), must,
                          corpus_texts=corpus, parse_gate=args.parse_gate,
                          use_sbert=not args.no_sbert)

    import json
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```


---


*Belge sonu — 8/8 dosya eksiksiz aktarıldı.*
