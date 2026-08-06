# ADR-001 — Evidence-First v2.0 Ürün Sözleşmesi (TASLAK — ONAY BEKLİYOR)

**Tarih:** 2026-08-04
**Durum:** 🟡 **TASLAK — henüz kabul edilmedi.** Bu belge bir karar önerisidir, bir karar
duyurusu değildir. Aşağıdaki "Kabul kriterleri" bölümünde açıkça belirtildiği gibi,
**Ahmet'in (Product Owner) bu metni onaylaması olmadan hiçbir v2.0 kod değişikliği
başlamaz.**
**Kaynak:** Bu taslak, Notion'daki kanonik karara sadık bir transkripsiyondur — yeni bir
mimari karar önermez. Kaynaklar: "ATS-Friendly-CV-Modules — Kritik Başarı Roadmap'i ve
Uygulama Todo Listesi" (30 Temmuz 2026, TD-001/TD-004), "Claude + ChatGPT — Nihai Çapraz
Denetim ve Kapanış Raporu" (2 Ağustos 2026, §9.2), ve repodaki mevcut
`docs/decisions/ADR-000-pre-production-status.md` (2026-08-03, zaten kabul edilmiş).

## Bağlam

`ADR-000` (kabul edilmiş, `v1.5.1` ile birlikte) şunu zaten netleştirdi: v1.5.1 yalnızca
**stabilizasyon** kapsamındaydı (yeni özellik yok) ve *"v2.0 contract-first çalışmasının
ne zaman başlayacağı ayrı bir insan kararıdır, bu ADR onu otomatik olarak başlatmaz."*

Bu taslak (`ADR-001`), o ayrı kararın **içeriğini** önceden hazırlar — böylece Ahmet
"evet" dediğinde mühendislik ekibi (Viktor dahil) tam olarak neyin onaylandığını bilir.
Onay verilene kadar bu bir taslaktır; onaylandığında dosya adından `-DRAFT` kaldırılıp
`Durum: Kabul edildi` yapılır.

## Önerilen karar

`v1.5.x` mevcut hâliyle **Legacy Diagnostic Engine** olarak dondurulur. Yeni geliştirme
`v2.0.0-alpha` altında, tek bir "ATS geçme / mülakata hazır skoru" yerine bağımsız
**kanıt bütünlüğü (evidence integrity), uygunluk (eligibility), belge ayrıştırma (document
parse), gereksinim kapsamı (requirement coverage), terminoloji (lexical/semantic), başvuru
tutarlılığı (application consistency) ve insan değerlendirmesi** sonuçları üreten
evidence-first bir karar destek sistemi olarak yürütülür.

**Bu, repository'yi baştan yazmak anlamına gelmez.** Korunacaklar (TD-004):
- Python çekirdeği ve paketleme (`ats_engine/data/`, `domain_pack_data/` — v1.5.1'de
  zaten düzeltildi)
- CLI iskeleti (`cli.py` — `report/score/parse/bank` alt-komutları)
- BM25/TF-IDF diagnostic araçları
- TR/EN normalizasyonu (word-boundary matching — v1.5.1'de zaten düzeltildi)
- Domain-pack loader
- Kanıt bankası (evidence bank) fikri
- Test/CI temeli (64 test, ruff, mypy — v1.5.1'de zaten temiz)
- Archive/changelog geçmişi

### Yedi kritik hamle (kabul kriterleri v2 için)

1. Ürün sözleşmesini dondur: `%75–85`, `>90 stuffing`, "ATS geçti" ve "mülakata hazır"
   ifadelerini kanonik karar mekanizmasından çıkar (not: v1.5.1 zaten dokümanlardan bu
   dili büyük ölçüde temizledi — STAB-011; v2 bunu API/schema seviyesinde kalıcı hale
   getirir).
2. Kanıt zincirini zorunlu kıl: final CV'ye giren her iddia `evidence_id + source_id +
   source_locator` taşısın.
3. Bağımsız ve fail-closed kapılar kur: eligibility, evidence integrity ve document parse
   hataları yüksek lexical/semantic değerlerle geçersiz kılınamasın.
4. Gerçek belgeyi test et: düz metin heuristiğini gerçek DOCX OOXML, PDF text layer ve
   reading-order testlerinden ayır (canlı doğrulandı: `cv_parser.py` şu an yalnız
   `str` alıyor, gerçek binary parsing yok — bu gerçek bir açık).
5. Tek skoru diagnostic'lere böl: lexical, semantic ve coverage değerleri bilgilendirici
   kalsın; işe alım sonucu veya evrensel pass/fail üretmesin.
6. Kod–veri–belge güven zinciri kur: negatif testler, schema validation, veri manifesti
   ve doküman/prompt/skill contract lint'i CI'da birlikte çalışsın.
7. Ürünleştirmeyi doğrulamadan sonra yap: UI, Notion otomasyonu, vendor gözlemleri,
   outcome tracking ve yeni dil/domain genişlemesi ancak bu P0 güven sözleşmesi
   geçtikten sonra başlar.

### Bağımlılık kuralı

Milestone 0–6 (bkz. Notion "Kritik Başarı Roadmap'i", TD-001→TD-607) bitmeden UI, Notion
otomasyonu, vendor-specific davranış, yeni skor ağırlığı veya "production-ready" iddiası
başlatılmaz.

## Bu ADR onaylandıktan SONRA yapılacak ilk adımlar (kod değil, hâlâ onay/planlama)

- `docs/baseline/2026-08-04-v2-baseline.md` — dondurulmuş baseline manifesti (git SHA,
  Notion page ID'leri, bilinen 3 eksik kaynak, bilinen P0 mimari boşluklar)
- GitHub üzerinde Milestone 0–8 + EPIC-0..7 yapısı (Notion TD-003) — Ahmet onayı sonrası
  Viktor açabilir
- `contracts/status.py` ve JSON şemaları (TD-101, TD-102...) — **bu ADR onaylanmadan
  yazılmaz**

## Kabul kriterleri

- [ ] Ahmet bu taslağı okudu ve karar metnini (yukarıdaki "Önerilen karar" ve "yedi kritik
      hamle") onaylıyor
- [ ] "ATS geçti", "mülakata hazır" ve sonuç olasılığı ifadeleri v2 ürün vaadi *değildir*
      — bu netleşti
- [ ] Legacy skor yalnız açıkça deprecated bir adapter üzerinden sunulacak — bu netleşti
- [ ] **Kullanıcı onayı alınmadan hiçbir v2.0 kod değişikliği (contracts/, schemas/,
      yeni modül) başlamaz** — bu taslağın en kritik maddesi

## Notlar

- Bu belge, Notion'daki "Candidate Track" kararından (2 Ağustos 2026 kapanış raporu, §10)
  **bağımsızdır**: Candidate Track (Ahmet'in kişisel CV üretimi) zaten onaylı ve bu ADR'yi
  beklemeden devam edebilir/etmektedir — bu belge yalnızca **repository/v2.0 mimari**
  kararını kapsar.
- Bu belge merge edilse bile yalnızca *niyet ve sözleşmeyi* kayda geçirir; kod değişikliği
  başlatmaz. Gerçek v2.0 uygulaması ayrı, kabul kriterleri geçtikten sonra açılacak
  PR'larla ilerler.
