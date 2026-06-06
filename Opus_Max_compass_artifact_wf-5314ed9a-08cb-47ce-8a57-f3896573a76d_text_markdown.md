# ANALİZ ↔ SENTEZ Motoru: Herhangi Bir İş İlanı İçin ATS-Uyumlu CV Üretiminin Matematiksel ve Algoritmik Sistem Spesifikasyonu
**(Domain-agnostic / sektör bağımsız, ~100 ilana uygulanabilir yeniden kullanılabilir protokol)**

## TL;DR (Özün Özü — Üç Madde)
- **Sistem, iki katmanlı diyalektik bir motordur:** (1) **ANALİZ katmanı** ("düğümü çözme") herhangi bir iş ilanını en ince ögelerine ayrıştırır — tokenizasyon, lemmatizasyon, NER (skill/araç/sertifika/kıdem), n-gram çıkarımı, zorunlu/tercih ayrımı ve TF-IDF + BM25 ile **ağırlıklı anahtar kelime** üretimi; (2) **SENTEZ katmanı** ("düğümü bağlama") bu ögeleri ATS-optimize bir CV'ye yeniden birleştirir — semantik kümeleme, LSI/embedding genişletme, eylem-fiili eşlemesi ve XYZ/CAR formüllü nicelenmiş başarı cümleleri. Bu, Descartes'ın analiz (parçalara bölme) ve sentez (basitten karmaşığa yeniden inşa) kurallarının bir IR problemine operasyonelleştirilmiş halidir.
- **Skorlama, hibrit ağırlıklı bir "ATS Match Score"dur:** **Score = α·Lex + β·Sem + γ·Cov + δ·Parse − ζ·Stuffing**; lexical (TF-IDF/BM25), semantik (SBERT kosinüs), zorunlu kapsam, parse uygunluğu ve stuffing cezası birleşir. Bileşenler min-max ile [0,1]'e normalize; ağırlıklar grid-search/validasyonla ayarlanır. Bu yapı modern ATS'lerin (Workday, Greenhouse, iCIMS) 2024–2026'da yaptığı lexical+semantik hibrit eşleştirmeyi taklit eder.
- **Dürüst gerçeklik kontrolü:** "Özgeçmişlerin %75'i hiçbir insan tarafından görülmez" **kanıtlanmamış bir mittir** (kaynak: tasfiye olmuş Preptel firmasının satış argümanı); Enhancv'nin 25 işe alımcı çalışmasında %92'si CV'leri otomatik reddetmediğini söyledi. Gerçek risk "otomatik ret" değil, **düşük sıralama + yanlış ayrıştırmadır.** Sistem oyun oynamayı (stuffing) değil, doğru/kanıtlanabilir hizalamayı hedefler; aşırı optimizasyon (>%90 eşleşme, tekrar) ceza üretir.

> **Metodoloji (kullanıcının "Önce Sentez, Sonra Analiz" tercihi):** Rapor önce bütünsel manzarayı sentezler, sonra bileşenleri ayrıştırıp eleştirir. Teknik terimler/formüller İngilizce, açıklamalar Türkçedir.

---

## 1. Felsefi-Bilişsel Çekirdek ve Sistem Akışı
Mimari, **analiz** ve **sentez** çiftine dayanır. Descartes'ın *Discours de la méthode* (1637) eserindeki iki kural doğrudan temeldir:
- **Analiz (ayrıştırma):** "Her güçlüğü mümkün olduğunca çok parçaya böl." Karmaşık fikri indirgenemez **"natures simples" (basit doğalar)** kümesine indir.
- **Sentez (yeniden inşa):** "En basit nesnelerden başla, derece derece en karmaşığa yüksel." Analizden sonraki **yapıcı fazdır.**

Fransız epistemoloji bunu **"dénouer/décomposer"** (düğümü çözmek) ve **"composer un tout"** (bütünü kurmak) olarak adlandırır. CV motorundaki eşleme:

| Süreç | Descartes | IR/SEO karşılığı | CV motoru |
|---|---|---|---|
| **ANALİZ** | Basit doğalara in | Term ağırlıklandırma, keyword extraction | Tokenize → lemmatize → NER → zorunlu/tercih ayır → TF-IDF/BM25 ağırlıkla |
| **SENTEZ** | Basitten karmaşığa kur | Semantik kümeleme, içerik üretimi | Semantik kümeler → LSI genişletme → XYZ/CAR cümleleri → tutarlılık |

