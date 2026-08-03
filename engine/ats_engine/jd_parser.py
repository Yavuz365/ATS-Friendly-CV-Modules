"""
ats_engine.jd_parser — İş İlanı (JD) 7 Katmanlı Ayrıştırıcı (ANALİZ katmanı).

jd-decomposition.md'deki şemanın DETERMINISTIK, heuristik bir uygulamasıdır:
  1) Kimlik   2) Zorunlu   3) Tercih   4) Sorumluluk/eylem
  5) Niyet    6) Semantik/LSI         7) Ağırlık metası

DÜRÜST SINIR: Bu, bir LLM değildir; kurallara dayalı bir ilk-geçiş iskeletidir.
Skill'in tam gücü LLM (Claude / Master Prompt) ile gelir; bu modül tutarlı,
tekrarlanabilir bir taban + 'gerçek sayı' üretir ve LLM çıktısını çapalar.

Bağımlılık: yalnızca standart kütüphane (+ ats_engine.lexicons, text).
"""

from __future__ import annotations

import re
from collections import Counter

from . import lexicons
from .text import sentences, tokenize, tr_lower

# Bölüm başlığı ipuçları (TR + EN).
_MUST_CUES = re.compile(r"(aranan nitelik|gerekli|gereklilik|zorunlu|şart|olmazsa olmaz|must[- ]?have|requirements?|required|qualifications?)", re.IGNORECASE)
_NICE_CUES = re.compile(r"(tercih|tercihen|artı|avantaj|nice[- ]?to[- ]?have|preferred|plus|bonus|a plus)", re.IGNORECASE)
_RESP_CUES = re.compile(r"(sorumluluk|görev|ne yapacak|yapacağınız|responsibilit|duties|what you.?ll do|role)", re.IGNORECASE)

# Kıdem sözlüğü.
_SENIORITY = [
    (re.compile(r"\b(lead|principal|head|director|chief|müdür|direktör|şef)\b", re.IGNORECASE), "lead"),
    (re.compile(r"\b(senior|sr\.?|kıdemli|uzman)\b", re.IGNORECASE), "senior"),
    (re.compile(r"\b(mid|orta|deneyimli)\b", re.IGNORECASE), "mid"),
    (re.compile(r"\b(junior|jr\.?|stajyer|intern|entry)\b", re.IGNORECASE), "junior"),
]

_WORK_MODE = [
    (re.compile(r"\b(remote|uzaktan|home[- ]?office)\b", re.IGNORECASE), "remote"),
    (re.compile(r"\b(hybrid|hibrit|karma)\b", re.IGNORECASE), "hybrid"),
    (re.compile(r"\b(on[- ]?site|ofis|yerinde)\b", re.IGNORECASE), "on-site"),
]

# P0-8/9 fix: eskiden TEK bir regex hem dil adını hem seviye kodunu (c1/b2 vb.)
# aynı düz listeye basıyordu → "dil: Almanca, B2, C1, İngilizce" gibi eşleşmemiş,
# anlamsız bir liste üretiyordu (dil ile seviye HİÇ eşleştirilmiyordu). Artık iki
# ayrı regex var; _parse_language_requirements() bunları segment bazında eşleştirir.
_LANG_NAMES = re.compile(
    r"\b(ingilizce|english|almanca|german|fransızca|french|ispanyolca|spanish|"
    r"rusça|russian|arapça|arabic|çince|chinese|italyanca|italian|portekizce|portuguese)\b",
    re.IGNORECASE,
)
_LANG_LEVEL = re.compile(
    r"\b(c1|c2|b1|b2|a1|a2|akıcı|fluent|native|anadil|advanced|ileri|orta)\b",
    re.IGNORECASE,
)


