# docs/13 — Grammarly Kapısı (AI-Detector / Rewriter / Builder)

> CV'nin Grammarly ile AI-tespit kontrolü, yeniden yazma ve son cilalanması.

## 1. Neden Grammarly Kapısı?

AI tarafından üretilen CV metinleri:
- Tekrarlayan kalıplar içerir ("leveraged", "spearheaded", "orchestrated")
- ATS'den geçse bile insan HR tarafından tespit edilebilir
- Bazı şirketler AI-detection araçları kullanmaya başladı

**Çözüm:** Motor (engine/) deterministik skor üretir → LLM CV yazar → Grammarly son katman.

## 2. Pipeline'daki Yeri

```
Motor Skoru (%75-85 bandı) → CV onaylandı → Grammarly Kapısı
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ▼               ▼               ▼
                              AI-Detector      Rewriter         Builder
                              (tespit)         (yeniden yaz)    (güçlendir)
```

## 3. Üç Fonksiyon

### 3a. AI-Detector (Tespit)

Grammarly'nin AI-detection özelliği ile CV metnini tara:
- **< %30 AI skoru** → Güvenli, doğrudan gönder
- **%30 – %80** → Rewriter gerekli
- **> %80** → Ciddi yeniden yazma + insan düzenleme

### 3b. Rewriter (Yeniden Yazma)

AI-detector skoru yüksekse:
1. Her CV bölümünü ayrı ayrı Grammarly'den geçir
2. "Rewrite for clarity" özelliğini kullan
3. Sonra tekrar AI-detector ile kontrol et
4. Döngü: AI skoru < %30 olana kadar

**Dikkat:** Yeniden yazma keyword density'yi etkileyebilir → yeniden `ats_match_score()` çalıştır.

### 3c. Builder (Güçlendirme)

Grammarly'nin dil kalitesi metrikleri:

| Metrik | Hedef | Açıklama |
|--------|-------|----------|
| Correctness | %95+ | Dilbilgisi, yazım, noktalama |
| Clarity | %90+ | Cümle uzunluğu, karmaşıklık |
| Engagement | %80+ | Kelime çeşitliliği, dinamizm |
| Delivery | %85+ | Ton, profesyonellik |

## 4. Keyword Koruma Stratejisi

Grammarly yeniden yazma sırasında JD terimlerini değiştirebilir. Koruma kuralları:

1. **Teknik terimler** → dokunulmaz listesi: ERP, SAP, akreditif, incoterms, vb.
2. **Zorunlu (must-have) terimler** → yeniden yazma sonrası `coverage()` kontrolü
3. **Aksiyon fiilleri** → tier1 fiiller (`action_verbs.json`) korunmalı
4. Yeniden yazma sonrası `ats_match_score()` ≥ önceki skor − 5 puan

## 5. Pratikte Kullanım

```
Adım 1: Motor skoru hesapla → %78 (mülakata hazır bant)
Adım 2: CV'yi Grammarly'ye yapıştır
Adım 3: AI-detector → %45 (orta risk)
Adım 4: Rewriter → bölüm bölüm yeniden yaz
Adım 5: AI-detector → %22 (güvenli)
Adım 6: Correctness/Clarity/Engagement/Delivery kontrol
Adım 7: Motor skoru yeniden hesapla → %76 (hâlâ banda içinde)
Adım 8: Gönder ✅
```

## 6. Entegrasyon Notu

Grammarly harici bir araçtır — motor (engine/) Grammarly'ye bağımlı değildir.
Grammarly kapısı **isteğe bağlı son katmandır**.

Gelecekte API entegrasyonu (Grammarly Developer API) ile otomatikleştirilebilir.
