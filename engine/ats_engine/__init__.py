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

from . import lexicons, text
from .calibration import create_calibration, suggest_weight_adjustment
from .cliche_tone import detect_cliches

# Faz 1 modülleri
from .completeness_guard import evidence_recall
from .domain_packs import (
    all_keywords,
    detect_domain,
    enrich_must_terms,
    keywords_by_category,
    list_packs,
    load_pack,
)
from .evidence_bank import Evidence, parse_bank, provenance_check
from .format_metadata_hygiene import full_hygiene_check
from .jd_parser import parse_jd
from .locale_consistency import detect_locale, locale_mismatches
from .multilevel import (
    L1_GATE_THRESHOLD,
    L2_SEAM_PENALTY,
    SECTION_LABELS,
    detect_language,
    lang_gate,
    language_purity,
    level1_gate,
    level2_best_of,
    level2_final,
    level3_category,
)
from .quantification_score import quantification_audit
from .report import build_report, to_json, to_markdown
from .scoring import DEFAULTS, THRESHOLDS, ats_match_score, coverage, prf, tfidf_cosine
from .synthesis import (
    anti_stuffing_report,
    audit_bullet,
    build_car,
    build_xyz,
    classify_gaps,
    cluster_skills,
    stopping_condition,
)
from .text import tr_lower

__version__ = "1.5.0"

__all__ = [
    "DEFAULTS",
    "L1_GATE_THRESHOLD",
    "L2_SEAM_PENALTY",
    "SECTION_LABELS",
    "THRESHOLDS",
    "Evidence",
    "__version__",
    "all_keywords",
    "anti_stuffing_report",
    "ats_match_score",
    "audit_bullet",
    "build_car",
    "build_report",
    "build_xyz",
    "classify_gaps",
    "cluster_skills",
    "coverage",
    "create_calibration",
    "detect_cliches",
    "detect_domain",
    "detect_language",
    "detect_locale",
    "enrich_must_terms",
    "evidence_recall",
    "full_hygiene_check",
    "keywords_by_category",
    "lang_gate",
    "language_purity",
    "level1_gate",
    "level2_best_of",
    "level2_final",
    "level3_category",
    "lexicons",
    "list_packs",
    "load_pack",
    "locale_mismatches",
    "parse_bank",
    "parse_jd",
    "prf",
    "provenance_check",
    "quantification_audit",
    "stopping_condition",
    "suggest_weight_adjustment",
    "text",
    "tfidf_cosine",
    "to_json",
    "to_markdown",
    "tr_lower",
]
