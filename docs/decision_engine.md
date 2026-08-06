# Decision Engine — Uygulanan G0–G4 Sözleşmesi

> **Durum:** `2.0.0-alpha.1` içinde uygulanmış contract alpha. Production export kapısı değildir.

`engine/ats_engine/decision.py`, rapor sinyallerini tipli `DecisionReport` altında birleştirir.
Lexical/semantic değerler yalnız `DiagnosticResult`tır ve kapıları override edemez.

| Gate | Anlam | Mevcut davranış |
|---|---|---|
| G0 | Input / Integrity | Parse sinyali ≥0.70 ise PASS; düşükse FAIL; üretilemezse ERROR |
| G1 | Eligibility | Knockout gereksinimi varsa REVIEW; aday uygunluk verisi yoksa NOT_RUN |
| G2 | Evidence / Truth | Lexical evidence olsa bile REVIEW; kaynak/insan incelemesi olmadan PASS yok |
| G3 | Parse / Language / Consistency | LangGate rapora bağlıdır; locale mismatch WARN |
| G4 | Human Approval | Yalnız açık `human_approved=True` ile PASS |

Genel durum önceliği: `ERROR → FAIL → REVIEW/NOT_RUN → WARN → PASS`.

## Bilinçli sınırlar

- G1 için yapılandırılmış aday uygunluk deposu henüz tam ingestion akışına bağlı değildir.
- G2 lexical support ile olgusal verification’ı ayırır; otomatik `VERIFIED` üretmez.
- G4 onayı diğer başarısız kapıları geçersiz kılmaz.
- Production DOCX/PDF export uygulanmadı.

JSON/Markdown/CLI aynı `decision_report` payload’ını tüketir. CLI blocking/review durumda
çıktıyı korur ve exit `4` döner.