**Vurgu:** Sistem yalnızca "anahtar kelime analizi" değildir; sentez katmanı en az analiz kadar titizlikle tasarlanmıştır. IR analojisi hibrit aramadır: lexical analiz (BM25) + semantik sentez (embedding). Modern RAG boru hatları tam bu analiz→sentez (retrieve→generate) döngüsünü kullanır.

### 1.1. İki yönlü akış (bütünsel sentez)
```
[HERHANGİ BİR İŞ İLANI (JD)] → ANALİZ → {ağırlıklı keyword, requirement decomposition, intent, özet}
        ↓ [ADAY MASTER CV]
SENTEZ → {semantik kümeler, LSI genişletme, eylem-fiili XYZ cümleleri, ATS-optimize CV taslağı}
        ↓
SKORLAMA + GAP ANALİZİ → {hibrit ATS Match Score, eksik zorunlu keyword'ler, precision/recall/F1, öneriler}
        ↓ [REVİZYON DÖNGÜSÜ: skor < hedef ise sentez'e dön]
```
Bu döngü 100 ilanın her birine uygulanır; tek değişen girdi (JD + aday), **motorun mantığı sabittir** — istenen domain-agnostic engine budur.

---

## 2. Modern ATS'nin Doğrulanmış İşleyişi ve Mitlerin Düzeltilmesi
### 2.1. ATS boru hattının altı adımı (doğrulanmış)
1. **Metin çıkarımı/parsing:** Word XML ayrıştırma >%95; metin-PDF iyi; **taranmış/görüntü PDF OCR ile %70–85 — başlıca başarısızlık noktası.**
2. **Tokenizasyon + NER:** "Google"→Organizasyon, "2018–2022"→tarih; skill/araç yapısal alanlara yazılır.
3. **Inverted index:** "Python" araması terime bağlı aday ID'lerini anında getirir; recruiter Boolean kullanır (`Java AND (Spring OR Hibernate) NOT Junior`).
4. **Scoring/ranking:** Eski ATS = saf frekans; modern ATS (Workday AI katmanı, Greenhouse skorlama, iCIMS Talent Cloud) NLP ile "Python programming/development/scripting"i aynı yetkinlik sayar.
5. **Knockout questions:** Çalışma izni/lokasyon gibi ikili kurallar — otomatik retin asıl mekanizması.
6. **Recruiter review:** Sıralı liste insana sunulur; eşik üstü incelenir.

### 2.2. "%75 mit"i — dürüst düzeltme
Kaynak: ~2012'de tasfiye olmuş **Preptel** satış argümanı + 2018 CIO.com/Forbes (yazarı CV-hizmeti kurucusu, reklam). Karşı kanıt: **Enhancv'nin 25 ABD'li işe alımcı çalışması** — %92'si format/keyword/düşük skor nedeniyle otomatik reddetmiyor; otomatik ret yalnızca %8'de ve sadece çok spesifik rollerde. İşe alımcı **Jan Tegze:** "Başvuruların %90–95+'ı insan tarafından inceleniyor." Eski Amazon/Google işe alımcısı **Amy Miller:** ATS'in "dahi, AI-dolu araç" olduğu fikri "saçma."
**Çıkarım:** Asıl tehdit (a) **yanlış ayrıştırma** (tablo/sütun/grafik/header-footer parser'ı bozar; bir çalışmada iletişim bilgisi %25 vakada header/footer'da kaybolmuş), (b) **düşük sıralama** (400 aday içinde alt yarı = "işlevsel görünmez"). Sistem bu iki gerçek riske karşı optimize eder.

### 2.3. Kanıta dayalı format kuralları (motorun kısıtları)
- **Dosya:** `.docx` en güvenilir; modern ATS metin-PDF de okur; format belirtilmemişse `.docx`. Görüntü-PDF'ten kaçın. (Federal USAJobs: 27 Eylül 2025'ten itibaren 2 sayfa sınırı.)
- **Düzen:** Tek sütun; standart başlıklar; tablo/grafik/metin kutusu yok; iletişim ana gövdede.
- **Kronoloji:** Ters kronolojik veya hibrit.
- **Akronim:** Hem açık hem kısaltma — "Arama Motoru Optimizasyonu (SEO)".
- **Coverage > density:** Recruiter araması literaldir — "Tableau" hiç yazmadıysanız "veri görselleştirme"yi 10 kez yazsanız da bulunamayabilirsiniz.

---

