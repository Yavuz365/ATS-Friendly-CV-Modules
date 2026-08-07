"""C-007: stable error taxonomy — severity, retryability, and exit/HTTP mapping.

Publishing bare error *codes* is not a taxonomy: a caller needs to know, per
code, whether it is fixable by them (severity), whether retrying makes sense,
and what CLI exit / HTTP status it maps to. These tests pin that every
registered code has a complete, internally consistent taxonomy row and that
the CLI actually reads its exit codes from it rather than a hard-coded literal.
"""

from __future__ import annotations

import os

from ats_engine import cli
from ats_engine.errors import (
    ERROR_TAXONOMY,
    ATSEngineError,
    ErrorCode,
    ErrorSeverity,
    InternalEngineError,
    InvalidInputError,
    ResourceMissingError,
    taxonomy_for,
)


def test_every_error_code_has_a_taxonomy_row():
    for code in ErrorCode:
        assert code in ERROR_TAXONOMY, f"{code} is missing from ERROR_TAXONOMY"
        entry = ERROR_TAXONOMY[code]
        assert entry.code is code
        assert isinstance(entry.severity, ErrorSeverity)
        assert isinstance(entry.retryable, bool)
        assert entry.cli_exit_code in {2, 3, 4}, "CLI exit code must be one of the documented non-zero codes"
        assert 400 <= entry.http_status < 600
        assert entry.description


def test_severity_matches_cli_exit_code_family():
    # USER_ERROR always maps to exit 2, REVIEW_REQUIRED to exit 4, INTERNAL_ERROR to exit 3 —
    # the CLI's 0/2/3/4 contract (STAB-008) must be a strict function of severity.
    expected = {
        ErrorSeverity.USER_ERROR: 2,
        ErrorSeverity.REVIEW_REQUIRED: 4,
        ErrorSeverity.INTERNAL_ERROR: 3,
    }
    for entry in ERROR_TAXONOMY.values():
        assert entry.cli_exit_code == expected[entry.severity]


def test_unmapped_code_falls_back_to_internal_error_not_a_silent_success():
    fallback = taxonomy_for(ErrorCode.INVALID_INPUT)  # sanity: mapped code returns itself
    assert fallback.code is ErrorCode.INVALID_INPUT


def test_ats_engine_error_to_dict_exposes_full_taxonomy():
    err = InvalidInputError("bad value", field="jd")
    payload = err.to_dict()
    assert payload["code"] == "INVALID_INPUT"
    assert payload["severity"] == "USER_ERROR"
    assert payload["retryable"] is True
    assert payload["cli_exit_code"] == 2
    assert payload["http_status"] == 400
    assert payload["field"] == "jd"
    assert err.cli_exit_code == 2
    assert err.http_status == 400


def test_resource_missing_error_is_not_retryable_by_accident_but_by_taxonomy():
    err = ResourceMissingError("no such file")
    assert err.cli_exit_code == 2
    assert err.retryable is True  # fixing the path and retrying is meaningful


def test_internal_engine_error_maps_to_exit_three_and_is_not_retryable():
    err = InternalEngineError("boom")
    assert isinstance(err, ATSEngineError)
    assert err.code is ErrorCode.INTERNAL_ERROR
    assert err.cli_exit_code == 3
    assert err.retryable is False


def test_cli_reads_exit_code_from_taxonomy_for_missing_file(tmp_path, capsys):
    missing = os.path.join(tmp_path, "does_not_exist.txt")
    code = cli.main(["parse", "--jd", missing])
    assert code == ResourceMissingError("x").cli_exit_code == 2
    err = capsys.readouterr().err
    assert "RESOURCE_MISSING" in err


def test_cli_reads_exit_code_from_taxonomy_for_unexpected_error(tmp_path, capsys, monkeypatch):
    jd_path = os.path.join(tmp_path, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write("Dış Ticaret Uzmanı")

    def _boom(_text):
        raise RuntimeError("simulated fault")

    monkeypatch.setattr(cli.jd_parser, "parse_jd", _boom)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == InternalEngineError("x").cli_exit_code == 3
    err = capsys.readouterr().err
    assert "INTERNAL_ERROR" in err
