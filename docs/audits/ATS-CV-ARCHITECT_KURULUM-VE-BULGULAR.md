# ATS CV ARCHITECT — Denetim, Düşünme Yöntemi ve Kurulum Dosyası
*Bu sohbetteki üç raporun (Analiz, Sentez, ATS Sistemi) ve kurulum kılavuzunun birleştirilmiş, denetlenmiş ve yeniden örgütlenmiş halidir. `synthesis-analysis-research` disipliniyle (Katman 0–5, kaynak/provenans defteri, dürüst güven) hazırlanmış; `skill-creator` ile `ats-cv-architect.skill` üretilmiştir.*

---

## BÖLÜM 0 — Yöntem: Diyalektik Döngü (yeniden inşa)
Bu sohbette örtük kullandığımız düşünme biçimini açık bir 6-vuruşlu döngüye sabitliyoruz. Sizin ifadenizle: "veriyi al → sentezle → parçala → analiz et → parçaları eşleştir → yeniden sentezle → analiz sonrası sentezle sentetik düşünmeye geç."

| Vuruş | Ad | Edim | CV motorundaki karşılığı |
|------|-----|------|---------------------------|
| 0 | Ön-sentez | Bütünü kabaca kavra | İlanın "özü"nü tek cümleyle yakala (Katman 1) |
| 1 | Ayrıştırma | Bütünü parçalara böl | JD'yi 7 katmana çöz (Katman 2) |
| 2 | Analiz | Parçaları tek tek incele, ağırlıkla | TF-IDF/BM25 + modality + konum ağırlığı |
| 3 | Eşleştirme | Parçaları ihtiyaçla karşılaştır | JD terimleri ↔ Framework CV girdileri; skor + gap |
| 4 | Yeniden sentez | Yeni, tutarlı bütün kur | Kümeleme + XYZ cümleleri + üst özet → CV |
| 5 | Doğrulayıcı analiz | Bütünü sına | Provenans kontrolü + skoru yeniden hesapla |
| → | Sentetik düşünme | Bütünden üret | Doğrulanmış CV'den ilana özel anlatı/strateji |

**Çekirdek ilke (üç rapordan damıtılan):** Analiz çözer, sentez bağlar; ama hiçbiri tek başına yetmez. Saf analiz anlamı kaybeder (parçaya ayrılan kurbağa artık yaşamaz — beliren nitelik buharlaşır); saf sentez temelsiz kalır (sahte/erken sentez). Gerçek kavrayış, parça ile bütün arasındaki tükenmeyen döngüdür (hermenötik döngü). CV motoru bu döngünün mühendislik hali: çöz → ölç → bağla → doğrula → gerekirse yeniden bağla.

---

## BÖLÜM 1 — DENETİM (audit-mode): Sistemde bulunan hatalar
`synthesis-analysis-research` denetim disipliniyle üç raporu ve kurulum metnini taradım. Bulgular önem sırasıyla, her birinde **düzeltme** ile:

### Yüksek önem
- **H1 — Revizyon döngüsü sonsuza girer (mantık hatası).** Eski kural: `skor < hedef VEYA gap ≠ boş → döngü`. Dürüst CV'de adayda olmayan zorunlu beceriler hep kalır → gap asla boşalmaz → sonsuz döngü. **Düzeltme:** durma koşulu `skor ≥ hedef VE *kapatılabilir* gap kalmadı`; gap'i kapatılabilir (kanıtı var, yansımamış) ve kapatılamaz (gerçekten yok) diye ayır; yalnızca kapatılabilir üzerinde dön.
- **H2 — Taşınabilirlik kırılması (kullanılabilirlik).** Bir Claude `.skill` AI aracı/ChatGPT/DeepSeek/GLM/Qwen/Mistral'da çalışmaz; sizin akışınız çok-araçlı. Yalnızca .skill verilseydi akışın çoğu çalışmazdı. **Düzeltme:** taşınabilir Master Prompt (`master-prompt-TR.md`) — aynı mantığı her LLM'e kopyalar; çok-araçlı akışın bel kemiği skill değil bu prompttur.

### Orta-yüksek önem
- **MY1 — Provenans (dürüstlük) yalnızca ilkeydi, adım değildi.** "Sahte beceri ekleme" kuralı vardı ama uygulamada zorlayan bir kontrol yoktu. **Düzeltme:** çıkıştan önce zorunlu provenans tablosu — her CV maddesi Framework CV'deki bir girdi-id'sine bağlanmalı; bağlanamayan madde çıkar. (Source Registry'nin CV'ye uygulanmış hali.)
- **MY2 — JD + AI aracı SEO çıktısı aynı bölümde → kirlenme.** Enjekte LSI/eşanlamlı terimler adayda *olmayan* beceriler olabilir; karışırsa CV-yazıcı bunları "gerçek" sanır → şişirme + dürüstlük ihlali. **Düzeltme:** Word'de etiketli bölümler `[JD-ORİJİNAL] / [ANALİZ] / [SENTEZ-ÖNERİ]`; önerilen terimler "aday-tarafı hedef", olgu değil.
- **MY3 — 20 sayfa Framework CV'yi ham beslemek.** Bağlamı boğar, eşleşmeyi gürültüyle zayıflatır. **Düzeltme:** Framework CV'yi etiketli "kanıt bankası"na çevir (her başarı = bir girdi, beceri+metrik etiketli); her ilanda yalnızca eşleşen girdileri çek.