## 3. ANALİZ Katmanı: Ayrıştırma Şeması, NLP Boru Hattı, TF-IDF ve BM25
### 3.1. Ön-işleme boru hattı
1. **Tokenization** 2. **Normalization/lowercasing** 3. **Stop-word removal** (dil-bağımlı) 4. **Lemmatization/stemming** ("managed/manage"→"manage"; lemmatizasyon tercih edilir) 5. **POS filtering** (fiiller VB: design/build/optimize; isimler NN: Python/ISO; spaCy ile "experience" sonrası yapılar self-supervised yakalanır) 6. **n-gram extraction** (1-3 gram; "supply chain management", "letter of credit" tek token).

### 3.2. Varlık çıkarımı (NER)
Çıkarılacak türler (genel şema, her sektörde aynı): **hard skills/araçlar/teknolojiler, soft skills, sertifika/lisans, kıdem/deneyim yılı, eğitim, sorumluluk fiilleri.** Modern yaklaşım transformer NER'dir (JobBERT, ESCOXLM-R, SkillSpan veri seti: 265 İngilizce profil, 12.5K span); Skill-LLM gibi ince-ayarlı LLM'ler SOTA'yı aşar.

### 3.3. Gereksinim ayrıştırma + niyet tespiti
- **Modality:** "required/must"→ağırlık 1.0; "preferred/plus"→~0.3 (Çince kaynak: "CPA sertifikası" 1.0, "VBA makro" 0.3).
- **Positional weight:** İtalyanca Jobiri kaynağı modern ATS'lerin "azalan ilgililik mantığı" kullandığını, **ilk 100–150 kelimenin yüksek ağırlık** taşıdığını belirtir.

### 3.4. TF-IDF (matematiksel çekirdek 1)
$$\mathrm{tf}(t,d)=\frac{f_{t,d}}{\sum_{t'} f_{t',d}};\quad \mathrm{idf}(t)=\log\frac{N}{df_t}\ \left(\text{yumuşatılmış }\log\frac{N}{1+df_t}\right);\quad w_{t,d}=\mathrm{tf}\times\mathrm{idf}$$
Ağırlık belge-içi sıklıkla artar, corpus yaygınlığıyla azalır. Corpus = aday havuzu/sektör ilanları; "Kubernetes" yüksek, "team player" düşük ağırlık alır.

### 3.5. BM25 / Okapi BM25 (matematiksel çekirdek 2)
$$\text{BM25}(D,Q)=\sum_{i=1}^{n}\mathrm{IDF}(q_i)\cdot\frac{f(q_i,D)\cdot(k_1+1)}{f(q_i,D)+k_1\left(1-b+b\cdot\frac{|D|}{\text{avgdl}}\right)}$$
- **$k_1$ (saturation):** TF katkısının doyma hızı; tipik **1.2–2.0** (Lucene varsayılanı 1.2). Doyum fonksiyonu stuffing'i matematiksel cezalandırır — tekrarlar asimptotik $k_1+1$'e yaklaşır.
- **$b$ (length norm), 0–1:** varsayılan **0.75**; aynı terimi 3 kez geçiren iki belgeden kısa olan daha yüksek skor (öz CV ödüllenir).
- **TF-IDF'ten üstün:** doyum + uzunluk normalizasyonu; Elasticsearch/Lucene fiili standardı. Çince kaynak ATS skorlamasını "TF-IDF varyantı" olarak doğrular.

### 3.6. ANALİZ çıktısı (doldurulacak alanlar)
```
analiz = { weighted_keywords:[{term,tf_idf,bm25_weight,modality,positional_weight}],
  must_have:[...], nice_to_have:[...],
  entities:{hard_skills,soft_skills,tools,certifications,seniority,education},
  action_verbs:[...], skill_nouns:[...], intent_summary:"rolün özü" }
```

---

## 4. SEMANTİK Katman: LSA/SVD, SBERT/STS, Kosinüs ve Ontolojiler
### 4.1. LSA/LSI + SVD (matematiksel çekirdek 3)
Deerwester ve ark. (1988–90). Adımlar: (1) Document-Term Matrix $A$ (TF-IDF hücreler); (2) **SVD:** $A=U\Sigma V^{T}$ ($U$=terim-kavram, $\Sigma$=tekil değerler, $V^T$=kavram-belge); (3) **Truncated SVD:** en büyük $r$ tekil değer → $m$ terimden $r$ latent kavrama indirgeme. **Eşanlamlılık/çok anlamlılık** sorunlarını hafifletir. Sınırı: doğrusaldır, SVD büyük veride pahalı (çözüm: Randomized SVD).

