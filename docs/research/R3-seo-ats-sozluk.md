# R3 — SEO/ATS Sözlüğü (Grammarly kaynağından ATS-ilgili damıtım)

> Kaynak: `Keyword_Optimization_-_Grammarly_docx.md`. Burada yalnızca ATS-CV motoruyla doğrudan ilgili alt küme, indeks olarak tutulur (tam metin değil). Operasyonel veri: `engine/data/action_verbs.json`, `engine/data/skill_synonyms.json`.

## Eşleştirme & benzerlik
- TF-IDF, BM25 (k1/b), kosinüs benzerliği, RRF füzyonu.
- Fuzzy matching: **Jaccard**, **Levenshtein**; **Skill Normalization**.
- LSI / örtük anlamsal indeksleme; semantik (SBERT) eşanlamlı/parafraz.

## Cümle & dil
- **XYZ / CAR** formülleri; quantification pattern (sayı/%/süre).
- 700+ aktif eylem fiili (kategorize: liderlik, başarı, optimizasyon, analiz, iletişim, inşa…).
- Active vs passive; Flesch-Kincaid okunabilirlik; ton/formellik eşleşmesi.

## ATS uyum
- Parse_gate / format okunabilirliği; keyword stuffing cezası (density anomaly).
- E-E-A-T (Trust), provenans/dürüstlük.
- Coverage > density; evrensel eşik yoktur. Threshold yalnız sürümlü evaluation profile
  içinde tanı amaçlı kullanılabilir.

> Not: Bu sözlük "ne aktarıldı + nereye" indeksidir; karşılaştırmanın gerekçesi `docs/05-grammarly-entegrasyonu.md`'dedir.
