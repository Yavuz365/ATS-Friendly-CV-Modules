"""
ats_engine.calibration — Jobscan-Parity Feedback Loop (Y36-18).

Engine skoru ile Jobscan skoru arasındaki farkı ölçer ve kalibre eder.
Hedef: Engine %86.7 diyorsa Jobscan da ~85+ vermeli.

Kalibrasyon tablosu: Birden fazla JD ile test edip sistematik sapma ölç.

Bağımlılık: yalnızca standart kütüphane.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CalibrationEntry:
    """Tek bir JD için engine vs Jobscan karşılaştırması."""
    jd_name: str
    engine_score: float  # %
    jobscan_score: float  # %
    delta: float = 0.0  # engine - jobscan

    def __post_init__(self):
        self.delta = round(self.engine_score - self.jobscan_score, 1)


@dataclass
class CalibrationReport:
    """Çok-JD kalibrasyon raporu."""
    entries: list[CalibrationEntry] = field(default_factory=list)
    mean_delta: float = 0.0
    std_delta: float = 0.0
    bias_direction: str = ""  # "engine_inflated" | "engine_deflated" | "aligned"
    verdict: str = ""

    def compute(self):
        if not self.entries:
            self.verdict = "⚠️ Kalibrasyon verisi yok"
            return
        deltas = [e.delta for e in self.entries]
        n = len(deltas)
        self.mean_delta = round(sum(deltas) / n, 1)
        variance = sum((d - self.mean_delta) ** 2 for d in deltas) / n
        self.std_delta = round(variance ** 0.5, 1)

        if self.mean_delta > 5:
            self.bias_direction = "engine_inflated"
            self.verdict = f"⚠️ Engine ortalama +{self.mean_delta}pp şişiriyor (σ={self.std_delta})"
        elif self.mean_delta < -5:
            self.bias_direction = "engine_deflated"
            self.verdict = f"⚠️ Engine ortalama {self.mean_delta}pp düşük veriyor (σ={self.std_delta})"
        else:
            self.bias_direction = "aligned"
            self.verdict = f"✅ Engine ve Jobscan arasında iyi korelasyon (Δ={self.mean_delta}pp, σ={self.std_delta})"


def create_calibration(
    jd_results: list[tuple[str, float, float]],
) -> CalibrationReport:
    """
    Kalibrasyon raporu oluştur.

    Args:
        jd_results: [(jd_name, engine_score, jobscan_score), ...]

    Returns:
        CalibrationReport
    """
    entries = [
        CalibrationEntry(name, engine, jobscan)
        for name, engine, jobscan in jd_results
    ]
    report = CalibrationReport(entries=entries)
    report.compute()
    return report


def suggest_weight_adjustment(report: CalibrationReport) -> dict:
    """
    Kalibrasyon raporuna göre ağırlık ayarlama önerisi.

    Returns:
        {"adjustment": str, "suggested_changes": [...]}
    """
    if not report.entries:
        return {"adjustment": "none", "suggested_changes": []}

    suggestions = []
    if report.bias_direction == "engine_inflated":
        suggestions.append("Lex ağırlığını 0.35 → 0.30 düşür (semantik şişirme)")
        suggestions.append("Coverage eşiğini %50 → %60 artır")
        suggestions.append("Anti-stuffing cezasını sıkılaştır")
    elif report.bias_direction == "engine_deflated":
        suggestions.append("SBERT ağırlığını artır (semantik eşleşme eksik)")
        suggestions.append("skill_synonyms genişlet (eşanlamlı bulamama)")

    return {
        "adjustment": report.bias_direction,
        "mean_delta": report.mean_delta,
        "suggested_changes": suggestions or ["Ayarlama gerekmiyor — skorlar uyumlu"],
    }
