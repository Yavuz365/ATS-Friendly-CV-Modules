# 07 — Drive + Çok-Araçlı + Otomasyon İş Akışı

> **Planlanan/legacy workflow:** Production otomasyonu doğrulanmış değildir; bkz. `docs/limitations.md`.

Tam metin: `skills/ats-cv-architect/references/workflow-drive-multitool.md`.

## Aşamalar
- **Zemin (bir kez):** Framework CV → etiketli kanıt bankası; beceri sözlüğü (ESCO/O*NET ya da 100–200 kelimelik tablo); 50–100 ilanlık corpus.
- **Tek ilan:** A.1 JD'yi Drive'a etiketli Word olarak yükle → A.2 AI aracı (herhangi bir LLM) ile analiz+sentez, çıktıyı **`[SENTEZ-ÖNERİ]`** bölümüne (asla orijinale karıştırma) → A.3 Master Prompt ile 6 alan → B.1 CV-yazıcı yalnızca eşleşen+kanıtlı girdilerle ATS CV.
- **Toplu (100 ilan):** otomasyon platformu (n8n, Make, Zapier vb.): Drive tetikleyici → LLM → 6 alanı Notion/Sheet satırına yaz → Slack/Telegram bildirimi → skora göre sırala.

## Veri kirlenmesi önlemi
LLM'lerin ürettiği LSI/eşanlamlı terimler adayda *olmayan* beceriler olabilir; ham veriyle aynı bloğa yazılmaz (halüsinasyon/şişirme riski).

Bakınız: `workflows/otomasyon platformu (n8n, Make, Zapier vb.)/ats-cv-pipeline.md`, `workflows/notion/veritabani-semasi.md`.
