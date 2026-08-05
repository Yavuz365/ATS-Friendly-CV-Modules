# docs/10 — Sekiz-Parça Skorlama + QA Pipeline

> **Legacy diagnostic:** Tek skor ürün kararı değildir; QA hataları v2’de `ERROR/REVIEW` olarak görünür.

> CV'yi 8 bölüme ayırıp her bölümü ayrı skorlama ve kalite kontrol süreci.

## 1. Sekiz Bölüm

| # | Bölüm | İngilizce | Açıklama |
|---|-------|-----------|----------|
| 1 | Özet | Summary | Kariyer özeti / profesyonel profil |
| 2 | Deneyim 1 | Experience 1 | En güncel / en ilgili pozisyon |
| 3 | Deneyim 2 | Experience 2 | İkinci pozisyon |
| 4 | Deneyim 3 | Experience 3 | Üçüncü pozisyon |
| 5 | Deneyim 4 | Experience 4 | Dördüncü pozisyon |
| 6 | Beceriler | Skills | Teknik + genel yetkinlikler |
| 7 | Eğitim | Education | Üniversite + kurslar |
| 8 | Sertifikalar | Certifications | Profesyonel sertifikalar |

## 2. Bölüm-Bazlı Skorlama

Her AI aracı her bölüm için ayrı bir metin üretir. Motor:

```python
from ats_engine.multilevel import level2_best_of

tool_sections = {
    "chatgpt":   {"summary": "...", "experience_1": "...", ...},
    "claude":    {"summary": "...", "experience_1": "...", ...},
    "gemini":    {"summary": "...", "experience_1": "...", ...},
    "copilot":   {"summary": "...", "experience_1": "...", ...},
    "perplexity":{"summary": "...", "experience_1": "...", ...},
}

result = level2_best_of(jd_text, tool_sections, must_terms)
# result["best_sections"]["summary"]["tool"] → "claude"
# result["best_sections"]["summary"]["score"] → 0.82
```

## 3. En-İyi Seçim Kuralları

Her bölüm için:
1. JD'ye karşı `ats_match_score()` hesaplanır
2. En yüksek skoru alan araç seçilir
3. Eşit skor → ilk gelen (araç sırası değişmez)

## 4. Birleştirme + Dikiş Cezası

Farklı araçlardan gelen parçalar birleştirildiğinde ton/stil tutarsızlığı riski:

```
Dikiş Cezası = κ × (1 − dominant_tool_oranı)
κ = 0.15 (sabit)
```

**Örnek:**
- 8 parçadan 6'sı Claude → dominant oran = 0.75 → ceza = 0.15 × 0.25 = 0.0375
- 8 parçadan 3'ü farklı araç → dominant oran = 0.375 → ceza = 0.15 × 0.625 = 0.09375

## 5. QA Pipeline

Birleşik CV'nin son kalite kontrolü:

| Adım | Kontrol | Araç |
|------|---------|------|
| 1 | Parse güvenlik skoru | `cv_parser.parse_safety_score()` |
| 2 | Dil tutarlılığı | `multilevel.lang_gate()` |
| 3 | Provenans doğrulama | `evidence_bank.provenance_check()` |
| 4 | Anti-stuffing kontrolü | `synthesis.anti_stuffing_report()` |
| 5 | Grammarly AI-detector | Harici (docs/13) |
| 6 | Final skor | `scoring.ats_match_score()` |

## 6. Dış Doğrulama

Motorun skorunu harici araçla karşılaştır:
- **Jobscan** ATS Match Score ile `ats_match_score()` arasında ±10 puan fark kabul edilebilir
- Daha fazla fark → ağırlık kalibrasyonu (α, β, γ, ζ) gözden geçirilmeli