### 4.2. SBERT + STS (matematiksel çekirdek 4)
Reimers & Gurevych (EMNLP 2019): BERT'i **siamese/triplet** ağlarla değiştirip kosinüsle karşılaştırılabilir cümle gömmeleri üretir. 10K cümlede en benzer çift: BERT ~65 saat → **SBERT ~5 saniye**; yedi **STS** görevinde InferSent'e +11.7, USE'ye +5.5 puan. Mimari: BERT + **mean pooling** → 768-boyut; STS regresyon hedefi (kosinüs vs. etiket MSE). CV'de "AARRR ile kullanıcı büyümesi" ↔ JD'deki "user retention" bağını yakalar. Çok dilli conSultantBERT, CV-ilan eşleşmesinde hem TF-IDF hem ham BERT'i geçer.

### 4.3. Cosine Similarity (matematiksel çekirdek 5)
$$\cos\theta=\frac{\mathbf{A}\cdot\mathbf{B}}{\lVert\mathbf{A}\rVert\lVert\mathbf{B}\rVert}=\frac{\sum A_iB_i}{\sqrt{\sum A_i^2}\sqrt{\sum B_i^2}}$$
TF-IDF'te [0,1]; embedding'de [−1,1]; 1=özdeş. "Job-Resume Matching" çalışmalarının çekirdeği (TF-IDF+Cosine veya SBERT+Cosine). CLiC-it 2025: çok dilli embedding kosinüsü TF-IDF ve ham BERT'i geçer.

### 4.4. Ontoloji genişletme (ESCO, O*NET, SFIA)
- **ESCO:** ~3.000 meslek, ~13.000+ beceri; **26 Avrupa dili + Arapça** — çok dilli sistem için ideal.
- **O*NET:** ABD Çalışma Bakanlığı veritabanı; **SFIA:** BT becerileri altın standardı.
- Yöntem: skill'i ontolojiye fuzzy/embedding ile eşle; benzerlik ağırlığı $\alpha$ eşiğini geçenleri tut. "supply chain" ↔ "tedarik zinciri" ↔ "lojistik" genişletmesini **stuffing olmadan** kontrollü yapar.

---

## 5. Hibrit ATS Match Score: Tam Formül, Ağırlık Ayarı, Worked Example, Precision/Recall/F1
### 5.1. Bileşenler ([0,1]'e normalize)
- **(a) Lex:** $\text{Lex}=\dfrac{\text{BM25}(D_{CV},Q_{JD})}{\text{BM25}_{\max}(Q_{JD})}$
- **(b) Sem:** $\text{Sem}=\max(0,\cos(\vec{v}_{CV},\vec{v}_{JD}))$ (madde düzeyinde maximum-over-chunks da olabilir)
- **(c) Cov (recall-odaklı):** $\text{Cov}=\dfrac{\sum_{j\in M} w_j\,\mathbb{1}[j\in CV]}{\sum_{j\in M} w_j}$ ($w_j$=modality×positional)
- **(d) Parse:** ayrıştırılabilirlik kontrol listesi skoru
- **(e) Stuffing:** anormal yoğunluk/tekrar cezası

### 5.2. Birleşik skor
$$\boxed{\ \text{Score}=\alpha\cdot\text{Lex}+\beta\cdot\text{Sem}+\gamma\cdot\text{Cov}+\delta\cdot\text{Parse}-\zeta\cdot\text{Stuffing}\ }$$
$\alpha+\beta+\gamma+\delta=1$; $\zeta$ ayrı ceza. **Önerilen defaultlar:** $\alpha=0.30$ (literal recruiter araması kritik), $\beta=0.25$, $\gamma=0.30$ (zorunlu kapsam en yüksek), $\delta=0.15$, $\zeta=0.20$. (Alman kaynağı pratik füzyonu "0.6·dense+0.4·sparse" örnekler.)
**Alternatif füzyon — RRF:** $\text{RRF}(d)=\sum_s\frac{1}{k+\text{rank}_s(d)}$ (tipik $k=60$); ölçek uyumsuzluğunu çözer. Üretimde **cross-encoder reranker** (ColBERT/LLM) ilk 20 adayı yeniden sıralar.

