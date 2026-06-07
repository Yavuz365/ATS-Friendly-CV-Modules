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
- `1.0` — açıkça zorunlu ("required/must/şart").
- `0.7` — güçlü ima / tekrarlı: "required" etiketi yok ama terim ≥2–3 kez geçiyor ya da sorumluluk katmanında merkezî. Saf 1.0/0.3 ikilisi bu gizli zorunlulukları kaçırır.
- `0.3` — açıkça tercih ("preferred/plus/avantaj").
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