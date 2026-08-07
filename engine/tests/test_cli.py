"""A9 (kalan parça): CLI exit code sözleşmesi testleri.

Öncesinde main() hiçbir hatayı yakalamıyordu; dosya bulunamadı da, beklenmeyen
bir motor hatası da aynı ham traceback + exit code 1 olarak dışarı sızıyordu.
Bu testler Kanonik Blueprint'in (§9.3 P0.2) önerdiği şemayı kilitler:
0=başarı, 2=girdi hatası, 3=beklenmeyen dahili hata, 4=review/blocking.
"""

from __future__ import annotations

import json
import os

from ats_engine import cli

FRAMEWORK = "## Kanıt Bankası\n\n- Dış ticaret operasyonlarını yönetti, incoterms ve akreditif süreçlerini yürüttü.\n"
JD = "Dış ticaret uzmanı aranıyor. Incoterms ve akreditif bilgisi şarttır."
# JD with explicit must-have section so parse returns review_required=False → exit 0
JD_WITH_MUST = "Dış Ticaret Uzmanı\nZorunlu: SAP, Incoterms.\nSorumluluklar: İhracat operasyonlarını yönetin.\n"


def _write(tmp_path, name: str, content: str) -> str:
    path = os.path.join(tmp_path, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_main_returns_zero_on_success(tmp_path, capsys):
    # Use a JD with explicit "Zorunlu:" section so parse_jd returns review_required=False
    jd_path = _write(tmp_path, "jd.txt", JD_WITH_MUST)
    fw_path = _write(tmp_path, "framework.md", FRAMEWORK)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 0
    out = capsys.readouterr().out
    json.loads(out)  # valid JSON çıktısı üretmiş olmalı
    # ikinci bir alt komutla da doğrula (report) — JD ile eşleşen framework kullan
    code2 = cli.main(["report", "--jd", jd_path, "--framework", fw_path, "--format", "json", "--no-sbert"])
    assert code2 == 4  # yapılandırılmış evidence + insan onayı olmadığı için REVIEW


def test_main_returns_two_on_missing_file(tmp_path, capsys):
    missing = os.path.join(tmp_path, "does_not_exist.txt")
    code = cli.main(["parse", "--jd", missing])
    assert code == 2
    err = capsys.readouterr().err
    assert "Girdi hatası" in err
    assert "does_not_exist.txt" in err


def test_main_returns_three_on_unexpected_internal_error(tmp_path, capsys, monkeypatch):
    jd_path = _write(tmp_path, "jd.txt", JD)

    def _boom(_text):
        raise RuntimeError("simüle edilmiş dahili hata")

    monkeypatch.setattr(cli.jd_parser, "parse_jd", _boom)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 3
    err = capsys.readouterr().err
    assert "Beklenmeyen dahili hata" in err
    assert "RuntimeError" in err


def test_diagnose_returns_typed_review_exit_four(tmp_path, capsys):
    jd_path = _write(tmp_path, "jd.txt", "Dış Ticaret Uzmanı\nZorunlu: SAP")
    cv_path = _write(tmp_path, "cv.txt", "SAP deneyimi")
    fw_path = _write(tmp_path, "framework.md", 'EXP-01 | ERP | beceriler: [SAP] | kanıt: "SAP kullandım"')
    code = cli.main(
        [
            "diagnose",
            "--jd",
            jd_path,
            "--cv",
            cv_path,
            "--framework",
            fw_path,
            "--no-sbert",
        ]
    )
    assert code == 4
    payload = json.loads(capsys.readouterr().out)
    assert payload["gates"][0]["gate_id"] == "G0"
    assert payload["overall_status"] == "REVIEW"


# ── STAB-008: additional exit contract tests ──────────────────────────────────


def test_invalid_utf8_returns_exit_two(tmp_path, capsys):
    """Invalid UTF-8 bytes → exit 2 (input error), not exit 3 (internal error)."""
    bad_path = os.path.join(tmp_path, "bad.txt")
    with open(bad_path, "wb") as f:
        f.write(b"valid prefix\xff\xfe invalid bytes")
    code = cli.main(["parse", "--jd", bad_path])
    assert code == 2
    err = capsys.readouterr().err
    assert "Girdi hatası" in err


def test_parse_review_required_returns_exit_four(tmp_path, capsys, monkeypatch):
    """parse result with review_required=True → exit 4."""
    jd_path = _write(tmp_path, "jd.txt", JD)

    def _parse_with_review(_text):
        return {"review_required": True, "some": "data"}

    monkeypatch.setattr(cli.jd_parser, "parse_jd", _parse_with_review)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 4


def test_parse_normal_success_returns_exit_zero(tmp_path, capsys, monkeypatch):
    """parse result without review_required → exit 0."""
    jd_path = _write(tmp_path, "jd.txt", JD)

    def _parse_no_review(_text):
        return {"review_required": False, "some": "data"}

    monkeypatch.setattr(cli.jd_parser, "parse_jd", _parse_no_review)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 0
