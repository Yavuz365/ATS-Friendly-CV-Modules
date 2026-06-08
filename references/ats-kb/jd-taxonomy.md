# JD (İş İlanı) Taksonomisi

> **Kanonik konum:** `references/ats-kb/jd-taxonomy.md`  
> İş ilanlarını (JD) katmanlara ayırma, yorumlama ve ATS analizi için sınıflandırma rehberi.

---

## 1. JD 7 Katman Modeli

JD'nin her bölümünü ayrıştır ve 7 katmana ata:

| Katman | Etiket | İçerik Türü | Ağırlık |
|--------|--------|-------------|---------|
| 1 | `COMPANY_SIGNAL` | Şirket kültürü, misyon, değerler | ×0.4 |
| 2 | `ROLE_CORE` | Temel iş fonksiyonları | ×1.0 |
| 3 | `MUST_HAVE` | Açıkça belirtilmiş zorunlu nitelik | ×1.0 |
| 4 | `IMPLIED_REQUIRED` | Zımni/varsayılan gereklilik | ×0.7 |
| 5 | `NICE_TO_HAVE` | "tercih / avantaj / plus" | ×0.3 |
| 6 | `CULTURAL_FIT` | İletişim, ekip çalışması, liderlik sinyalleri | ×0.5 |
| 7 | `DISQUALIFIER_RISK` | Kırmızı bayrak (visa/konum/deneyim yılı kırılıcı) | Özel |

### Katman Uygulama Notları

- **MUST_HAVE** her zaman JD'nin "Aranan Nitelikler" bölümünde ama bazen iş tanımına gömülü.
- **IMPLIED_REQUIRED** → "en az N yıl deneyim" yazmamasına rağmen iş ilanı kıdemli bir rol anlatıyorsa varsayım.
- **DISQUALIFIER_RISK** → herhangi bir koşul gerçekleşirse → kullanıcıyı uyar; ilerlenip ilerlenemeyeceğini sor.

---

## 2. JD Ayrıştırma Prosedürü

```
1. Tüm JD metnini al.
2. Bölüm başlıklarını tespit et (Hakkımızda, Görevler, Aranan Nitelikler, Tercihler…).
3. Her cümleyi / maddeyi uygun katmana ata.
4. Aynı cümleyi birden fazla katmana atama (tek en yüksek katmanı seç).
5. DISQUALIFIER_RISK var mı? → Varsa hemen önce raporla.
6. Keyword listesi çıkar: [MUST_HAVE], [IMPLIED_REQUIRED] sıralanmış liste.
7. Modality + konum ağırlığını uygula → öncelikli keyword sıralaması üret.
```

---

## 3. Standart JD Veri Akışı

```
Jira (merged JD) → JD ayrıştırıcı (7 katman) → keyword özeti
                                                  ↓
                               Keyword özeti → skills/ats-cv-architect/SKILL.md
                                                  ↓
                               SKILL → Framework CV + kanıt bankası eşleme
```

Bkz. `integrations/jira.md` — Jira'dan JD nasıl alınır.

---

## 4. Çok Dilli Anlam Eşleştirme

| JD'deki Türkçe | JD'deki İngilizce | Eşdeğer keyword |
|---------------|-------------------|----------------|
| Akreditif | Letter of Credit | L/C |
| Gümrükleme | Customs clearance | Customs, declaration |
| Tedarik zinciri | Supply chain | Logistics, procurement |
| Bütçe hazırlamak | Budget planning | Financial planning |
| Süreç iyileştirme | Process improvement | Operational efficiency |

Bu tabloyu ilgili sektörler için genişlet. Bkz. `references/ats-kb/keyword-ontology.md`.

---

## 5. JD Doğrulama Kontrolleri

Analiz tamamlandığında şunları sağla:

- [ ] En az 3 MUST_HAVE keyword tespit edildi
- [ ] En az 1 ROLE_CORE tanımlandı
- [ ] DISQUALIFIER_RISK varsa raporlandı
- [ ] Tüm keyword'ler modality ağırlığı aldı
- [ ] Çok dilli eşdeğerler eklendi
- [ ] Çıktı, `assets/templates/jd-tagged-template.md` formatında

---

## 6. Örnek Ayrıştırma Çıktısı

```json
{
  "jd_url": "...",
  "jd_date": "2024-01",
  "layers": {
    "MUST_HAVE": ["Incoterms", "akreditif", "gümrükleme", "MS Excel"],
    "IMPLIED_REQUIRED": ["tedarik zinciri yönetimi", "ERP deneyimi"],
    "NICE_TO_HAVE": ["SAP", "İngilizce raporlama"],
    "DISQUALIFIER_RISK": []
  },
  "priority_keywords": ["Incoterms (1.0)", "akreditif (0.9)", "gümrükleme (0.9)", "MS Excel (0.8)"]
}
```