### 5.3. Ağırlık ayarı
Grid-search/held-out validasyon ile $(\alpha,\beta,\gamma,\delta,\zeta)$ ve $(k_1,b)$ → nDCG@k/MAP maksimize. **Dynamic Alpha Tuning:** nadir-terimli JD'de $\alpha$ yükselt.

### 5.4. Normalizasyon
Min-max: $x'=\frac{x-\min}{\max-\min}$; Z-score: $z=\frac{x-\mu}{\sigma}$ (aday havuzunda göreli sıralama).

### 5.5. Worked example
10 zorunlu keyword; $\text{Cov}=0.82$, $\text{Lex}=0.74$, $\text{Sem}=0.69$, $\text{Parse}=1.0$, $\text{Stuffing}=0.10$:
$$\text{Score}=0.30(0.74)+0.25(0.69)+0.30(0.82)+0.15(1.0)-0.20(0.10)=0.222+0.1725+0.246+0.15-0.02=\mathbf{0.7705}\approx\%77$$
**Eşik yorumu:** %75–85 = "mülakata hazır"; **>%90 = aşırı-optimizasyon (stuffing) sinyali**; <%50 = ciddi iyileştirme. (İspanyolca Minova kaynağı da optimal %75–85, >%90 "olası keyword aşırı yüklemesi" der.)

### 5.6. Precision/Recall/F1 + gap analizi
$M$=JD zorunlu terimleri, $C$=CV terimleri:
$$P=\frac{|C\cap M|}{|C|},\quad R=\frac{|C\cap M|}{|M|},\quad F_1=\frac{2PR}{P+R}$$
- **Recall** = JD zorunluluk kapsamı (eksik must-have = gap, recall düşürür).
- **Precision** = CV terimlerinin ne kadarının ilgili olduğu (düşük = alakasız/şişirilmiş = stuffing).
- İnce-ayarlı LLM eşleştiricilerde F1 ~%90 (örn. fine-tuned Phi-4: %90.62).
- **Gap çıktısı:** $M\setminus C$ = "eksik zorunlu keyword listesi" → sentez katmanına revizyon talimatı.

---

## 6. SENTEZ Katmanı: Kümeleme, LSI Genişletme, E-E-A-T, XYZ/CAR/STAR, Tutarlılık
Yapıcı faz — "düğümü bağlama" (Descartes'ın sentez kuralı).

### 6.1. Semantik kümeleme
**k-means** (sabit $k$) veya **hiyerarşik** kümeleme embedding üzerinde; **LDA** topic modeling ile JD'nin gizli temaları çıkarılıp CV alt-başlıklarına eşlenir. İlgili beceriler gruplanır (ör. "Dış Ticaret Operasyonları: Incoterms, akreditif, gümrük") → hem ATS bölüm-ayrıştırması hem insan okunabilirliği.

### 6.2. LSI/embedding genişletme — STUFFING OLMADAN
ESCO/O*NET + embedding komşuluğundan kontrollü varyant (R.E.A.L.: Read-Extract-Apply-Layer). **Kısıt:** tekrar değil, varyasyonla semantik derinlik. Bir terimin "Skills" (iddia) + "Experience" (kanıt) bölümlerinde birer kez geçmesi, tek blokta üç kez geçmesinden yüksek skor alır (bağlam penceresi). **Yoğunluk:** 1–3% birincil, >%5 stuffing; ama en güçlü modern kaynaklar "**density yanlış birincil metriktir; coverage+proof doğrudur**" der. Pratik: önemli her keyword **2–3 kez farklı bölümde**, toplam **15–25 ilgili keyword** dağıtılmış.

### 6.3. Eylem-fiili eşlemesi + E-E-A-T
POS-filtreli action verb'ler her cümlenin başına (led/developed/optimized/negotiated/reduced). **E-E-A-T** (Google, Aralık 2022'de E-A-T'ye Experience ekledi; **rater kılavuzu, doğrudan sıralama faktörü DEĞİL**): **Experience** (birinci-elden gerçek deneyim), **Expertise** (kanıtlanabilir bilgi/sertifika), **Authoritativeness** (tanınma/liderlik kapsamı), **Trustworthiness** (Google'a göre **en önemli üye** — "güvenilmez sayfalar ne kadar Deneyimli/Uzman/Otoriter görünse de düşük E-E-A-T'ye sahiptir"). CV'de Trust = doğruluk, abartısızlık, savunulabilir metrikler; sahte beceri/keyword *yok* (mülakatta çöker).

