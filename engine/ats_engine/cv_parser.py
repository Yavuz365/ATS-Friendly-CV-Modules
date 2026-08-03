"""
ats_engine.cv_parser — CV metin ayrıştırıcı.

CV'yi ATS-güvenli bölümlere ayırır, bölüm tespiti yapar ve
ayrıştırılabilirlik güvenlik skoru hesaplar.

ATS sistemleri düz metin (plain text) parse eder. Bu modül:
  1. section_detect() — CV'den bölüm sınırlarını bulur
  2. parse()          — yapılandırılmış CVSchema çıkarır
  3. parse_safety_score() — ATS uyumlu biçim güvenlik skoru [0, 1]

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ─── Bölüm etiketleri ve regex'ler ──────────────────────────────────────────

_SECTION_PATTERNS: dict[str, re.Pattern] = {
    "summary": re.compile(
        r"(?i)^(?:summary|profess?ional\s*summary|profile|özet|profil|kariyer\s*özeti|executive\s*summary)",
    ),
    "experience": re.compile(
        r"(?i)^(?:experience|work\s*experience|professional\s*experience|"
        r"deneyim|iş\s*deneyimi|mesleki\s*deneyim|employment)",
    ),
    "education": re.compile(
        r"(?i)^(?:education|eğitim|öğrenim|academic|akademik)",
    ),
    "skills": re.compile(
        r"(?i)^(?:skills|technical\s*skills|core\s*competencies|"
        r"beceriler|yetkinlikler|teknik\s*beceriler|competencies)",
    ),
    "certifications": re.compile(
        r"(?i)^(?:certifications?|certificates?|licenses?|"
        r"sertifikalar?|belgeler?|lisanslar?)",
    ),
    "languages": re.compile(
        r"(?i)^(?:languages?|diller?|yabancı\s*dil)",
    ),
    "projects": re.compile(
        r"(?i)^(?:projects?|notable\s*projects?|projeler?)",
    ),
    "awards": re.compile(
        r"(?i)^(?:awards?|honors?|achievements?|ödüller?|başarılar?)",
    ),
    "publications": re.compile(
        r"(?i)^(?:publications?|yayınlar?)",
    ),
    "references": re.compile(
        r"(?i)^(?:references?|referanslar?)",
    ),
}

# ATS-kırıcı biçim tespit regex'leri
_TABLE_PATTERN = re.compile(r"[|┌┐└┘├┤┬┴┼─│]")
_MULTI_COLUMN = re.compile(r"\t{2,}|\s{8,}")  # çift sütun belirteci
_IMAGE_REF = re.compile(r"(?i)!\[.*?\]\(.*?\)|<img\s|data:image")
_HEADER_FOOTER = re.compile(r"(?i)^(?:page\s*\d+|confidential|curriculum\s*vitae)\s*$")
# Y36-9: Genişletilmiş özel karakter regex'i — middle dot, em/en-dash,
# smart quotes, emoji, ve diğer ATS-kırıcı semboller.
_SPECIAL_CHARS = re.compile(
    r"[★☆●◆▪▸►■□▶✓✗✔✘→←↑↓♦♣♠♥"
    r"·‧∙"                          # middle dot varyantları
    r"—–"                           # em-dash, en-dash
    r"\u201c\u201d\u2018\u2019"     # smart quotes: "" ''
    r"«»"                           # guillemets
    r"…"                            # ellipsis
    r"•‣⁃"                          # bullet varyantları
    r"℃℉™®©"                       # semboller
    r"\U0001F300-\U0001F9FF"        # emoji bloğu
    r"]"
)


@dataclass
class CVSection:
    """Tek bir CV bölümü."""
    label: str
    text: str
    start_line: int
    end_line: int


@dataclass
class CVSchema:
    """Ayrıştırılmış CV yapısı."""
    sections: dict[str, CVSection] = field(default_factory=dict)
    raw_text: str = ""
    unmatched_lines: list[str] = field(default_factory=list)


def section_detect(text_input: str) -> dict[str, str]:
    """
    CV metninden bölüm sınırlarını tespit eder.

    Returns:
        {bölüm_adı: bölüm_metni} sözlüğü. Tanınmayan satırlar
        'unmatched' anahtarında toplanır.
    """
    lines = text_input.split("\n")
    sections: list[tuple[str, int]] = []

    for i, line in enumerate(lines):
        stripped = line.strip().rstrip(":")
        if not stripped:
            continue
        for label, pattern in _SECTION_PATTERNS.items():
            if pattern.match(stripped):
                sections.append((label, i))
                break

    result: dict[str, str] = {}
    unmatched_lines: list[str] = []

    if not sections:
        return {"unmatched": text_input}

    # Bölümden önceki satırlar → unmatched
    pre_lines = lines[:sections[0][1]]
    if any(ln.strip() for ln in pre_lines):
        unmatched_lines.extend(pre_lines)

    for idx, (label, start) in enumerate(sections):
        end = sections[idx + 1][1] if idx + 1 < len(sections) else len(lines)
        block = "\n".join(lines[start:end]).strip()

        # Aynı etiket birden fazla kez geçebilir (örn. experience)
        if label in result:
            count = sum(1 for k in result if k.startswith(label))
            label = f"{label}_{count + 1}"
        result[label] = block

    if unmatched_lines:
        result["unmatched"] = "\n".join(unmatched_lines).strip()

    return result


def parse(text_input: str) -> CVSchema:
    """
    CV metnini yapılandırılmış CVSchema'ya dönüştürür.
    """
    raw_sections = section_detect(text_input)
    lines = text_input.split("\n")
    schema = CVSchema(raw_text=text_input)

    for label, content in raw_sections.items():
        if label == "unmatched":
            schema.unmatched_lines = [ln for ln in content.split("\n") if ln.strip()]
            continue

        # Satır numaralarını bul
        start = 0
        for i, line in enumerate(lines):
            if content.split("\n")[0].strip() in line:
                start = i
                break
        end = start + len(content.split("\n"))

        schema.sections[label] = CVSection(
            label=label,
            text=content,
            start_line=start,
            end_line=end,
        )

    return schema


def parse_safety_score(text_input: str) -> dict:
    """
    CV'nin ATS ayrıştırılabilirlik güvenlik skorunu hesaplar [0, 1].

    Cezalar:
      - Tablo/grafik kullanımı → −0.15
      - Çift sütun (tab/boşluk) → −0.20
      - Resim referansı → −0.10
      - Özel karakterler (★●◆) → −0.05
      - Header/footer tekrarı → −0.05
      - Bölüm başlığı bulunamadı → −0.10
      - Çok kısa metin (<100 kelime) → −0.15

    Returns:
        {"score": float, "penalties": list, "recommendation": str}
    """
    score = 1.0
    penalties: list[dict[str, str | float]] = []

    # Tablo
    if _TABLE_PATTERN.search(text_input):
        score -= 0.15
        penalties.append({"type": "table_graphics", "penalty": -0.15,
                          "detail": "Tablo/grafik karakterleri tespit edildi — ATS parser çoğunu yok sayar"})

    # Çift sütun
    if _MULTI_COLUMN.search(text_input):
        score -= 0.20
        penalties.append({"type": "multi_column", "penalty": -0.20,
                          "detail": "Çift sütun düzeni tespit edildi — ATS parse sırasını bozar"})

    # Resim
    if _IMAGE_REF.search(text_input):
        score -= 0.10
        penalties.append({"type": "image_reference", "penalty": -0.10,
                          "detail": "Resim referansı tespit edildi — ATS görselleri okuyamaz"})

    # Özel karakterler
    special_count = len(_SPECIAL_CHARS.findall(text_input))
    if special_count > 3:
        score -= 0.05
        penalties.append({"type": "special_chars", "penalty": -0.05,
                          "detail": f"{special_count} özel karakter — bazı ATS'ler bunları yanlış parse eder"})

    # Header/footer
    header_hits = len(_HEADER_FOOTER.findall(text_input))
    if header_hits > 1:
        score -= 0.05
        penalties.append({"type": "header_footer", "penalty": -0.05,
                          "detail": "Tekrarlayan header/footer — ATS bunları içerik olarak okuyabilir"})

    # Bölüm tespiti
    sections = section_detect(text_input)
    recognized = [k for k in sections if k != "unmatched"]
    if len(recognized) < 2:
        score -= 0.10
        penalties.append({"type": "no_sections", "penalty": -0.10,
                          "detail": "2'den az tanınabilir bölüm başlığı — ATS yapısal parse yapamaz"})

    # Çok kısa metin
    word_count = len(text_input.split())
    if word_count < 100:
        score -= 0.15
        penalties.append({"type": "too_short", "penalty": -0.15,
                          "detail": f"Metin çok kısa ({word_count} kelime) — yeterli içerik yok"})

    score = max(0.0, min(1.0, score))

    if score >= 0.90:
        rec = "Mükemmel ATS uyumu — güvenle gönderilebilir"
    elif score >= 0.70:
        rec = "İyi ATS uyumu — küçük düzeltmeler önerilir"
    elif score >= 0.50:
        rec = "Orta ATS uyumu — biçim düzeltmeleri gerekli"
    else:
        rec = "Düşük ATS uyumu — CV biçimi baştan gözden geçirilmeli"

    return {
        "score": round(score, 2),
        "penalties": penalties,
        "recommendation": rec,
        "word_count": word_count,
        "sections_found": recognized,
    }
