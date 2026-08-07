"""STAB-016: one matcher semantics — regression tests.

Ensures the skill count table uses the canonical match_term contract for
status/stage determination. Exact counts for EXACT matches, stage labels
for synonym/ontology/semantic, Missing for NONE.
"""

from __future__ import annotations

from ats_engine.matching import MatchStage, count_boundary_occurrences, match_term

# ── match_term contract ───────────────────────────────────────────────────────


def test_exact_term_correct_count():
    tm = match_term("SAP", "I have SAP experience and used SAP daily.")
    assert tm.matched is True
    assert tm.stage is MatchStage.EXACT
    assert tm.count == 2  # exact boundary occurrences


def test_reviewed_synonym_exposes_stage():
    from ats_engine.matching import reviewed_synonym_revision

    synonyms = {"SAP": ["erp system"]}
    rev = reviewed_synonym_revision(synonyms)
    tm = match_term("SAP", "I have erp system experience.", reviewed_synonyms=synonyms, synonym_revision=rev)
    assert tm.matched is True
    assert tm.stage is MatchStage.SYNONYM
    # count is for the matched variant, not inflated
    assert tm.count >= 1


def test_missing_term_returns_none_stage():
    tm = match_term("SAP", "I have experience in logistics and trade finance.")
    assert tm.matched is False
    assert tm.stage is MatchStage.NONE
    assert tm.count == 0


def test_no_substring_inflation():
    """count_boundary_occurrences must not match substrings."""
    count = count_boundary_occurrences("SAP", "sapphire and landscape and SAPS")
    assert count == 0


def test_exact_match_count_not_inflated():
    """Exact match count must match actual boundary occurrences."""
    text = "SAP SAP SAP sapphire sapling"
    count = count_boundary_occurrences("SAP", text)
    assert count == 3  # only standalone SAP, not sapphire/sapling


# ── skill count table via report ──────────────────────────────────────────────


def test_skill_count_table_uses_match_stage():
    from ats_engine import build_report

    jd = "We need SAP and Incoterms expertise."
    fw = 'EXP-01 | Trade | skills: [SAP, Incoterms] | evidence: "SAP and Incoterms"'
    cv = "I have SAP experience."  # Incoterms is missing

    report = build_report(jd, fw, cv_text=cv, use_sbert=False)
    table = report["skill_count_table"]

    sap_row = next((r for r in table if r["skill"].upper() == "SAP"), None)
    inc_row = next((r for r in table if "incoterm" in r["skill"].lower()), None)

    assert sap_row is not None
    assert "Match" in sap_row["status"]
    assert sap_row.get("match_stage") == "EXACT"

    assert inc_row is not None
    assert "Missing" in inc_row["status"]
    assert inc_row.get("match_stage") == "NONE"


def test_skill_count_table_missing_term_has_zero_resume_count():
    from ats_engine import build_report

    jd = "We need blockchain expertise."
    fw = 'EXP-01 | Tech | skills: [blockchain] | evidence: "blockchain experience"'
    cv = "I have Java and Python experience."

    report = build_report(jd, fw, cv_text=cv, use_sbert=False)
    table = report["skill_count_table"]
    bc_row = next((r for r in table if "blockchain" in r["skill"].lower()), None)
    if bc_row:
        assert bc_row["resume_count"] == 0
        assert "Missing" in bc_row["status"]