### 6.4. Başarı cümlesi formülleri
**Google XYZ** (Laszlo Bock): **"Accomplished [X] as measured by [Y], by doing [Z]"** — X=sonuç (güçlü fiil), Y=metrik, Z=yöntem. Örnek: "Satışları %25 artırdım, Q1'de yeni iş kolu başlatarak." **CAR** (Context-Action-Result) ve **STAR** (Situation-Task-Action-Result): STAR mülakat anlatısı, XYZ CV cümlesi içindir. Japonca kaynak CAR'ı metriklerle örnekler (churn %8→%5; ilk yanıt 48s→6s). **Niceleme:** her cümlede ≥1 sayı; "önemli ölçüde artırdım" değil "%45 artırdım". Madde ≤1–2 satır.

### 6.5. Anlatısal tutarlılık
**Üst özet:** ilk 3–5 cümle en yüksek ağırlıklı keyword'leri + rolün özünü yansıtır (ilk 100–150 kelime yüksek ağırlık). **Tutarlılık:** CV↔LinkedIn↔kapak mektubu aynı standart unvanları kullanmalı (dahili/yaratıcı unvanları sektör-standardına çevir). **"Robot+insan testi":** keyword skorunu geçmeli VE 6 saniyede taranıp değer iletmeli.

### 6.6. SENTEZ çıktısı (doldurulacak alanlar)
```
sentez = { semantic_clusters:[{cluster_label,member_skills}],
  lsi_expansions:{keyword:[varyantlar]},
  achievement_bullets:[{verb,X,Y_metric,Z_method,source_role}],
  summary:"üst özet (ilk 100-150 kelime)",
  section_map:{Summary,Skills,Experience,Education,Certifications} }
```

---

## 7. Yeniden Kullanılabilir Algoritmik Boru Hattı (100 İlana Uygulanan Motor — Pseudocode)
```
GİRDİ: job_posting (JD), candidate_master_cv, corpus (sektör ilanları/CV havuzu),
       skill_ontology (ESCO/O*NET), embedding_model (SBERT), weights(α,β,γ,δ,ζ,k1,b)

# ——— ANALİZ ———
1.  text = parse_and_clean(JD)                       # tokenize, lowercase, stop-word, lemmatize
2.  ngrams = extract_ngrams(text, n=1..3)
3.  entities = NER(text) → {skills, tools, certs, seniority, education, verbs}
4.  for term in entities ∪ ngrams:
        tfidf[term]  = tf(term,JD) * idf(term,corpus)
        bm25[term]   = BM25_term(term, JD, corpus, k1, b)
        modality     = classify_must_vs_nice(term, JD)      # 1.0 / 0.3
        pos_weight   = positional_weight(term, JD)           # ilk 100-150 kelime ↑
        w[term]      = bm25[term] * modality * pos_weight
5.  must_have = {t : modality(t)=1.0};  nice = {t : modality(t)=0.3}
6.  analysis_summary = summarize_intent(JD)
7.  ÇIKTI-A: {weighted_keywords:w, must_have, nice, entities, analysis_summary}

# ——— SENTEZ ———
8.  clusters   = cluster(embed(keywords), method=kmeans|hierarchical)
9.  topics     = LDA(JD)
10. expansions = {kw: ontology_neighbors(kw) ∪ embedding_synonyms(kw)}   # stuffing yok
11. for each relevant experience in candidate_master_cv:
        bullet = XYZ(verb=map_action_verb(JD), X=result, Y=metric, Z=method)
12. cv_draft = assemble(summary, clusters→Skills, bullets→Experience, Education, Certs)
13. ÇIKTI-S: {clusters, expansions, achievement_bullets, summary, cv_draft}

# ——— SKORLAMA + GAP ———
14. Lex  = BM25(cv_draft, JD) / BM25_max(JD)
15. Sem  = max(0, cos(embed(cv_draft), embed(JD)))
16. Cov  = Σ wj·1[j∈cv_draft] / Σ wj    over must_have
17. Parse = parse_checklist_score(cv_draft)
18. Stuffing = density_anomaly(cv_draft, JD)
19. Score = α·Lex + β·Sem + γ·Cov + δ·Parse − ζ·Stuffing      # min-max normalize edilmiş
20. P,R,F1 = prf(cv_draft_terms, must_have)
21. gap = must_have \ cv_draft_terms
22. ÇIKTI-G: {Score, P, R, F1, gap, recommendations}

# ——— REVİZYON DÖNGÜSÜ ———
23. if Score < target(0.75) OR gap ≠ ∅:  feed gap → step 10–13 (sentez tekrar); goto 14
24. else: return final_cv, full_report
```

