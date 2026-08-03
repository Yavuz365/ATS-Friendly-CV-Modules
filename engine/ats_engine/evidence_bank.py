"""
ats_engine.evidence_bank — Kanıt Bankası (Provenans / dürüstlük omurgası).

Framework CV (adayın tüm kariyerini içeren büyük belge) ham olarak değil, etiketli
girdilere ayrılmış bir 'kanıt bankası' olarak tutulur. Çıktı CV'sindeki HER madde,
bu bankadaki benzersiz bir girdiye (Input-ID) bağlanabilmelidir; bağlanamayan madde
uydurma riski taşır ve elenir. (synthesis-analysis-research'teki Source Registry'nin
CV'ye uygulanmış hali.)

Girdi formatı (esnek; '|' ile ayrık, key:value ya da konumsal):
  EXP-07 | Dış Ticaret | beceriler: [gümrükleme, KPI, landed cost] | metrik: süre −%30 | dönem: 2019–2022 | kanıt: "..."

Bağımlılık: yalnızca standart kütüphane (+ ats_engine.lexicons).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from . import lexicons

_ID = re.compile(r"^\s*((?:EXP|SKILL|EDU|CERT|PROJ)-\d+)\b", re.IGNORECASE)
_LIST = re.compile(r"\[(.*?)\]")


@dataclass
class Evidence:
    id: str
    domain: str = ""
    skills: list[str] = field(default_factory=list)
    metric: str = ""
    period: str = ""
    sentence: str = ""
    raw: str = ""

    def haystack(self) -> str:
        """Eşleştirme için birleşik metin."""
        return " ".join([self.domain, " ".join(self.skills), self.metric, self.sentence]).lower()


def _field_value(part: str) -> str:
    """'beceriler: x' -> 'x' ; düz değerse olduğu gibi."""
    if ":" in part:
        return part.split(":", 1)[1].strip()
    return part.strip()


def parse_line(line: str) -> Evidence | None:
    m = _ID.match(line)
    if not m:
        return None
    eid = m.group(1).upper()
    parts = [p.strip() for p in line.split("|")]
    ev = Evidence(id=eid, raw=line.strip())
    # ilk parça ID; sonrakileri anahtar kelimeye göre dağıt
    for part in parts[1:]:
        low = part.lower()
        if any(k in low for k in ["beceri", "skill"]):
            inner = _LIST.search(part)
            vals = inner.group(1) if inner else _field_value(part)
            ev.skills = [s.strip() for s in re.split(r"[,;]", vals) if s.strip()]
        elif any(k in low for k in ["metrik", "metric", "kpi", "sonuç", "result"]):
            ev.metric = _field_value(part)
        elif any(k in low for k in ["dönem", "donem", "period", "tarih", "date", "year", "yıl"]):
            ev.period = _field_value(part)
        elif any(k in low for k in ["kanıt", "kanit", "cümle", "evidence", "bullet", "açıklama"]):
            ev.sentence = _field_value(part).strip('"').strip()
        elif not ev.domain:
            ev.domain = part
        elif not ev.sentence:
            ev.sentence = part.strip('"').strip()
    return ev


def parse_bank(text: str) -> list[Evidence]:
    """Etiketli Framework CV metnini Evidence girdilerine ayrıştırır."""
    out: list[Evidence] = []
    for line in (text or "").splitlines():
        ev = parse_line(line)
        if ev:
            out.append(ev)
    return out


def find_support(claim: str, bank: list[Evidence], min_overlap: float = 0.18) -> tuple[Evidence | None, float]:
    """
    Bir CV iddiasını destekleyen en iyi kanıt girdisini bulur (token örtüşmesi + Jaccard).
    Döner: (girdi | None, skor). Skor min_overlap altındaysa destek yok sayılır.
    """
    best, best_score = None, 0.0
    claim_low = (claim or "").lower()
    claim_tokens = set(re.findall(r"[a-zA-ZçÇğĞıİöÖşŞüÜ0-9]+", claim_low))
    for ev in bank:
        hay = ev.haystack()
        hay_tokens = set(re.findall(r"[a-zA-ZçÇğĞıİöÖşŞüÜ0-9]+", hay))
        if not hay_tokens:
            continue
        overlap = len(claim_tokens & hay_tokens) / max(1, len(claim_tokens))
        jac = lexicons.jaccard(claim_low, hay)
        score = max(overlap, jac)
        # beceri birebir geçiyorsa güçlü sinyal
        if any(s.lower() in claim_low for s in ev.skills if s):
            score = max(score, 0.5)
        if score > best_score:
            best, best_score = ev, score
    if best_score < min_overlap:
        return None, round(best_score, 3)
    return best, round(best_score, 3)


def provenance_check(cv_bullets: list[str], bank: list[Evidence]) -> dict:
    """
    Her CV maddesini kanıt bankasına bağlamaya çalışır. Çıktı:
      table: [{cv_bullet, framework_cv_id, support_score, status}]
      unverified: bağlanamayan maddeler (CV'den çıkarılmalı/işaretlenmeli)
      pass: tüm maddeler bağlandıysa True (dürüstlük geçişi)
    """
    table = []
    unverified = []
    for bullet in cv_bullets:
        ev, score = find_support(bullet, bank)
        if ev:
            table.append({"cv_bullet": bullet, "framework_cv_id": ev.id,
                          "support_score": score, "status": "doğrulandı"})
        else:
            table.append({"cv_bullet": bullet, "framework_cv_id": None,
                          "support_score": score, "status": "İŞARETLİ — kanıt yok"})
            unverified.append(bullet)
    return {"table": table, "unverified": unverified, "pass": len(unverified) == 0,
            "bank_entries": [asdict(e) for e in bank]}
