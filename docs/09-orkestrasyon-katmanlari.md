# docs/09 — Orkestrasyon Katmanları

> **Legacy tasarım:** Güncel orkestratör G0–G4 `DecisionReport` sözleşmesidir.

> Araç-bağımsız, rol-bazlı ATS-CV pipeline orkestrasyon mimarisi.

## 1. Genel Akış

```
┌─────────────────────────────────────────────────────────────────┐
│ İŞ İLANI (JD)                                                  │
│   → JDParser (7 katman ayrıştırma)                              │
│     → Zorunlu terimler + modality + positional ağırlıklar       │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 1: ARAÇ-CV KAPISI                                        │
│   Her AI aracı (ChatGPT, Claude, Gemini, Copilot, vb.) ayrı   │
│   ayrı CV üretir → her biri JD'ye karşı skorlanır.             │
│   Eşik: τ = 0.70 — altındakiler elenir.                        │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 2: SEKİZ-PARÇA EN-İYİ SEÇİMİ                            │
│   8 bölüm (özet, deneyim×4, beceriler, eğitim, sertifika)     │
│   → Her bölüm için tüm araçlardan en yüksek skoru seçer       │
│   → Birleştirir + dikiş cezası (κ = 0.15) uygular             │
│   → Birleşik CV'yi yeniden skorlar                              │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ LEVEL 3: KATEGORİ ROBUSTNESS                                   │
│   Birleşik CV'yi aynı kategorideki 3+ ilana test eder.         │
│   σ ≤ 0.10 → robust | σ > 0.10 → aşırı uyarlanmış             │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ PROVENANS + GAP ANALİZİ                                        │
│   evidence_bank → her CV maddesini Framework CV'ye bağlar       │
│   gap_closable / gap_unclosable ayrımı → revizyon döngüsü      │
│   DUR koşulu: skor ≥ hedef VEYA kapatılabilir gap = 0          │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ GRAMMARLY KAPISI (docs/13)                                     │
│   AI-detector → %80+ ise yeniden yazma (rewriter)               │
│   Son Grammarly skoru: doğruluk, netlik, akıcılık               │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Roller ve Sorumluluklar (Araç-Bağımsız)

| Rol | İşlev | Herhangi Bir AI Aracı |
|-----|--------|-----------------------|
| ANALIST | JD'yi 7 katmana ayırır | Master Prompt → herhangi bir LLM |
| SENTEZCİ | Framework CV + JD analizi → CV taslağı | Herhangi bir LLM |
| PUANLAYICI | Deterministik skor | `ats_engine.scoring` (Python) |
| DENETÇİ | Provenans + gap + stuffing kontrolü | `ats_engine.evidence_bank` + `synthesis` |
| EDİTÖR | Dil doğruluk + AI-detector | Grammarly veya benzeri araç |

## 3. Araç-Bağımsızlık İlkesi

Bu repo **hiçbir AI aracına bağımlı değildir**:

- ❌ "Gemini'de analiz yap" → ✅ "Herhangi bir LLM'de analiz yap"
- ❌ "n8n ile pipeline kur" → ✅ "Otomasyon platformu ile pipeline kur"
- ❌ "Claude native skill yükle" → ✅ "LLM'e Master Prompt'u kopyala"

Motor (engine/) Python kodudur ve herhangi bir LLM'den bağımsız çalışır.

## 4. Entegrasyon Noktaları

```
otomasyon platformu → JD klasörünü izle → JDParser tetikle
Linear/Jira         → Roadmap + sprint takibi
GitHub              → Kod + versiyon yönetimi
Google Drive        → JD dosyaları (.docx)
Notion              → Framework CV + kanıt bankası
Slack               → Bug/debug webhook
```
