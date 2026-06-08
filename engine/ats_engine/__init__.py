"""
ats_engine — ATS-Friendly-CV-Modules Engine (çekirdek motor).

'Önce çöz (ANALİZ) → yeniden bağla (SENTEZ) → ölç (SKOR + GAP) → gerekirse yeniden bağla'
diyalektik döngüsünün deterministik, çalışır Python uygulaması.

Genel API:
    from ats_engine import parse_jd, ats_match_score, build_report, parse_bank
    rapor = build_report(jd_text, framework_cv_text, cv_text=None)

Katmanlar:
    text          — tokenizasyon, n-gram, durak kelime, dil-kalitesi
    bm25          — Okapi BM25
    scoring       — TF-IDF kosinüs, (ops.) SBERT, hibrit ATS Match Score
    lexicons      — Grammarly-türevli aktif fiiller + beceri normalizasyonu/LSI
    jd_parser     — 7 katmanlı JD ayrıştırması
    evidence_bank — Framework CV → kanıt bankası + provenans
    synthesis     — XYZ/CAR, kümeleme, gap sınıflandırma, anti-stuffing
    report        — 6 alanlık çıktı (JSON + Markdown)
"""

from .scoring import ats_match_score, tfidf_cosine, coverage, prf, DEFAULTS, THRESHOLDS
from .jd_parser import parse_jd
from .evidence_bank import parse_bank, provenance_check, Evidence
from .synthesis import (
    build_xyz, build_car, audit_bullet, cluster_skills,
    classify_gaps, stopping_condition, anti_stuffing_report,
)
from .report import build_report, to_json, to_markdown
from . import lexicons, text

from .multilevel import (
    level1_gate, level2_best_of, level2_final, level3_category,
    lang_gate, language_purity, detect_language,
    SECTION_LABELS, L1_GATE_THRESHOLD, L2_SEAM_PENALTY,
)

__version__ = "1.1.0"

__all__ = [
    "ats_match_score", "tfidf_cosine", "coverage", "prf", "DEFAULTS", "THRESHOLDS",
    "parse_jd", "parse_bank", "provenance_check", "Evidence",
    "build_xyz", "build_car", "audit_bullet", "cluster_skills",
    "classify_gaps", "stopping_condition", "anti_stuffing_report",
    "build_report", "to_json", "to_markdown",
    "level1_gate", "level2_best_of", "level2_final", "level3_category",
    "lang_gate", "language_purity", "detect_language",
    "SECTION_LABELS", "L1_GATE_THRESHOLD", "L2_SEAM_PENALTY",
    "lexicons", "text", "__version__",
]