### 7.1. Her ilan için AI araçlarının dolduracağı standart veri alanları
| Alan | İçerik |
|---|---|
| **keywords** | ağırlıklı liste {term, bm25_weight, modality, positional_weight} |
| **analysis** | requirement decomposition, entities, must/nice ayrımı, niyet |
| **summary** | rolün özü + üst-özet taslağı (ilk 100–150 kelime) |
| **synthesis** | semantik kümeler, LSI genişletmeler, XYZ/CAR cümleleri, section_map |
| **match_score** | hibrit Score + bileşenler (Lex, Sem, Cov, Parse, Stuffing) |
| **gap_analysis** | eksik zorunlu keyword'ler + precision/recall/F1 + somut öneriler |

---

## 8. Çok Dilli Kaynak Sentezi (13+ dil — farklı entelektüel gelenekler)
Sistem, IR/NLP/ATS/özgeçmiş bilimi üzerine çok dilli kaynakların sentezidir; çıktı Türkçedir.
- **EN (İngilizce):** Okapi BM25 (Wikipedia/Robertson-Spärck Jones; Elastic, Cornell, NEU ders notları), SBERT (Reimers & Gurevych, EMNLP 2019/arXiv 1908.10084), LSA (Landauer/Foltz/Laham 1998; IBM; Wikipedia), Jobscan, TopResume, Teal, Interview Guys (75% mit debunk), Enhancv çalışması (itbrief.co.uk, hr-gazette), Google XYZ (Teal/Simplify/Jobseeker), Google E-E-A-T (developers.google.com Search Central, Aralık 2022); SkillSpan/Skill-LLM (arXiv 2410.12052), ESCO matching (arXiv 2512.03195, 2601.09119).
- **FR (Fransızca):** Descartes analiz/sentez — culturesciences.fr, philosophes.org, philosciences.com, persée.fr ("dénouer/décomposer/composer un tout"), Deleuze (utime.unblog).
- **DE (Almanca):** Hibrit lexical+semantik arama, RRF, ağırlık füzyonu (it-glossary.com, Elastic.de, ralfdodler.de — "0.6·dense+0.4·sparse", k1 0.9–1.5, b 0.5–0.9).
- **ZH (Çince):** ATS = "TF-IDF varyantı", Word2Vec/BERT semantik, modality ağırlıkları (resumemakeroffer, zhihu/Resume-Matcher+Qdrant, CSDN, Hays-China, Sohu — %70 hizalama eşiği).
- **RU (Rusça):** Semantik analiz (React=React.js), 2–3% yoğunluk, parsing+ranking (habr.com, banki.ru, hirehi.ru, brainhire.ru).
- **JA (Japonca):** CAR formülü + metrikler, .docx tercihi, keyword matching (somali.co.jp, rirekisho.jp, job-cruise.com, hireplanner.com).
- **ES (İspanyolca):** BERT semantik %15.85 daha iyi, NER %88–95, optimal %75–85 eşleşme (caixabank.com, minova.ai, stylingcv.com, cvmaker.es, cvscore.net).
- **KO (Korece):** Parsing→keyword matching→scoring→ranking, STAR/nicel sonuç, Workday %39 pazar payı (jobkorea.co.kr, velog.io, passcheck.kr, mylivecv.com).
- **AR (Arapça):** ATS keyword'leri JD'den çıkar+entegre et, tablo/sütun parser'ı bozar (sabbar.com/blog/ats-cv, ats-conditions; wdeftksa.com — %88 işveren/%99 Fortune 500).
- **PT (Portekizce):** Algoritma keyword'e göre skor atar, yüksek skor önceliklenir (jobconvo.com, onlinecurriculo.com).
- **IT (İtalyanca):** Çok-faktörlü ranking (frekans+bağlamsal konum+semantik yakınlık+göreli yoğunluk), ilk 100–150 kelime ağırlık, NLP semantik parsing (onlinecv.it, jobiri.com, it.indeed.com).
- **HI/IN (Hintçe/Hindistan):** ATS parsing+keyword optimizasyonu (Indeed Hindi, Novoresume, Jobscan).
- **Akademik çok-dilli:** Kazakça TF-IDF eşanlamlı uzantısı (arXiv 2211.12364), SIF ağırlıklandırma (arXiv 1902.09875).

