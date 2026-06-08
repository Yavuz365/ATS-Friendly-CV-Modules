# Drive + Çok-LLM İş Akışı (A.1–A.3 / B.1) — Kurulum ve Denetim

Kullanıcının somut akışı: iş ilanını Drive'a Word olarak koy, AI aracı ile SEO analiz+sentez geçir, Master Prompt ile stratejik yapıya oturt, sonra (Claude/ChatGPT/DeepSeek/GLM/Qwen/Mistral'dan biriyle) Drive'dan veri çekip Framework CV ile eşleştirerek ATS CV yazdır. Bu dosya akışı adım adım kurar ve denetimde bulunan riskleri düzeltir.

## Akış (düzeltilmiş)

### A.1 — JD'yi Drive'a Word olarak yükle, ETİKETLİ
Word belgesini üç etiketli bölümle aç:
```
[JD-ORİJİNAL]      ← ilanın ham, değiştirilmemiş metni. Asla kirletme.
[ANALİZ]           ← 7 katmanlı ayrıştırma çıktısı (jd-decomposition.md)
[SENTEZ-ÖNERİ]     ← AI aracı'nin SEO genişletmeleri, LSI terimleri, öneriler
```
**[DENETİM-DÜZELTME C2 — kirlenme riski.]** JD'yi ve AI aracı'nin SEO çıktısını aynı bölüme karıştırma. Enjekte edilen LSI/eşanlamlı terimler adayda *olmayan* beceriler olabilir; karışırsa CV-yazıcı bunları sonradan "JD gerçeği" veya "aday özelliği" sanır → şişirme + dürüstlük ihlali. Etiketli bölümler bunu önler.

### A.2 — AI aracı ile SEO analiz + sentez
AI aracı'ye `assets/master-prompt-TR.md`'nin ANALİZ+SENTEZ kısmını ver; çıktıyı **yalnızca `[SENTEZ-ÖNERİ]` bölümüne** yapıştır. AI aracı'ye açıkça söyle: ürettiğin genişletilmiş terimler *aday-tarafı hedeflerdir; yalnızca aday gerçekten karşılıyorsa kullanılacaktır*, JD hakkında ya da aday hakkında olgu değildir.

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
- **SENTEZ (cümle yazımı, kümeleme):** Claude/GPT/AI aracı — yaratıcı-akıl katmanı.
- **Skor/gerçek matematik:** kod (scripts/ats_score.py). LLM "tahmini skor" verir; tutarlılık için koda taşı.
- **Otomasyon:** otomasyon platformu — Drive tetikleyici → model çağrısı → 6 alanı tabloya yaz → Telegram/Slack bildirimi.

## Taşınabilirlik uyarısı (tekrar)
**[DENETİM-DÜZELTME C1.]** Bu .skill yalnızca Claude'da çalışır. AI aracı/ChatGPT/DeepSeek/GLM/Qwen/Mistral için `assets/master-prompt-TR.md`'yi kullan — aynı mantığı taşınabilir prompt olarak taşır. Çok-araçlı akışın bel kemiği bu prompttur, skill değil.

## Toplu mod (100 ilan / data mining)
Her ilan bir satır olacak şekilde bir Google Sheet/Notion tablosu kur; sütunlar = 6 alan + final skor. otomasyon platformu akışı her yeni ilanda pipeline'ı çalıştırıp satırı doldurur. Sonra skora göre sırala → "bana en uygun ilanlar" listesi. İstenirse xlsx skill ile karşılaştırma tablosu/grafiği üret.
