# R1 — Sistemik Veri & ATS Mimarisi (damıtılmış özet)

> Kaynak (Drive): "ATS Uyumlu Özgeçmiş Mimarisinde Algoritmik Sentez ve Analiz" (doc id: 1WI1eFK8tJYvr4mgMnU4UpLEmTdHQ31ulUjg9sMoNDAw). Atıflı, paraflanmış özet.

## Felsefe→pratik
Mekanistik indirgemecilikten (Descartes) sistem holizmine (Ackoff: "sentez analizi önceler"). Kant/Hegel ile sentetik yargının gerekliliği. İş ilanı = çözülecek makro sistem; önce niyet/bağlam sentezi, sonra istatistiksel ayrıştırma.

## 7 katmanlı ayrıştırma
Kimlik · Zorunlu (knockout, ağırlık 1.0) · Tercih (0.3) · Sorumluluk/eylem · Niyet/alt-metin · Semantik/LSI · Ağırlık metası (frekans + konum). (Detay: `docs/02-jd-decomposition.md`.)

## ATS parsing mimarileri
- **Taleo/Workday:** çok katmanlı AI ayrıştırıcı; belgeyi "Ağaç Hiyerarşisi"ne çevirir. 2-sütun/tablo/grafik/yaratıcı başlık → ayrıştırıcıyı bozar ("parse edilemeyen CV puanlanamaz").
- **SAP SuccessFactors:** İş Mantığı katmanı + TF-IDF/semantik; kelimenin doğru bağlamda ve kıdeme uygun olması şart.
- **Kariyer.net:** yapılandırılmış profil alanları (Skill Tags) ağırlıklı.
- **LinkedIn Recruiter AI:** string değil **entity** tabanlı; "Entity SEO", NAP/NTC tutarlılığı → E-E-A-T.

## Parse_gate
Format kalitesi JD'den bağımsız bir **geçirgenlik çarpanı**dır; CV verisinin ~%40'ı format hatasıyla "görünmez" olabilir. Hatalı biçim skoru orantılı çökertir ("Kara Delik"). Tek sütun + DOCX + basit tipografi → gate ≈ 1.0.

## Matematik & dürüstlük
TF-IDF, Okapi BM25 (k1 doygunluk, b uzunluk-norm.), kosinüs, SBERT; hibrit skor (clamp + Parse_gate çarpan). Kanıt bankası + provenans; kapatılabilir/kapatılamaz gap; %90+ aşırı-optimizasyon riski.