### Orta önem
- **M1 — Skor alt sınırı kıskaçlanmamış.** `α+β+γ+δ=1` pozitif kısmı [0,1]'de tutar ama `−ζ·Stuffing` negatife itebilir. **Düzeltme:** `Score = clamp(..., 0, 1)`.
- **M2 — Parse "match" skoruna toplanmış.** Parse, *bu ilana uyum* değil *genel okunabilirlik*tir (JD'den bağımsız). Toplamak iki farklı şeyi karıştırır. **Düzeltme:** Parse'ı kapı/çarpan yap: `Score = Parse_gate × (α·Lex+β·Sem+γ·Cov − ζ·Stuff)`; bozuk biçim skoru orantılı düşürür.
- **M3 — Lex ve Cov bağımlı (çift sayım).** İkisi de "terim var mı"yı ödüllendirir; bağımsızmış gibi toplanırsa kapsam fazla ağırlık alır. **Düzeltme:** Lex = TÜM JD terimleri üzerinden TF-IDF kosinüs; Cov = yalnızca zorunlular üzerinden ikili kapsam; ağırlıkları buna göre düşür.
- **M4 — modality ∈ {1.0, 0.3} fazla kaba.** Gizli zorunlulukları (etiketsiz ama tekrarlı/merkezî terim) kaçırır. **Düzeltme:** 3 kademe (1.0 / 0.7 güçlü-ima / 0.3) + sıklık katkısı.

### Düşük önem
- **D1 — İki semantik çekirdek (LSA/SVD + SBERT) paralel sunulmuş** → uygulayıcı ikisini birden kurabilir. **Düzeltme:** SBERT birincil; LSA/SVD kavramsal ata / hafif yedek.
- **D2 — Çözümlü örnek aritmetiği DOĞRU (0.7705) — hata yok.** (Denetim yalnızca hata avı değildir; bunu da teyit ediyoruz.) Ancak örnek Lex/Cov bağımlılığını ve kıskaçlamayı gizler; düzeltilmiş örnek `scoring-formulas.md`'de.
- **D3 — Vendor-kaynaklı istatistikler ödünç otoriteyle sunulmuş** (%98 Fortune 500, %88 işveren, 3.2×, BERT %15.85, F1 %90.62). Yön doğru; kesin rakamlar her geçtikleri yerde "vendor/tek-çalışma kaynaklı" çekincesiyle dolaşmalı.
- **D4 — "%75 mit"i ile sistemin gerekçesi arasında çerçeve gerilimi.** Raporlar miti dürüstçe çürütüyor (CV'lerin ~%90+'ı insan inceler) ama TL;DR hâlâ ATS-merkezli. **Düzeltme:** çerçeveyi "botu geç"ten "sıralamayı kazan + temiz parse + insana hızlı evet" e kaydır.

> **Genel hüküm:** Sistem sağlam ve kullanışlı; kritik tek gerçek mantık hatası H1 (döngü) ve kritik kullanılabilirlik eksiği H2 (taşınabilirlik) idi. İkisi de yeni skill'de giderildi. Diğer düzeltmeler skoru daha dürüst ve daha kalibre yapıyor.

---

## BÖLÜM 2 — Bir İş İlanı Hangi Parçalara Ayrılır? (ANALİZ şeması)
ATS-CV amacıyla her JD **7 katmana** ayrılır (ayrıntı: skill'in `references/jd-decomposition.md`):
1. **Kimlik** — unvan, kıdem, sektör, lokasyon, şirket, çalışma biçimi, dil.
2. **Zorunlu (must-have)** — sert beceri/araç, sertifika, deneyim yılı, eğitim, yasal/knockout (ikili eler). Ağırlık 1.0.
3. **Tercih (nice-to-have)** — "preferred/plus/avantaj". Ağırlık 0.3.
4. **Sorumluluk/eylem** — "ne yapacaksın" fiilleri → XYZ başarı cümlelerine hammadde.
5. **Niyet/alt-metin** — "Bu rol esasen ___ arıyor" (ör. memur değil denetçi).
6. **Semantik/LSI** — her önemli terimin eşanlamlı/akraba kümesi (yalnızca eşleşmeyi *anlamak* için, doldurmak için değil).
7. **Ağırlık metası** — her terime modality (1.0/0.7/0.3) + konum ağırlığı (ilk 150 kelime ağır) + sıklık.

Bu yedi parça, hem skorlamanın hem sentezin doğrudan girdisidir.

---

## BÖLÜM 3 — Matematik Özeti (formüller)
Tam türetim ve düzeltmeler: `ats-cv-architect_SCORING-FORMULAS.md`.
- **TF-IDF:** `w = tf × idf`, `idf = log(N/df)`.
- **BM25:** doyumlu (k1≈1.5) + uzunluk-normalizeli (b≈0.75); şişirmeyi matematiksel cezalar.
- **Kosinüs:** `cos = A·B/(‖A‖‖B‖)`.
- **Semantik:** SBERT cümle gömme + kosinüs (eşanlamlı/parafraz yakalar).
- **Hibrit (düzeltilmiş):** `RAW = α·Lex + β·Sem + γ·Cov − ζ·Stuff`; `Score = clamp(Parse_gate × RAW, 0, 1)`; öneri `α=0.35, β=0.30, γ=0.35, ζ=0.20`, `Parse_gate∈[0.6,1.0]`.
- **P/R/F1 + gap:** `R` = zorunlu kapsam (eksik = gap), `P` = ilgililik (düşük = şişirme); gap'i kapatılabilir/kapatılamaz ayır.
- **Eşik (v2 düzeltmesi):** Evrensel eşik yoktur; yalnız sürümlü evaluation profile içinde tanı amaçlıdır.

---

## BÖLÜM 4 — KURULUM: Sıfırdan İnşa Adımları (yapmanız gerekenler)

### Aşama 0 — Zemin (bir kez)
1. **Framework CV'yi kanıt bankasına çevir.** 20 sayfayı tek tek girdilere böl: `EXP-07 | alan | [beceriler] | metrik | dönem | kanıt-cümlesi`. (En kritik adım; sentez bundan beslenir.)
2. **Beceri sözlüğü bağla.** ESCO (çok dilli) veya O*NET; ya da kendi sektörün için 100–200 kelimelik eşanlamlılar tablosu.
3. **Corpus topla.** Aynı sektörden 50–100 ilan (TF-IDF/BM25'in "nadir vs sıradan" ayrımı için). İlk ilanlarda küçük, zamanla güçlenir.

### Aşama 1 — Skill'i kur (Claude tarafı)
4. `ats-cv-architect.skill` dosyasını Claude'a yükle (Settings → Capabilities/Skills → upload). Artık "CV'mi şu ilana göre uyarlar mısın" dediğinde tetiklenir.

### Aşama 2 — Çok-araçlı akışı kur (AI aracı/ChatGPT/DeepSeek/…)
5. `master-prompt-TR.md`'yi bu araçlara kopyala-yapıştır şablonu olarak sakla (skill onlarda çalışmaz).
6. Drive'da JD için **etiketli Word** şablonu: `[JD-ORİJİNAL] / [ANALİZ] / [SENTEZ-ÖNERİ]`.

### Aşama 3 — Tek ilan akışı (her ilan)
7. **A.1** JD'yi Word'ün `[JD-ORİJİNAL]` bölümüne koy, Drive'a yükle.
8. **A.2** AI aracı'de Master Prompt'un ANALİZ+SENTEZ kısmını çalıştır → çıktıyı `[SENTEZ-ÖNERİ]`ye yapıştır (asla orijinale karıştırma).
9. **A.3** Tam Master Prompt ile 6 alanı üret (keywords/analysis/summary/synthesis/match_score/gap_analysis).
10. **B.1** CV-yazıcı: Drive'dan 6 alan + kanıt bankasını alır, eşleşen+kanıtlı girdileri seçer, ATS CV yazar, skoru hesaplar, kapatılabilir gap üzerinde revize eder, provenans kontrolünü geçirir.

### Aşama 4 — Gerçek matematik (opsiyonel, tutarlılık için)
11. `scripts/ats_score.py`'yi çalıştır (LLM tahmini yerine deterministik skor). SBERT için `pip install sentence-transformers`; corpus klasörü ver. Corpus+SBERT yoksa skoru göreli oku.

### Aşama 5 — Otomasyon + toplu mod (100 ilan)
12. otomasyon platformu: Drive tetikleyici → model çağrısı → 6 alanı Google Sheet/Notion satırına yaz → Telegram/Slack bildirimi.
13. Skora göre sırala → "bana en uygun ilanlar". İstersen xlsx ile karşılaştırma tablosu.

### Önerilen sıra (boğulmamak için)
- **Hafta 1:** Kanıt bankası + tek ilanı elle (Master Prompt'la) çalıştır, mantığı hisset.
- **Hafta 2:** Skill'i kur, 5–10 ilanda test et.
- **Hafta 3:** `ats_score.py`'yi gerçek corpus+SBERT ile devreye al.
- **Hafta 4:** otomasyon platformu ile 100 ilanı otomatikleştir.

---

## Dürüst sınırlamalar
- Skor repository’nin lexical/semantic tanısıdır; Workday/Greenhouse/iCIMS iç formüllerinin
  proxy’si veya yaklaşımı olduğu iddia edilmez.
- Corpus+SBERT olmadan `ats_score.py` skorları muhafazakâr/göreli; kalibrasyon için ikisi de gerekir.
- Aşırı optimizasyon (>%90, tekrar) geri teper.
- Dürüstlük mutlaktır: provenansa bağlanamayan hiçbir madde CV'ye girmez; sahte terim mülakatta çöker.
- Bu skill yalnızca Claude'da çalışır; diğer modeller için Master Prompt kullan.
