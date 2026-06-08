# Katkı Rehberi

## İlkeler (asla taviz verilmez)
- **Dürüstlük/provenans:** çıktı CV'sindeki her madde kanıt bankasına bağlanabilmeli.
- **Coverage > density:** anahtar kelime doldurma yok.
- **Skor = proxy:** tescilli ATS formüllerinin yaklaşıklaması; mutlak gerçek gibi sunma.
- **H1 kuralı:** revizyon döngüsü `skor≥hedef VEYA kapatılabilir-gap=0` ile durur; bu değişmez.

## Geliştirme
1. `make dev` → `make test` (PR'dan önce yeşil olmalı).
2. Yeni özellik = yeni test. Audit-düzeltmelerini (clamp, Parse_gate çarpan, gap ayrımı) bozma.
3. Veri güncellemeleri (`engine/data/*.json`) kaynağıyla (Grammarly/ESCO) birlikte belgelensin.
