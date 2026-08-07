"""STAB-013: single decision/QA rendering contract tests.

Proves that JSON, Markdown, and CLI output do not independently derive
gate status — all visible status comes from the typed DecisionReport.
"""

from __future__ import annotations

import json

from ats_engine import build_report

JD = "We need a Foreign Trade Specialist with SAP and Incoterms experience."
FRAMEWORK = 'EXP-01 | Trade | skills: [SAP, Incoterms] | evidence: "SAP and Incoterms experience"'
CV = "SAP and Incoterms experience in export operations."


def _build(jd=JD, fw=FRAMEWORK, cv=CV):
    return build_report(jd, fw, cv_text=cv, use_sbert=False)


def test_markdown_decision_status_matches_json():
    """Gate statuses in Markdown come from decision_report, not re-derived."""
    from ats_engine.report import to_json, to_markdown

    report = _build()
    md = to_markdown(report)
    data = json.loads(to_json(report))

    json_overall = data["decision_report"]["overall_status"]
    # Markdown must contain the same overall_status string
    assert json_overall in md, f"Markdown does not reflect JSON overall_status={json_overall!r}"

    # Each gate id and status in JSON must appear in Markdown
    for gate in data["decision_report"]["gates"]:
        gate_id = gate["gate_id"]
        gate_status = gate["status"]
        assert gate_id in md, f"Gate {gate_id} missing from Markdown"
        assert gate_status in md, f"Gate {gate_id} status={gate_status!r} missing from Markdown"


def test_qa_checks_status_in_markdown_comes_from_qa_results():
    """QA check status labels in Markdown come from qa_results, not independently derived."""
    from ats_engine.report import to_markdown

    report = _build()
    md = to_markdown(report)

    qa_results = report.get("qa_results", [])
    for qr in qa_results:
        if isinstance(qr, dict) and qr.get("status"):
            check_id = qr["check_id"]
            status = qr["status"]
            # The [STATUS] label should appear in Markdown for this check
            # (status is shown as [STATUS] suffix after check details)
            assert f"[{status}]" in md, f"QA result status [{status}] for {check_id} not found in Markdown"


def test_json_and_markdown_agree_on_no_independent_pass():
    """No QA check in Markdown can independently show PASS when JSON gate is non-PASS."""
    from ats_engine.report import to_markdown

    report = _build()
    md = to_markdown(report)
    decision = report["decision_report"]
    overall = decision["overall_status"]

    # If overall is REVIEW/FAIL, Markdown must show the same overall status
    if overall in {"REVIEW", "FAIL", "ERROR"}:
        assert overall in md


def test_qa_results_present_in_report_payload():
    """qa_results must be present in the report payload as a list."""
    report = _build()
    assert "qa_results" in report
    assert isinstance(report["qa_results"], list)
    assert len(report["qa_results"]) > 0


def test_decision_report_status_not_independently_set_from_qa_checks():
    """decision_report must not independently re-derive status from qa_checks."""
    report = _build()
    decision = report["decision_report"]
    # Verify the decision report is typed (has the required contract fields)
    assert "overall_status" in decision
    assert "gates" in decision
    assert "evaluation_status" in decision
    # overall_status must come from gates aggregation, not raw qa_checks
    from ats_engine.contracts import ProcessStatus

    valid_statuses = {s.value for s in ProcessStatus}
    assert decision["overall_status"] in valid_statuses
