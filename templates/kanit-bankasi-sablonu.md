# Kanıt Bankası Şablonu (Framework CV → etiketli girdiler)

Her başarı tek satır. ID satır başında. `|` ile ayır. Motor (`evidence_bank.py`) bu formatı okur.

```
EXP-01 | Dış Ticaret | beceriler: [customs clearance, incoterms, akreditif] | metrik: süre −%30 | dönem: 2019-2023 | kanıt: "Gümrük süreçlerini YYS/AEO ile optimize ettim..."
EXP-02 | ERP/Operasyon | beceriler: [SAP MM, regulatory compliance] | metrik: maliyet −%15 | dönem: 2017-2019 | kanıt: "..."
SKILL-01 | Diller | beceriler: [İngilizce C1, Almanca B2]
EDU-01 | Eğitim | İşletme Lisans | dönem: 2013-2017
CERT-01 | Sertifika | CPIM | dönem: 2021
```

Alan anahtarları esnek: `beceri/skill`, `metrik/kpi/sonuç`, `dönem/tarih/yıl`, `kanıt/cümle/açıklama`. ID önekleri: `EXP / SKILL / EDU / CERT / PROJ`.
