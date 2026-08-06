# Legacy Diagnostic Formülleri — Ürün Kararı Değildir

> Bu matematik ticari ATS formülünün yaklaşımı olarak sunulamaz. Değerler yalnız
> lexical/semantic hizalanma tanısıdır. Açık must listesi yoksa genel skor üretilmez:
> `score_percent=null`, `NOT_EVALUATED/REVIEW`.

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

Evrensel eşik yoktur. Eşik ancak kaynak, tarih, dil, domain, corpus ve comparator
versiyonu bağlı bir evaluation profile içinde tanı amacıyla kullanılabilir. Bir değer
ATS geçişi, mülakat veya işe alım olasılığı değildir.

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
