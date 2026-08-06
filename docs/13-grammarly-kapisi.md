# docs/13 — İsteğe Bağlı Dil ve Stil Danışmanlığı

> **Legacy/vendor notu:** Harici vendor sonucu otomatik veya evrensel kalite kapısı sayılmaz.

> Harici dil aracı çıktısı yalnız danışmanlıktır; ATS, aday uygunluğu veya AI-yazımı
> hakkında doğrulanmış bir kapı değildir.

## 1. Neden Grammarly Kapısı?

CV metni tekrarlayan kalıplar, dilbilgisi sorunları veya gereksiz karmaşıklık içerebilir.
Harici bir dil aracı bunları işaretleyebilir; nihai karar insan incelemesidir.

## 2. Pipeline'daki Yeri

```
Lexical/semantic tanı (evrensel eşik yok) → isteğe bağlı dil denetimi
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ▼               ▼               ▼
                              Dil denetimi      Rewriter         Builder
                              (advisory)        (yeniden yaz)    (güçlendir)
```

## 3. Üç Fonksiyon

### 3a. Dil ve Stil Sinyalleri

Correctness, clarity ve tekrar sinyallerini incele. Sabit yüzde eşiği kullanma; bu
değerleri “güvenli/güvensiz”, “insan/AI yazımı” veya işe-alım sonucu olarak yorumlama.

### 3b. Rewriter (Yeniden Yazma)

Metin açık değilse:
1. Her CV bölümünü ayrı ayrı Grammarly'den geçir
2. "Rewrite for clarity" özelliğini kullan
3. Korunan olguların ve JD terimlerinin değişmediğini doğrula
4. İnsan okunabilirliği yeterli olduğunda döngüyü durdur

**Dikkat:** Yeniden yazma keyword density'yi etkileyebilir → yeniden `ats_match_score()` çalıştır.

### 3c. Builder (Güçlendirme)

Grammarly'nin dil kalitesi metrikleri:

| Metrik | Hedef | Açıklama |
|--------|-------|----------|
| Correctness | Advisory | Dilbilgisi, yazım, noktalama |
| Clarity | Advisory | Cümle uzunluğu, karmaşıklık |
| Engagement | Advisory | Kelime çeşitliliği |
| Delivery | Advisory | Ton, profesyonellik |

## 4. Keyword Koruma Stratejisi

Grammarly yeniden yazma sırasında JD terimlerini değiştirebilir. Koruma kuralları:

1. **Teknik terimler** → dokunulmaz listesi: ERP, SAP, akreditif, incoterms, vb.
2. **Zorunlu (must-have) terimler** → yeniden yazma sonrası `coverage()` kontrolü
3. **Aksiyon fiilleri** → tier1 fiiller (`action_verbs.json`) korunmalı
4. Yeniden yazma sonrası kanıt ID’leri, korunan olgular ve açık gereksinimler yeniden doğrulanır

## 5. Pratikte Kullanım

```
Adım 1: Motor tanısını hesapla → değer yalnız sürümlü evaluation profile bağlamında yorumlanır
Adım 2: CV'yi Grammarly'ye yapıştır
Adım 3: Dil/stil sinyallerini incele
Adım 4: Rewriter → bölüm bölüm yeniden yaz
Adım 5: İnsan okunabilirliği ve olgu korumasını doğrula
Adım 6: Correctness/Clarity/Engagement/Delivery kontrol
Adım 7: Motor tanısını yeniden çalıştır; sonucu outcome/pass eşiği sayma
Adım 8: Gönder ✅
```

## 6. Entegrasyon Notu

Grammarly harici bir araçtır — motor (engine/) Grammarly'ye bağımlı değildir.
Grammarly kapısı **isteğe bağlı son katmandır**.

Gelecekte API entegrasyonu (Grammarly Developer API) ile otomatikleştirilebilir.
