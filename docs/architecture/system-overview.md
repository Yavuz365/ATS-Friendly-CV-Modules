# Sistem Mimarisi — ATS CV Architect

> **Kanonik kaynak:** Bu repodaki ATS CV üretim motorunun genel mimarisini açıklar.

---

## Genel Mimari

Sistem **iki katmanlı diyalektik bir motordur**:

```
[İŞ İLANI (JD)] ──► ANALİZ (çöz) ──► 7 katmanlı ayrıştırma + ağırlıklı keyword listesi
                                              │
                         [ADAY FRAMEWORK CV] ─┘
                                              │
                       SENTEZ (yeniden bağla) ──► XYZ başarı cümleleri + semantik kümeler
                                              │
                     SKORLAMA + GAP ANALİZİ ──► Hibrit ATS Match Score + P/R/F1
                                              │
                          [skor < hedef?] ────┘ → sentez döngüsü
                                              │
                              FINAL ATS CV ◄──┘
```

**Hedef skor bandı (teşhis sinyali, garanti değil):** `%75–85` güçlü hizalanma · `>%90` şişirme sinyali · `<%50` ciddi iyileştirme gerekir. (A11 fix: bu bantlar işe alım sonucunu veya "ATS'yi geçme"yi garanti etmez — bkz. `docs/03-skorlama-matematigi.md` "Dürüst statü".)

---

## Kanonik Dosya Ağacı

```
skills/ats-cv-architect/
├── SKILL.md                          ← Orkestratör (her çalıştırmada yüklenir)
├── references/
│   ├── jd-decomposition.md           ← ANALİZ: JD'nin 7 katmanı
│   ├── scoring-formulas.md           ← Matematik: TF-IDF/BM25/kosinüs/hibrit skor
│   ├── synthesis-rules.md            ← SENTEZ: kümeleme/XYZ/E-E-A-T/provenans
│   └── workflow-drive-multitool.md   ← Entegrasyon: Drive + çok-LLM akışı
├── assets/
│   ├── master-prompt-TR.md           ← Taşınabilir prompt (her LLM'e)
│   └── output-fields-template.md     ← 6 alanlık çıktı şablonu
├── scripts/
│   └── ats_score.py                  ← Deterministik skorlayıcı (Python)
└── dist/
    └── ats-cv-architect.skill        ← Dağıtılabilir Claude skill paketi
```

---

## Katmanlar (Protokol 0–5)

| Katman | Ad | Giriş | Çıkış |
|--------|-----|-------|-------|
| 0 | Alım & Mod | JD + Framework CV | Mod seçimi, Provenans Defteri başlangıcı |
| 1 | Bütünsel Kavrama | Tüm belgeler | "Rolün özü" notu |
| 2 | ANALİZ | JD | 7 katmanlı ayrıştırma + ağırlıklı keyword listesi |
| 3 | SKORLAMA & GAP | CV + JD analizi | Hibrit skor, P/R/F1, gap listesi |
| 4 | SENTEZ | Gap listesi + Framework CV | XYZ cümleleri, semantik kümeler, ATS CV taslağı |
| 5 | Doğrulama & Teslim | CV taslağı | Provenans kontrolü, final skor, teslim |

---

## Tek Kaynak İlkesi

**Her bilgi parçasının bir ve yalnızca bir kanonik konumu vardır:**

| İçerik | Kanonik Konum |
|--------|--------------|
| Orkestratör / protokol | `skills/ats-cv-architect/SKILL.md` |
| Matematiksel formüller | `skills/ats-cv-architect/references/scoring-formulas.md` |
| Sentez kuralları | `skills/ats-cv-architect/references/synthesis-rules.md` |
| JD ayrıştırma şeması | `skills/ats-cv-architect/references/jd-decomposition.md` |
| Taşınabilir prompt | `skills/ats-cv-architect/assets/master-prompt-TR.md` |
| Deterministik skorlayıcı | `skills/ats-cv-architect/scripts/ats_score.py` |
| ATS KB / ontoloji | `references/ats-kb/` |
| Entegrasyon kılavuzları | `integrations/` |
| Şablonlar | `assets/templates/` |

Arşiv dosyaları (`archive/`) kanonik **değildir** ve doğrudan kullanılmamalıdır.

---

## Araç Yolu (çoklu-LLM)

```
Claude: skills/ats-cv-architect/dist/ats-cv-architect.skill → yükle → tetikle
AI aracı (ChatGPT / Gemini / DeepSeek / vb.): skills/ats-cv-architect/assets/master-prompt-TR.md → kopyala-yapıştır
Deterministik skor: skills/ats-cv-architect/scripts/ats_score.py
```

> Bkz. `integrations/` klasörü → Drive, OneDrive, Box/Dropbox, Jira, Linear, Slack, Jobscan+Grammarly entegrasyon kılavuzları.
