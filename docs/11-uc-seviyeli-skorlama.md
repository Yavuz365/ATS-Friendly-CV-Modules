# docs/11 — Üç-Seviyeli ATS Skorlama Matematiği

> **Legacy diagnostic:** Eşikler ticari ATS veya “güvenle gönderilebilir” kanıtı değildir.

> Level 1 → Level 2 → Level 3 skorlama zincirinin tam matematiksel tanımı.

## 1. Temel Hibrit Skor (Tüm Seviyelerde Kullanılır)

```
H(CV, JD) = LangGate × ParseGate × clamp(α·Lex + β·Sem + γ·Cov − ζ·Stuff, 0, 1)
```

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| α | 0.35 | TF-IDF kosinüs (leksikal) ağırlığı |
| β | 0.30 | SBERT kosinüs (semantik) ağırlığı |
| γ | 0.35 | Zorunlu terim kapsamı ağırlığı |
| ζ | 0.20 | Şişirme (stuffing) ceza katsayısı |
| k₁ | 1.5 | BM25 TF doyum parametresi |
| b | 0.75 | BM25 uzunluk normalizasyonu |

**SBERT yoksa:** β → 0, α ve γ orantılı genişler: α' = α/(α+γ), γ' = γ/(α+γ)

## 2. Level 1 — Araç-CV Kapısı

Tek bir AI aracının ürettiği tam CV'nin JD eşleşmesi.

```
L1(tool_i) = H(CV_i, JD)
Geçiş: L1 ≥ τ   (τ = 0.70)
```

- τ'nun altındaki araçlar Level 2'ye taşınmaz
- τ kalibre edilebilir: gevşek (0.60) veya sıkı (0.80)

## 3. Level 2 — Sekiz-Parça En-İyi + Dikiş Cezası

### 3a. Bölüm seçimi

Her bölüm `s ∈ S = {summary, exp_1..4, skills, edu, cert}` için:

```
best(s) = argmax_{tool_i} H(section_s(CV_i), JD)
```

### 3b. Birleştirme

```
CV_combined = concat(best(s) for s in S)
```

### 3c. Dikiş cezası

```
dominant_ratio = max(count_per_tool) / |S|
seam_penalty = κ × (1 − dominant_ratio)    (κ = 0.15)
```

### 3d. Final L2 skoru

```
L2 = H(CV_combined, JD) − seam_penalty
L2 = max(0, L2)
```

## 4. Level 3 — Kategori Robustness

Birleşik CV'yi N farklı ilana (aynı kategori) karşı test eder.

```
scores = [H(CV_combined, JD_j) for j in 1..N]
μ = mean(scores)
σ = std(scores)
robust ⟺ σ ≤ 0.10
```

| σ değeri | Yorum |
|----------|-------|
| ≤ 0.05 | Mükemmel robustness — CV kategoriye çok iyi uyarlanmış |
| 0.05 – 0.10 | Düşük varyans tanısı — gönderim veya outcome garantisi değil |
| 0.10 – 0.15 | Orta — bazı ilanlarda zayıf kalabilir |
| > 0.15 | Aşırı uyarlanmış — tek ilana optimize edilmiş, genelleme zayıf |

## 5. Dil Kapısı (LangGate)

```
jd_lang = detect_language(JD)
purity = language_purity(CV, jd_lang)
LangGate = min(1.0, purity / p₀)    (p₀ = 0.85)
```

- Saflık p₀ üstünde → LangGate = 1.0 (ceza yok)
- Saflık p₀ altında → orantılı ceza
- Türkçe ilana İngilizce karışık CV → skor düşer

## 6. Teşhis Bantları (A11 fix: "mülakata hazır" garantisi kaldırıldı — bu bir hizalanma sinyalidir, işe alım sonucu tahmini değildir)

| Bant | Aralık | Aksiyon |
|------|--------|---------|
| 🟢 Yüksek lexical hizalanma | Profile bağlı | Yalnız tanı; gönderim veya outcome kararı değil |
| 🟡 Hedefin Altında | %50 – 75 | Sentez (revizyon) turu |
| 🔴 Ciddi | < %50 | Framework CV gözden geçir |
| ⚠️ Aşırı Optimizasyon | > %90 | Şişirme/geri tepme riski |

## 7. Motor Kullanımı

```python
from ats_engine.multilevel import level1_gate, level2_final, level3_category, lang_gate

# Level 1
l1 = level1_gate(jd_text, cv_text, must_terms)
if not l1["passed"]:
    print(f"Elendi: {l1['score']:.0%} < τ={l1['threshold']}")

# Level 2
l2 = level2_final(jd_text, tool_sections, must_terms)
print(f"Birleşik: {l2['final_score']:.0%} (dikiş cezası: {l2['seam_penalty']:.3f})")

# Level 3
l3 = level3_category(combined_cv, [jd1, jd2, jd3], must_terms)
print(f"Robustness: μ={l3['mean']:.0%}, σ={l3['std']:.3f}, robust={l3['robust']}")

# Dil kapısı
lg = lang_gate(cv_text, jd_text)
print(f"LangGate: {lg:.3f}")
```
