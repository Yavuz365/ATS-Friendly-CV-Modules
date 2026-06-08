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
Madde bu tabloya giremiyorsa CV'ye de giremez.
