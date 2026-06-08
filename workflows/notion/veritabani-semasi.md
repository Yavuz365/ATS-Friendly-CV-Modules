# Notion — 6 İlişkili Veritabanı Şeması

Merkezi Doğruluk Kaynağı (Single Source of Truth).

1. **İş İlanları (Job Postings):** ID, Pozisyon, Şirket, Dil, Başvuru Tarihi, Durum (Toplandı→Analiz→CV Üretildi→Başvuruldu).
2. **CV Versiyonları (CV Versions):** İlan(ilişki), Üreten Araç, Lex, Sem, Cov, Toplam Skor, Onay Durumu.
3. **CV Bölümleri (CV Parts):** Versiyon(ilişki), Bölüm (Özet/Deneyim/Beceriler/Eğitim/Sertifika…), İçerik bloğu, Kanıt-ID.
4. **Şirketler (Companies):** Sektör analizi, mülakat hazırlık notları.
5. **Skorlama Günlükleri (Scoring Logs):** İlan(ilişki), BM25/Cosine/Cov dökümü, tarih, sistem tavsiyesi.
6. **İş Akışı (Workflow):** Adım, Engel (blocker), Durum notu.

> İlişkiler: İlan → CV Versiyonu → CV Bölümleri; İlan → Şirket; İlan → Skorlama Günlüğü.
