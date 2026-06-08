# Çıktı Şablonu — 6 Sabit Alan (her ilan için)

Her iş ilanı bu altı alanı üretir. Toplu modda her ilan tabloda bir satır olur; tek-ilan modunda tam form + FINAL CV verilir.

```json
{
  "ilan_id": "JD-001",
  "keywords": [
    {"term": "akreditif (letter of credit)", "modality": "zorunlu", "positional_weight": 1.3, "freq": 2}
  ],
  "analysis": {
    "identity": {"title": "", "seniority": "", "sector": "", "location": "", "company": "", "work_mode": "", "language_req": ""},
    "must_have": [{"term": "", "type": "skill|tool|cert|years|education|legal", "modality": 1.0}],
    "nice_to_have": [{"term": "", "type": "", "modality": 0.3}],
    "responsibilities": [{"action_verb": "", "object": ""}],
    "knockouts": [],
    "intent": "Bu rol esasen ___ arıyor."
  },
  "summary": {
    "role_essence": "1-2 cümle",
    "cv_top_summary_draft": "ilk 100-150 kelime, en kritik zorunlu terimler + konumlandırma"
  },
  "synthesis": {
    "semantic_clusters": [{"cluster_label": "", "member_skills": []}],
    "lsi_expansions": {"<term>": ["varyant1", "varyant2"]},
    "achievement_bullets": [
      {"verb": "", "X_result": "", "Y_metric": "", "Z_method": "", "framework_cv_id": "EXP-07"}
    ],
    "section_map": ["Özet", "Deneyim", "Beceriler", "Eğitim", "Sertifikalar"]
  },
  "match_score": {
    "score_percent": 0,
    "components": {"Lex": 0.0, "Sem": 0.0, "Cov": 0.0, "Parse_gate": 1.0, "Stuffing": 0.0},
    "interpretation": "hedef %75-85; >%90 şişirme; <%50 ciddi iyileştirme"
  },
  "gap_analysis": {
    "closable_gaps": [],
    "uncloseable_gaps": [],
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0,
    "recommendations": []
  },
  "provenance_check": [
    {"cv_bullet": "", "framework_cv_id": "", "jd_match": "", "status": "doğrulandı|işaretli"}
  ]
}
```

## Markdown (insan-okur) varyant
Aynı altı alanı başlıklarla ver:
```
## 1. keywords        (ağırlıklı liste)
## 2. analysis        (7 katman + niyet)
## 3. summary         (rolün özü + üst-özet taslağı)
## 4. synthesis       (kümeler + LSI + XYZ cümleleri + bölüm haritası)
## 5. match_score     (skor + bileşenler + yorum)
## 6. gap_analysis    (kapatılabilir/kapatılamaz + P/R/F1 + öneriler)
## + FINAL CV         (+ provenans tablosu)
```