def _parse_language_requirements(text: str) -> list[dict]:
    """
    Dil adlarını, en yakın segmentteki seviye kodlarıyla EŞLEŞTİRİR.

    P0-8 fix: önceki tek-regex yaklaşımı "Almanca, B2, C1, İngilizce" gibi bir
    ilan metninden ['almanca','b2','c1','ingilizce'] gibi 4 ayrı, eşleşmemiş öğe
    üretiyordu (dil-seviye ilişkisi tamamen kayboluyordu). Bu fonksiyon metni
    cümle/segment (nokta, satır, noktalı virgül) bazında bölüp her segmentteki
    dil(ler)i, o segmentteki seviye kod(lar)ıyla eşleştirir.
    """
    out: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for seg in re.split(r"[.\n;]", text or ""):
        lang_matches = list(_LANG_NAMES.finditer(seg))
        if not lang_matches:
            continue
        level_matches = list(_LANG_LEVEL.finditer(seg))
        used: set[int] = set()
        for lm in lang_matches:
            lang = lm.group(0)
            # Önce dil adından SONRA gelen en yakın (kullanılmamış) seviyeyi tercih et
            # (en yaygın kalıp: "İngilizce (C1)"); yoksa en yakın öncesi seviyeye düş.
            after = [(i, vm) for i, vm in enumerate(level_matches)
                     if i not in used and vm.start() >= lm.start()]
            if after:
                idx, vm = min(after, key=lambda p: p[1].start() - lm.start())
            else:
                before = [(i, vm) for i, vm in enumerate(level_matches) if i not in used]
                idx, vm = (min(before, key=lambda p: abs(p[1].start() - lm.start()))
                           if before else (None, None))
            level = None
            if vm is not None:
                level = vm.group(0)
                used.add(idx)
            key = (tr_lower(lang), tr_lower(level or ""))
            if key in seen:
                continue
            seen.add(key)
            out.append({"language": tr_lower(lang), "level": tr_lower(level) if level else None})
    return out

# Deneyim yılı.
_YEARS = re.compile(r"(\d+\s?[-–+]?\s?\d*)\s?(yıl|sene|years?|yr)", re.IGNORECASE)

# Sertifika/akronim adayı (büyük harf 2-6 harf, ya da bilinen kalıplar).
_ACRONYM = re.compile(r"\b([A-ZÇĞİÖŞÜ]{2,6}(?:[/-][A-ZÇĞİÖŞÜ]{1,5})?)\b")
_CERTS = ["pmp", "cpa", "cfa", "scrum master", "six sigma", "prince2", "itil", "aws", "iso 9001", "yys", "aeo"]

# P0-10 fix: _ACRONYM regex'i büyük harfli her 2-6 harfi yakalar (birim, kısaltma,
# rastgele büyük harfli kelime dahil). Bir "must" bölge başlığı bulunamayıp gövdeden
# zorunlu terim türetilirken bu tür anlamsız/gürültü kısaltmaların önerilen listeye
# girmesini önlemek için küçük bir kara liste (birim/bağlaç kısaltmaları).
_NOISE_ACRONYMS = {"mm", "cm", "km", "kg", "gr", "lt", "ml", "vb", "vs", "no"}

# Knockout (ikili eler) ipuçları.
_KNOCKOUT = re.compile(r"(çalışma izni|work permit|askerlik|ehliyet|driver.?s license|seyahat engeli|relocat|vatandaş|citizen)", re.IGNORECASE)


def _segment(text: str) -> dict[str, str]:
    """JD'yi kaba bölgelere ayırır: must / nice / resp / body (başlık satırlarına göre).

    P0-10b fix: eskiden yalnız "satırın TAMAMI kısa VEYA ':' ile biter" kalıbı başlık
    sayılıyordu. Çok yaygın tek-satırlık "Zorunlu: A, B, C." biçimi (etiket + aynı
    satırda içerik, satır 8 kelimeden uzun) bu şartı hiç sağlamıyordu → JD'de açıkça
    yazan zorunlu şartlar bile "explicit" değil "inferred_from_body" sayılıyordu.
    Artık satırın ilk ':' karakterinden ÖNCEKİ kısa etiket ayrıca kontrol edilir; eşleşirse
    ':'den SONRAKİ içerik o bölgeye eklenir (atlanmaz).
    """
    lines = [ln for ln in (text or "").splitlines()]
    region = "body"
    buckets = {"must": [], "nice": [], "resp": [], "body": []}
    for line in lines:
        stripped = line.strip()
        colon_idx = stripped.find(":")
        label = stripped[:colon_idx].strip() if 0 <= colon_idx <= 40 else None

        if label and _MUST_CUES.search(label):
            region = "must"
            remainder = stripped[colon_idx + 1:].strip()
            if remainder:
                buckets["must"].append(remainder)
                buckets["body"].append(remainder)
            continue
        if label and _NICE_CUES.search(label):
            region = "nice"
            remainder = stripped[colon_idx + 1:].strip()
            if remainder:
                buckets["nice"].append(remainder)
                buckets["body"].append(remainder)
            continue
        if label and _RESP_CUES.search(label):
            region = "resp"
            remainder = stripped[colon_idx + 1:].strip()
            if remainder:
                buckets["resp"].append(remainder)
                buckets["body"].append(remainder)
            continue

        # eski davranış: yalnız-başlık satırı (kısa satır, ':' yok veya içerik yok)
        is_heading = len(stripped) <= 80 and (stripped.endswith(":") or len(stripped.split()) <= 8)
        if is_heading and _MUST_CUES.search(stripped):
            region = "must"
            continue
        if is_heading and _NICE_CUES.search(stripped):
            region = "nice"
            continue
        if is_heading and _RESP_CUES.search(stripped):
            region = "resp"
            continue
        buckets[region].append(line)
        buckets["body"].append(line)
    return {k: "\n".join(v) for k, v in buckets.items()}


