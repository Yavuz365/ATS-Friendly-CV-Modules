# Provenans ve Halüsinasyon Önleme

> Sistemin dürüstlük güvencesinin operasyonel açıklaması.

---

## Neden Provenans?

Bir LLM, bağlamında olmayan bir beceriyi CV'ye ekleyebilir. Bu:
- İş görüşmesinde çöker (kandidat bilmez).
- İşverene güven kaybı yaratır.
- Etik ihlaldir.

**Provenans Defteri**, bu riski yapısal olarak ortadan kaldırır.

---

## Provenans Defteri — Nasıl Çalışır?

Her CV çalıştırmasında **Katman 0**'da başlatılır:

```
| CV maddesi | Framework CV girdi-id | JD'de karşılığı | durum |
|------------|------------------------|------------------|-------|
| "...%30 kısalttım" | EXP-07 | "gümrükleme/KPI" | doğrulandı |
| "Python analizi" | — | "veri analizi" | işaretli: kanıt yok |
```

**Kural:** `durum = işaretli` veya `framework_cv_id = —` olan madde CV'ye giremez.

---

## Framework CV → Kanıt Bankası Dönüşümü

Ham 20 sayfalık CV yerine **yapılandırılmış kanıt bankası** kullan:

```
EXP-07 | Dış Ticaret | beceriler: [gümrükleme, KPI] | metrik: süre −%30 | dönem: 2019-2022
EXP-12 | Lojistik Koordinasyon | beceriler: [tedarik, nakliye] | metrik: maliyet −%15
SKILL-03 | SAP WM modülü | tür: araç | kanıt: EXP-07 ile örtüşüyor
```

CV-yazıcı her ilanda yalnızca eşleşen girdileri (ör. `EXP-07, EXP-12`) çeker; 20 sayfalık ham içeriği boğmaz.

---

## Skor ile Provenans Farkı

| Metrik | Ölçtüğü | Kaynak |
|--------|---------|--------|
| Hibrit ATS Match Score | JD–CV kelime/anlam örtüşmesi | `references/scoring-formulas.md` |
| Provenans skoru | CV maddelerinin kanıt bağ oranı | Bu belge / Provenans Defteri |

İkisi bağımsızdır. Yüksek match score + düşük provenans → şişirme riski.

---

## Anti-Halüsinasyon Kontrol Listesi (Katman 5)

Teslim öncesi aşağıdakiler geçilmeli:

- [ ] Her CV maddesi Provenans Defterinde bir Framework CV girdi-id'sine bağlı
- [ ] `durum = işaretli` satır kalmamış
- [ ] LSI/semantik genişletmeden gelen hiçbir terim kanıtsız CV'de geçmiyor
- [ ] `gap_kapatılamaz` listesi dürüstçe açıklanmış (döngüye sokulamamış)
- [ ] Skor %90+ ise şişirme kontrolü yapılmış

---

## Source Registry (synthesis-analysis-research Disipliniyle İlişki)

`synthesis-analysis-research` skill'indeki Source Registry ile ilişki:

| Synthesis-Analysis | ATS CV Architect |
|--------------------|-----------------|
| Dış kaynak kaydı | Framework CV kanıt bankası |
| Güven düzeyi (High/Med/Low) | Provenans durumu (doğrulandı/işaretli) |
| Çatışma çözümü | Gap kapatılabilir/kapatılamaz ayrımı |

ATS CV Architect'in Provenans Defteri, synthesis-analysis-research'ın Source Registry'sini CV bağlamına özelleştirmiş halidir.
