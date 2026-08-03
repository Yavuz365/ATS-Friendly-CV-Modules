"""A9 (kalan parça): CLI exit code sözleşmesi testleri.

Öncesinde main() hiçbir hatayı yakalamıyordu; dosya bulunamadı da, beklenmeyen
bir motor hatası da aynı ham traceback + exit code 1 olarak dışarı sızıyordu.
Bu testler üç durumu da kilitler: 0=başarı, 2=girdi hatası, 1=beklenmeyen hata.
"""
from __future__ import annotations

import json
import os

from ats_engine import cli

FRAMEWORK = (
    "## Kanıt Bankası\n\n"
    "- Dış ticaret operasyonlarını yönetti, incoterms ve akreditif süreçlerini yürüttü.\n"
)
JD = "Dış ticaret uzmanı aranıyor. Incoterms ve akreditif bilgisi şarttır."


def _write(tmp_path, name: str, content: str) -> str:
    path = os.path.join(tmp_path, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_main_returns_zero_on_success(tmp_path, capsys):
    jd_path = _write(tmp_path, "jd.txt", JD)
    fw_path = _write(tmp_path, "framework.md", FRAMEWORK)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 0
    out = capsys.readouterr().out
    json.loads(out)  # valid JSON çıktısı üretmiş olmalı
    # ikinci bir alt komutla da doğrula (report)
    code2 = cli.main(["report", "--jd", jd_path, "--framework", fw_path, "--format", "json", "--no-sbert"])
    assert code2 == 0


def test_main_returns_two_on_missing_file(tmp_path, capsys):
    missing = os.path.join(tmp_path, "does_not_exist.txt")
    code = cli.main(["parse", "--jd", missing])
    assert code == 2
    err = capsys.readouterr().err
    assert "Girdi hatası" in err
    assert "does_not_exist.txt" in err


def test_main_returns_one_on_unexpected_internal_error(tmp_path, capsys, monkeypatch):
    jd_path = _write(tmp_path, "jd.txt", JD)

    def _boom(_text):
        raise RuntimeError("simüle edilmiş dahili hata")

    monkeypatch.setattr(cli.jd_parser, "parse_jd", _boom)
    code = cli.main(["parse", "--jd", jd_path])
    assert code == 1
    err = capsys.readouterr().err
    assert "Beklenmeyen dahili hata" in err
    assert "RuntimeError" in err
