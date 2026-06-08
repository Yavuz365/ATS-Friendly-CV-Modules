---
name: ats-cv-architect
description: Build ATS-optimized, tailored CVs by decomposing a job posting (ANALYSIS) and recombining it against the candidate's master/framework CV (SYNTHESIS), then scoring the fit. Use this WHENEVER the user wants to tailor a CV/résumé to a specific job posting or job description (JD), optimize a CV for ATS / applicant tracking systems, compute an ATS match score, run keyword or gap analysis between a JD and a CV, or push a job posting through an "analysis + synthesis" / SEO pass to produce CV-ready material — even if they only say "make my CV fit this job", "is my CV ATS-friendly", "tailor my resume to this posting", "analyze this job ad for my CV", or simply paste a JD and a CV together. Also fires when the user mentions match score, keyword coverage, gap analysis, or a Drive/Word workflow that feeds job postings to AI tools. Defaults to Turkish output; switches language on request.
license: Proprietary. Built for Ahmet's analyst/job-search workflow.
---

# ATS CV Architect

## Ne işe yarar (core mantra)
Bir iş ilanını **çöz** (ANALİZ), adayın gerçek kariyer verisiyle **yeniden bağla** (SENTEZ), sonra **ölç ve doğrula** (SKOR + GAP). Tek bir ATS-uyumlu, ilana özel CV ve onun arkasındaki 6 yapılandırılmış veri alanını üretir. Bu skill, "önce çöz, sonra bağla, sonra kontrol et, gerekirse yeniden bağla" diyalektik döngüsünü iş ilanı → CV problemine uygular.

Bu skill yalnızca "anahtar kelime sayma" aracı değildir. Sentez katmanı (kanıta dayalı başarı cümleleri, dürüstlük kontrolü, anlatısal tutarlılık) en az analiz katmanı kadar önemlidir. İki katman da uygulanmadan iş bitmiş sayılmaz.

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
- **A.2** JD'yi AI aracı ile SEO analiz+sentez'den geçir, çıktıyı **`[SENTEZ-ÖNERİ]` bölümüne** ekle — asla JD-orijinalin içine değil. (Neden: enjekte edilen LSI/eşanlamlı terimler, adayda *olmayan* beceriler olabilir; bunları sonradan CV-yazıcı "adayın özelliği" sanmamalı.)
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
- `references/workflow-drive-multitool.md` — Drive + AI aracı + çok-LLM iş akışının kurulumu ve denetimi.
- `assets/master-prompt-TR.md` — herhangi bir LLM'e taşınabilir Master Prompt (AI aracı/ChatGPT/DeepSeek/GLM/Qwen/Mistral).
- `assets/output-fields-template.md` — 6 alanlık çıktı şablonu.

Protokolü her çalıştırmada kısa yol kullanmadan yürüt. Disiplinin kendisi üründür.
