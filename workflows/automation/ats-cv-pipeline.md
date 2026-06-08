# otomasyon platformu — ATS CV Toplu Pipeline

## Akış
1. **Trigger:** Google Drive — `01-Job-Postings/` klasörüne yeni dosya.
2. **Extract:** dosyadan JD metnini çıkar (Docs/PDF).
3. **LLM (Analiz+Sentez):** Master Prompt ile 6 alanı üret (JSON iste).
4. **Engine (opsiyonel, deterministik skor):** `ats_engine` CLI'yi çağır:
   `python -m ats_engine.cli report --jd jd.txt --framework framework.md --format md`
5. **Persist:** 6 alanı Notion "İş İlanları" + "Skorlama Günlükleri" satırına yaz.
6. **Notify:** Slack/Telegram — "Yeni ilan skorlandı: %X — durum".
7. **Rank:** skora göre sırala → "bana en uygun ilanlar" görünümü.

## Klasör taksonomisi (Drive)
`01-Job-Postings/ · 02-Analyses/ · 03-CV-Outputs/ · 04-Scoring-Reports/`
Dosya adı: `[Pozisyon]_[Şirket].pdf`.
