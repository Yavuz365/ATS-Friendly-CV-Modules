# Legacy Migration Map

Bu belge, eski (kök düzey) dosya konumlarını yeni kanonik konumlarına eşler.
Referans kırılmalarını önlemek için geçiş sürecinde kullanın.

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

| Yeni konum | İçerik |
|-----------|--------|
| `skills/ats-cv-architect/references/jd-decomposition.md` | JD 7 katman şeması |
| `skills/ats-cv-architect/references/synthesis-rules.md` | Sentez kuralları |
| `skills/ats-cv-architect/references/workflow-drive-multitool.md` | Drive + çok-LLM akışı |
| `skills/ats-cv-architect/assets/output-fields-template.md` | 6 alan çıktı şablonu |
| `skills/ats-cv-architect/scripts/ats_score.py` | Deterministik skorlayıcı |
| `docs/architecture/system-overview.md` | Genel mimari |
| `docs/architecture/provenance-and-anti-hallucination.md` | Provenans sistemi |
| `references/ats-kb/keyword-ontology.md` | ATS keyword ontolojisi |
| `references/ats-kb/ats-parser-rules.md` | ATS ayrıştırıcı kuralları |
| `references/ats-kb/jd-taxonomy.md` | JD taksonomisi |
| `references/ats-kb/quality-gates.md` | Kalite kapıları |
| `assets/templates/jd-tagged-template.md` | Etiketli JD şablonu |
| `assets/templates/evidence-bank-template.md` | Kanıt bankası şablonu |
| `integrations/drive.md` | Google Drive entegrasyonu |
| `integrations/onedrive.md` | OneDrive entegrasyonu |
| `integrations/box-dropbox.md` | Box/Dropbox entegrasyonu |
| `integrations/jira.md` | Jira JD birleştirme |
| `integrations/linear.md` | Linear iş akışı |
| `integrations/slack-qa.md` | Slack QA kontrolleri |
| `integrations/final-gates-jobscan-grammarly.md` | Jobscan + Grammarly son kapılar |

---

## Geçiş Kuralları

1. **Yeni içerik eklerken** → her zaman `skills/ats-cv-architect/` veya ilgili yeni konuma yaz.
2. **Kök düzey kopya**lar yalnızca geriye uyumluluk için; düzenleme yapma.
3. **Arşiv** dosyalarına asla yeni içerik ekleme; referans olarak kullanma.
4. **Kök düzey kopyalar** ileride (bağlantı doğrulaması sonrası) kaldırılacak.
