# 00 — Sistem Mimarisi

> **Legacy metodoloji (v1.x):** Kanonik runtime ve ürün sözleşmesi için
> `docs/decisions/ADR-001-evidence-first-v2.md`, `schemas/v2/` ve testler esas alınır.

## Tek cümlede
Bir iş ilanını **çöz** (ANALİZ), adayın gerçek kariyer verisiyle **yeniden bağla** (SENTEZ), sonra **ölç ve doğrula** (SKOR + GAP) — gerekirse yalnızca kapatılabilir gap üzerinde döngüyü tekrarla.

## Katmanlar
```
                 ┌──────────────────────────────────────────┐
   İŞ İLANI (JD) │  Katman 0  Alım & Mod + Provenans Defteri  │
        │        │  Katman 1  Bütünsel kavrama (ön-sentez)     │
        ▼        │  Katman 2  ANALİZ — 7 katmanlı ayrıştırma   │  ← jd_parser.py
   FRAMEWORK CV  │  Katman 3  SKOR & GAP                       │  ← scoring.py
   (kanıt bank.) │  Katman 4  SENTEZ — küme + XYZ + provenans  │  ← synthesis.py
        │        │  Katman 5  Doğrulama & Teslim (6 alan)      │  ← report.py
        ▼        └──────────────────────────────────────────┘
   6 ALANLI ÇIKTI: keywords · analysis · summary · synthesis · match_score · gap_analysis
```

## Diyalektik döngü (6 vuruş)
| Vuruş | Ad | CV motorundaki karşılığı |
|---|---|---|
| 0 | Ön-sentez | İlanın özünü tek cümleyle yakala |
| 1 | Ayrıştırma | JD'yi 7 katmana çöz |
| 2 | Analiz | BM25/TF-IDF + modality + konum ağırlığı |
| 3 | Eşleştirme | JD terimleri ↔ kanıt bankası; skor + gap |
| 4 | Yeniden sentez | Kümeleme + XYZ cümleleri + üst özet |
| 5 | Doğrulayıcı analiz | Provenans kontrolü + skoru yeniden hesapla |

**Çekirdek ilke:** Analiz çözer, sentez bağlar; hiçbiri tek başına yetmez. Saf analiz anlamı kaybeder; saf sentez temelsiz kalır. Gerçek kavrayış, parça↔bütün arasındaki tükenmeyen döngüdür (hermenötik döngü).

## Kod ↔ kavram eşlemesi
| Kavram | Modül |
|---|---|
| 7 katmanlı ayrıştırma | `engine/ats_engine/jd_parser.py` |
| BM25 / TF-IDF / kosinüs | `engine/ats_engine/bm25.py`, `scoring.py` |
| Eşanlamlı-duyarlı kapsama, LSI | `engine/ats_engine/lexicons.py` (+ `data/skill_synonyms.json`) |
| Kanıt bankası / provenans | `engine/ats_engine/evidence_bank.py` |
| Kümeleme, XYZ/CAR, gap ayrımı, durma kuralı | `engine/ats_engine/synthesis.py` |
| 6 alanlı rapor | `engine/ats_engine/report.py` |
| Aksiyon-fiil kütüphanesi (Grammarly) | `engine/data/action_verbs.json` |
