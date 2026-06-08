# 06 — Denetim ve Düzeltmeler (Audit)

`synthesis-analysis-research` denetim disipliniyle özgün spesifikasyon tarandı. Bulgular ve düzeltmeler:

## Yüksek önem
- **H1 — Revizyon döngüsü sonsuza girer.** Eski: `skor<hedef VEYA gap≠boş → döngü`; dürüst CV'de gap asla boşalmaz. **Düzeltme:** durma = `skor≥hedef VEYA kapatılabilir-gap=0`; gap'i kapatılabilir/kapatılamaz ayır. → `engine/ats_engine/synthesis.py::stopping_condition` (+ test).
- **H2 — Taşınabilirlik.** Claude `.skill` diğer LLM'lerde çalışmaz; akış çok-araçlı. **Düzeltme:** taşınabilir Master Prompt (`prompts/master-prompt-TR.md`).

## Orta-yüksek
- **MY1 — Provenans ilkeydi, adım değildi.** → zorunlu provenans kontrolü (`evidence_bank.py`).
- **MY2 — JD + SEO çıktısı aynı blokta → kirlenme.** → etiketli bölümler `[JD-ORİJİNAL]/[ANALİZ]/[SENTEZ-ÖNERİ]` (`templates/jd-etiketli-sablon.md`).
- **MY3 — 20 sayfa ham Framework CV.** → etiketli kanıt bankası.

## Orta
- **M1** clamp(0,1) · **M2** Parse çarpan/kapı · **M3** Lex/Cov bağımlılığı · **M4** modality 3 kademe.
  Hepsi `engine/ats_engine/scoring.py` ve `jd_parser.py`'de uygulandı.

## Düşük
- **D1** SBERT birincil, LSA/SVD yedek · **D2** çözümlü örnek aritmetiği doğru · **D3** vendor istatistikleri "tek-kaynak" çekincesiyle · **D4** çerçeve "botu geç"ten "sıralamayı kazan + temiz parse + insana hızlı evet"e kaydı.

> **Genel hüküm:** Kritik tek mantık hatası H1, kritik kullanılabilirlik eksiği H2 idi; ikisi de giderildi. Diğer düzeltmeler skoru daha dürüst ve kalibre yaptı. Tam metin: `skills/.../KURULUM-VE-BULGULAR` muadili `ATS-CV-ARCHITECT_KURULUM-VE-BULGULAR.md`.
