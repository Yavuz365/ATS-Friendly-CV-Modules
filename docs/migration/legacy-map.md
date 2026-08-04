# Legacy Migration Map

Bu belge, eski (kök düzey) dosya konumlarını yeni kanonik konumlarına eşler.
Referans kırılmalarını önlemek için geçiş sürecinde kullanın.

> **Düzeltme (2026-08-05):** Aşağıdaki "Yeni Eklenen Dosyalar" tablosu bazı yolları
> repoda zaten var gibi listeliyordu; canlı repo ağacı taranarak kontrol edildi ve
> bir kısmının hiç oluşturulmadığı görüldü. Tablo artık gerçek durumu (Var / Planlandı)
> ayrı bir sütunda gösteriyor.

---

## Dosya Eşlem Tablosu

| Eski konum (kök) | Yeni kanonik konum | Durum |
|-----------------|-------------------|-------|
| `ats-cv-architect_SKILL.md` | `skills/ats-cv-architect/SKILL.md` | Kanonik taşındı; kök kopya uyumluluk için korunuyor |
| `ats-cv-architect_SCORING-FORMULAS.md` | `skills/ats-cv-architect/references/scoring-formulas.md` | Kanonik taşındı |
| `ats-cv-architect_MASTER-PROMPT-TR.md` | `skills/ats-cv-architect/assets/master-prompt-TR.md` | Kanonik taşındı |
| `ats-cv-architect.skill` | `skills/ats-cv-architect/dist/ats-cv-architect.skill` | Dağıtılabilir; kök kopya uyumluluk için korunuyor |
| `ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md` | `docs/audits/ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md` | Denetim/tarihçe dokümanı |
| `ats-cv-architect_TUM-SKILL-BIRLESIK.md` | `archive/ats-cv-architect_TUM-SKILL-BIRLESIK.md` | ARŞİV — düzenleme yapma |
| `synthesis-analysis-research_FULL.md` | `archive/synthesis-analysis-research_FULL.md` | ARŞİV — düzenleme yapma |
| `synthesis-analysis-research.skill` | Kök konumda; kapsam gözden geçirilmeli | İnceleme bekliyor |

---

## Yeni Eklenen Dosyalar (kök konumda olmayan)

| Yeni konum | İçerik | Repoda mevcut mu? (2026-08-05 kontrolü) |
|-----------|--------|-------------------------------|
| `skills/ats-cv-architect/references/jd-decomposition.md` | JD 7 katman şeması | ✅ Var |
| `skills/ats-cv-architect/references/synthesis-rules.md` | Sentez kuralları | ✅ Var |
| `skills/ats-cv-architect/references/workflow-drive-multitool.md` | Drive + çok-LLM akışı | ✅ Var |
| `skills/ats-cv-architect/assets/output-fields-template.md` | 6 alan çıktı şablonu | ✅ Var |
| `skills/ats-cv-architect/scripts/ats_score.py` | Deterministik skorlayıcı | ✅ Var |
| `docs/architecture/system-overview.md` | Genel mimari | ✅ Var |
| `docs/architecture/provenance-and-anti-hallucination.md` | Provenans sistemi | ✅ Var |
| `references/ats-kb/keyword-ontology.md` | ATS keyword ontolojisi | ✅ Var |
| `references/ats-kb/ats-parser-rules.md` | ATS ayrıştırıcı kuralları | ✅ Var |
| `references/ats-kb/jd-taxonomy.md` | JD taksonomisi | ✅ Var |
| `references/ats-kb/quality-gates.md` | Kalite kapıları | ❌ **Planlandı, henüz oluşturulmadı** |
| `assets/templates/jd-tagged-template.md` | Etiketli JD şablonu | ❌ **Planlandı, henüz oluşturulmadı** (`assets/` dizini repoda yok) |
| `assets/templates/evidence-bank-template.md` | Kanıt bankası şablonu | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/drive.md` | Google Drive entegrasyonu | ❌ **Planlandı, henüz oluşturulmadı** (`integrations/` dizini repoda yok) |
| `integrations/onedrive.md` | OneDrive entegrasyonu | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/box-dropbox.md` | Box/Dropbox entegrasyonu | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/jira.md` | Jira JD birleştirme | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/linear.md` | Linear iş akışı | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/slack-qa.md` | Slack QA kontrolleri | ❌ **Planlandı, henüz oluşturulmadı** |
| `integrations/final-gates-jobscan-grammarly.md` | Jobscan + Grammarly son kapılar | ❌ **Planlandı, henüz oluşturulmadı** |

---

## Geçiş Kuralları

1. **Yeni içerik eklerken** → her zaman `skills/ats-cv-architect/` veya ilgili yeni konuma yaz.
2. **Kök düzey kopya**lar yalnızca geriye uyumluluk için; düzenleme yapma.
3. **Arşiv** dosyalarına asla yeni içerik ekleme; referans olarak kullanma.
4. **Kök düzey kopyalar** ileride (bağlantı doğrulaması sonrası) kaldırılacak.
5. **"Planlandı" olarak işaretli satırlar** — bu dosyalar henüz yok; onlara link veren başka
   belgeler (örn. bu dosyanın kendisi) kırık referans üretebilir. Gerçekten ihtiyaç yoksa bu
   satırları kaldırmayı, varsa dosyaları oluşturmayı değerlendirin.
