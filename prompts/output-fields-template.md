# Evidence-First Çıktı Şablonu

Her ilan için aynı alanları üret. Bilinmeyen değerleri uydurma; `UNKNOWN`,
`NOT_COLLECTED`, `NOT_RUN` veya `null` kullan.

```json
{
  "analysis": {
    "must_have": [],
    "nice_to_have": [],
    "must_have_source": "explicit|none_detected",
    "review_required": true,
    "review_reason": ""
  },
  "match_score": {
    "score_percent": null,
    "evaluation_status": "NOT_EVALUATED",
    "process_status": "REVIEW",
    "legacy_diagnostic_percent": 0.0,
    "components": {},
    "interpretation": "Tanı; ticari ATS veya outcome tahmini değildir."
  },
  "gap_analysis": {
    "closable_gaps": [],
    "uncloseable_gaps": [],
    "recommendations": []
  },
  "provenance_check": [
    {
      "cv_bullet": "",
      "framework_cv_id": null,
      "support_type": "LEXICAL_SUPPORT|UNSUPPORTED",
      "verification_status": "UNVERIFIED",
      "status": "REVIEW"
    }
  ],
  "synthesis_change_set": {
    "id": "",
    "changes": [
      {
        "path": "cv.summary",
        "old_value": "",
        "new_value": "",
        "evidence_ids": ["EV-001"],
        "reason": ""
      }
    ],
    "status": "REVIEW",
    "human_approved": false
  },
  "decision_report": {
    "overall_status": "REVIEW",
    "evaluation_status": "NOT_EVALUATED",
    "gates": [
      {"gate_id": "G0", "status": "PASS", "reason": ""},
      {"gate_id": "G1", "status": "NOT_RUN", "reason": ""},
      {"gate_id": "G2", "status": "REVIEW", "reason": ""},
      {"gate_id": "G3", "status": "PASS", "reason": ""},
      {"gate_id": "G4", "status": "REVIEW", "reason": "İnsan onayı bekleniyor."}
    ],
    "human_approved": false
  },
  "limitations": []
}
```

Markdown varyantında aynı alanları başlıklarla ver. Blocking/review durumunda kısmi
tanıları koru, sonraki insan aksiyonunu açıkça yaz ve CLI karşılığının exit `4`
olduğunu belirt.