---

## ÖNERİLER (Aşamalı, Eyleme Dönük)
**Aşama 0 — Altyapı kurulumu (bir kez):** (1) Master CV oluştur (tüm başarılar, nicel metriklerle). (2) Embedding modeli seç (SBERT/çok dilli model — domain'e ince-ayar ideal). (3) ESCO (çok dilli) veya O*NET ontolojisini bağla. (4) Ağırlıkları defaultlarla başlat ($\alpha$=0.30, $\beta$=0.25, $\gamma$=0.30, $\delta$=0.15, $\zeta$=0.20; $k_1$=1.5, $b$=0.75).

**Aşama 1 — Her ilan için (100×):** Bölüm 7 boru hattını çalıştır → 6 veri alanını doldur. **Önce coverage'ı garanti et** (zorunlu keyword'lerin tümü, doğru bağlamda, gerçekten sahip olduklarınız). Sonra semantik zenginleştir.

**Aşama 2 — Skor + revizyon:** Score < 0.75 ise gap listesini sentez'e geri besle. Hedef **%75–85**. **Asla %90+ için keyword doldurma** — ceza üretir.

**Aşama 3 — İnsan testi:** Final CV'yi düz metne yapıştır (parser simülasyonu) + sesli oku (sözlük gibiyse aşırı-optimize). Tek sütun, .docx, standart başlık doğrula.

**Aşama 4 — Kalibrasyon (10–20 ilandan sonra):** Geri çağrı (callback) verisi varsa ağırlıkları grid-search ile yeniden ayarla; nDCG/F1 izle.

**Eşik/karar değiştiren ölçütler:** Callback oranı düşükse → $\gamma$ (coverage) ve Parse'a ağırlık ver. Çok teknik/nadir-terimli sektörlerde → $\alpha$ (lexical) yükselt. Çok dilli/çapraz-terminolojili rollerde → $\beta$ (semantik) + ontoloji genişletmesini güçlendir.

---

## CAVEATS (Dürüst Sınırlamalar)
1. **ATS iç mekanizmaları tescillidir (proprietary) ve kısmen bilinemez.** Workday/Greenhouse/iCIMS'in tam skorlama formülleri açık değildir; bu sistem *kamuya açık kanıt + IR teorisi*nden türetilmiş bir **yaklaşıklamadır (proxy)**, birebir kopya değil. ATS başına davranış değişir (USAJobs/USA Staffing tamamen farklı).
2. **"%75 reddedilir" miti yanlıştır** ama tersi de doğru değil — kötü parse/düşük sıralama gerçek risktir. Sistem "garantili mülakat" sağlamaz; ATS yalnızca *ilk kapıdır*, insan kararı ve networking belirleyicidir (Indeed: optimizasyon+networking = 3.2× daha fazla mülakat).
3. **Aşırı-optimizasyon geri teper.** Modern ATS density anomalisi/beyaz metin/tekrarı tespit eder ve cezalandırır; %90+ skor genelde stuffing işaretidir. Coverage+proof > density.
4. **Semantik skor iyi embedding'e bağlıdır.** Zayıf/yanlış-domain embedding semantik bozulma üretir; çok dilli rollerde domain'e ince-ayar şarttır. LSA doğrusaldır (doğrusal-olmayan örüntüleri kaçırır); SVD büyük veride pahalıdır.
5. **Etik sınır mutlaktır.** Sahte keyword/beceri eklemeyin — E-E-A-T'nin "Trust" piları en önemlisidir ve teknik mülakatta çöker. Keyword'ler yalnızca *gerçekten sahip olunan* deneyimi *doğru* yansıttığında değer üretir.
6. **Kaynak kalitesi karışıktır.** ATS-optimizasyon kaynaklarının çoğu ticarei CV-araç sitelerridir (çıkar çatışması olası); matematik/IR iddiaları akademik kaynaklarla (arXiv, ACL, Wikipedia, üniversite ders notları) çapraz-doğrulanmıştır. İstatistikler (%98 Fortune 500, %88 işveren) sıkça vendor-kaynaklıdır; yön doğru, kesin rakamlar ihtiyatla okunmalı.
7. **Ağırlıklar evrensel-optimal değildir.** Önerilen $\alpha,\beta,\gamma,\delta,\zeta$ defaultları başlangıç noktasıdır; her sektör/dil için validasyon verisiyle ayarlanmalıdır.