def _known_skills(text: str) -> list[str]:
    """Bilinen kanonik becerileri (skill_synonyms tabanlı) ve sertifika/akronimleri çıkarır."""
    found: dict[str, None] = {}
    low = tr_lower(text or "")
    # kanonik beceriler: her n-gram'ı normalize etmeye çalış
    toks = tokenize(text, ngram_max=3)
    for t in toks:
        canon = lexicons.normalize_skill(t)
        if canon:
            found[canon] = None
    # sertifikalar
    for c in _CERTS:
        if c in low:
            found[c.upper() if len(c) <= 4 else c.title()] = None
    # serbest akronimler (SAP, GTIP, REACH, KPI...)
    for m in _ACRONYM.findall(text or ""):
        if tr_lower(m) not in ("cv", "ats", "ik", "hr"):
            found[m] = None
    return list(found.keys())


def _intent(text: str, must: list[str], resp_verbs: list[str]) -> str:
    """Rolün özünü tek cümlede tahmin eden heuristik (denetçi mi memur mu vb.)."""
    low = tr_lower(text or "")
    audit_signals = sum(low.count(w) for w in ["denetim", "denetle", "uyum", "compliance", "audit", "raporla", "report", "kontrol", "control", "iyileştir", "optimi"])
    strategy_signals = sum(low.count(w) for w in ["strateji", "strategy", "büyüme", "growth", "yönet", "manage", "lead", "liderlik"])
    base = "Bu rol esasen "
    if audit_signals >= 3 and audit_signals > strategy_signals:
        return base + "rutin bir operasyon memuru değil; süreçleri denetleyen/iyileştiren bir DENETÇİ-OPTİMİZASYON profili arıyor."
    if strategy_signals >= 3:
        return base + "yürütmenin ötesinde STRATEJİ ve EKİP/PAYDAŞ yönetimi yapan bir profil arıyor."
    top = ", ".join(must[:3]) if must else (", ".join(resp_verbs[:3]) if resp_verbs else "temel rol gereksinimleri")
    return base + f"şu çekirdek yetkinlikleri arıyor: {top}."


