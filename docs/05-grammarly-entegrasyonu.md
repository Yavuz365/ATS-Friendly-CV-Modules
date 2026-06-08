# 05 — Grammarly Ansiklopedisi: Karşılaştırma & Motora Aktarım (ANALİZ)

Bu doküman, projedeki **Grammarly Keyword-Optimization / Resume-Builder** kaynağının (≈1800 satırlık iki dilli SEO+ATS ansiklopedisi) sistemle **karşılaştırmasıdır** ve nelerin motora veri olarak aktarıldığını belgeler. Kullanıcının "Grammarly ile kıyasla, neyi geliştirebiliriz" sorusunun yanıtıdır.

## 1. Örtüşen çekirdek (zaten sistemde vardı)
Grammarly kaynağı ile mevcut ATS mimarisi şu noktalarda **birebir örtüşüyor** — yani sistem bu açıdan doğrulandı:
- NLP tabanlı eşleştirme; TF-IDF/anahtar kelime ağırlığı.
- Bulanık eşleştirme: **Jaccard benzerliği + Levenshtein mesafesi** → "team management" ↔ "led a cross-functional team".
- **Skill Normalization** (eşanlamlı/normalize beceri tabanı).
- **XYZ / CAR** cümle mimarisi + niceliksel örüntüler (quantification).
- Aktif fiil vurgusu (passive→active).
- Flesch-Kincaid okunabilirlik / bilişsel yük azaltımı.
- Ton & formellik eşleşmesi.

## 2. Grammarly'nin getirdiği EK değer → motora aktarıldı
| Grammarly katkısı | Sisteme etkisi | Nereye kondu |
|---|---|---|
| **700+ aktif eylem fiili** kütüphanesi (Achieved, Orchestrated, Optimized, Streamlined…) | Sentez artık fiili "tahmin" etmiyor, kategorize veri tabanından çekiyor | `engine/data/action_verbs.json` + `lexicons.action_verbs_by_intent()` |
| **Skill synonym / LSI** kümeleri (Tedarik Zinciri ↔ Navlun, Akreditif, Incoterms, ERP) | Eşanlamlı-duyarlı kapsama ve LSI genişletme deterministik hâle geldi | `engine/data/skill_synonyms.json` + `lexicons.expand_lsi()` |
| **Jaccard + Levenshtein** fuzzy matching | Kapsama hesabı yalnızca birebir değil, varyant-toleranslı | `lexicons.jaccard()`, `matches_semantically()` |
| **Quantification pattern** tespiti | Bullet kalite denetimi (sayı var mı?) | `text.has_quantification()` + `synthesis.audit_bullet()` |
| **Readability** sinyali | Anti-stuffing/okunabilirlik raporu | `text.density()`, `looks_passive()` |

## 3. Sistemin Grammarly'den ÜSTÜN olduğu noktalar (geliştirme yönü)
Grammarly güçlü bir **dil/SEO** katmanı; ama tek başına bir ATS-CV motoru değil. Sistem şunları ekler:
1. **Provenans/dürüstlük zinciri** — Grammarly fiil/kelime önerir ama "bu adayda gerçekten var mı?" garantisi yok. Sistem her maddeyi kanıt bankasına bağlar (halüsinasyon önleyici).
2. **Audit-düzeltmeli hibrit skor** — Parse_gate çarpanı, clamp, Lex/Cov ayrımı; tescilli ATS davranışına daha sadık proxy.
3. **Kapatılabilir/kapatılamaz gap ayrımı + sonsuz-döngü düzeltmesi (H1)** — Grammarly'de yok.
4. **7 katmanlı JD niyeti** (memur değil denetçi) — saf kelime optimizasyonunun ötesinde stratejik okuma.
5. **Çok-araçlı taşınabilirlik + otomasyon** (Master Prompt, otomasyon platformu, Notion).

## 4. Sonuç
Grammarly ansiklopedisi sistemi **çürütmedi, güçlendirdi**: dil/fiil/synonym katmanını somut veriye dönüştürdü (`engine/data/*.json`). Sistemin ayırt edici omurgası (sentez-önce, provenans, audit-düzeltmeli skor, gap döngüsü) ise Grammarly'nin kapsamadığı katmandır. İkisi tamamlayıcıdır.

> Ham kaynak: `Keyword_Optimization_-_Grammarly_docx.md` (proje köküne referans). Damıtılmış sözlük: `docs/research/R3-seo-ats-sozluk.md`.