def parse_jd(text: str, first_window: int = 150) -> dict:
    """
    JD'yi 7 katmanlı yapıya ayrıştırır ve her terime ağırlık metası bağlar.
    Çıktı şeması jd-decomposition.md ile uyumludur ve scoring/synthesis'in girdisidir.
    """
    seg = _segment(text)
    head_words = tr_lower(" ".join((text or "").split()[:first_window]))
    freq = Counter(tokenize(text, ngram_max=3))

    # --- Katman 1: Kimlik ---
    first_line = next((ln.strip() for ln in (text or "").splitlines() if ln.strip()), "")
    seniority = next((label for rx, label in _SENIORITY if rx.search(text or "")), "unspecified")
    work_mode = next((label for rx, label in _WORK_MODE if rx.search(text or "")), "unspecified")
    lang = _parse_language_requirements(text or "")
    years = _YEARS.search(text or "")
    identity = {
        "title_guess": first_line[:120],
        "seniority": seniority,
        "work_mode": work_mode,
        "language_req": lang,
        "experience_years": years.group(0) if years else None,
    }

    # --- Katman 2/3: Zorunlu / Tercih ---
    # P0-10 fix: eskiden "must" bölge başlığı (ör. "Aranan Nitelikler:") hiç
    # bulunamazsa, ilanın GÖVDESİNDEN çıkan HERHANGİ bir 2-6 harfli büyük harf
    # kısaltma (ör. anlamsız "MM") doğrudan modality=1.0 "zorunlu" sayılıyordu.
    # Artık: (a) has_explicit_must=False ise bu terimler modality=0.6 (rapor
    # katmanında "tercih" bandına düşer, "zorunlu" DENMEZ) ile işaretlenir,
    # (b) tek başına anlamsız/gürültü kısaltmalar (ölçü birimleri vb.) filtrelenir.
    has_explicit_must = bool(seg["must"].strip())
    must_skills = _known_skills(seg["must"]) if has_explicit_must else []
    nice_skills = _known_skills(seg["nice"]) if seg["nice"].strip() else []
    body_skills = _known_skills(seg["body"])
    if not must_skills:
        must_skills = [
            s for s in body_skills
            if s not in nice_skills and tr_lower(s) not in _NOISE_ACRONYMS
        ][:12]
    # knockouts
    knockouts = sorted({m.group(0) for m in _KNOCKOUT.finditer(text or "")})

    def classify(term: str) -> str:
        low = tr_lower(term)
        if low in [c for c in _CERTS] or any(c in low for c in ["pmp", "cpa", "cfa", "iso", "aeo", "yys"]):
            return "cert"
        if any(k in low for k in ["sap", "erp", "python", "sql", "aws", "excel", "tableau", "power bi"]):
            return "tool"
        return "skill"

    # --- Katman 4: Sorumluluk / eylem fiilleri ---
    verbs = lexicons.all_action_verbs()
    resp_text = seg["resp"] if seg["resp"].strip() else (text or "")
    resp_verbs = []
    for s in sentences(resp_text):
        for w in re.findall(r"[a-zA-ZçÇğĞıİöÖşŞüÜ]+", tr_lower(s)):
            if w in verbs and w not in resp_verbs:
                resp_verbs.append(w)
    # TR sorumluluk fiilleri (kaba): -er/-ir ile biten yönetimsel fiiller
    for m in re.findall(r"\b(yönet\w*|koordine\w*|denetle\w*|raporla\w*|optimi\w*|planla\w*|geliştir\w*|takip\w*)\b", tr_lower(resp_text)):
        if m not in resp_verbs:
            resp_verbs.append(m)

    # --- Katman 7: Ağırlık metası (her terim için) ---
    def weight_meta(term: str, region: str) -> dict:
        low = tr_lower(term)
        f = freq.get(low, 0) or sum(freq.get(tr_lower(v), 0) for v in lexicons.expand_lsi(low)) or 1
        # modality: bölge + tekrar/merkezîlik
        if region == "must":
            # P0-10 fix: ilanda açık bir "Aranan Nitelikler/Zorunlu" bölümü YOKSA,
            # gövdeden türetilen terimler artık tam "zorunlu" (1.0) sayılmıyor —
            # 0.6 ile işaretlenir (report.py'de "tercih" bandına düşer, "zorunlu"
            # etiketi YALNIZCA ilanda açıkça yazan şartlara verilir).
            modality = 1.0 if has_explicit_must else 0.6
        elif region == "nice":
            modality = 0.3
        else:
            modality = 0.7 if (f >= 2 or low in head_words) else 0.5
        positional = 1.3 if low in head_words else 1.0
        return {"term": term, "type": classify(term), "modality": modality,
                "positional_weight": positional, "freq": f}

    must_meta = [weight_meta(t, "must") for t in must_skills]
    nice_meta = [weight_meta(t, "nice") for t in nice_skills]

    # --- Katman 6: Semantik / LSI ---
    lsi = {t: lexicons.expand_lsi(t) for t in must_skills if lexicons.expand_lsi(t)}

    # --- Katman 5: Niyet ---
    intent = _intent(text, must_skills, resp_verbs)

    return {
        "identity": identity,
        "must_have": must_meta,
        "nice_to_have": nice_meta,
        "responsibilities": resp_verbs,
        "intent": intent,
        "lsi": lsi,
        "knockouts": knockouts,
        # P0-10 fix: şeffaflık alanı — "must_have" listesinin ilanda AÇIKÇA yazan bir
        # zorunlu-şartlar bölümünden mi geldiği, yoksa gövdeden mi TAHMİN edildiği.
        "must_have_source": "explicit" if has_explicit_must else "inferred_from_body",
        "_scoring_weights": {  # scoring.coverage() için doğrudan kullanılabilir ağırlık tablosu
            tr_lower(m["term"]): round(m["modality"] * m["positional_weight"], 3) for m in must_meta
        },
        "_must_terms": [m["term"] for m in must_meta],
    }
