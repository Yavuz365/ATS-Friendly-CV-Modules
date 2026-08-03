#!/usr/bin/env python3
"""
ats_engine.cli — birleşik komut satırı arayüzü.

Alt komutlar:
  report  : JD + Framework CV (+ ops. mevcut CV) → 6 alanlık tam rapor (JSON/MD)
  score   : JD + CV → yalnızca hibrit ATS Match Score
  parse   : JD → 7 katmanlı ayrıştırma (JSON)
  bank    : Framework CV → ayrıştırılmış kanıt bankası (JSON)

Örnekler:
  python -m ats_engine.cli report --jd jd.txt --framework framework_cv.md --format md
  python -m ats_engine.cli score  --jd jd.txt --cv cv.txt --must "akreditif,incoterms,gtip" --parse-gate 0.6
  python -m ats_engine.cli parse  --jd jd.txt
  python -m ats_engine.cli bank   --framework framework_cv.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import evidence_bank, jd_parser, report, scoring

# A9 (kalan parça): CLI eskiden hiçbir hatayı yakalamıyordu -- dosya bulunamadı,
# bozuk girdi ya da beklenmeyen bir iç hata, hepsi aynı ham Python traceback +
# exit code 1 olarak dışarı sızıyordu. Artık iki sınıf ayrılıyor:
#   exit 0 -> başarı
#   exit 2 -> kullanıcı/girdi hatası (düzeltilebilir: yanlış yol, okunamayan dosya)
#             argparse'ın kendi kural-dışı-argüman exit code'uyla (2) tutarlı
#   exit 1 -> beklenmeyen dahili hata (motor/programlama hatası)


class CLIInputError(Exception):
    """Kullanıcının düzeltebileceği girdi hatası (örn. dosya bulunamadı)."""


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise CLIInputError(f"Dosya okunamadı: {path!r} ({e.strerror or e})") from e


def _load_corpus(path: str | None):
    if path and os.path.isdir(path):
        return [_read(os.path.join(path, f)) for f in os.listdir(path) if f.endswith(".txt")]
    return None


def cmd_report(args):
    corpus = _load_corpus(args.corpus)
    cv = _read(args.cv) if args.cv else None
    rep = report.build_report(
        _read(args.jd), _read(args.framework), cv_text=cv,
        parse_gate=args.parse_gate, corpus_texts=corpus,
        use_sbert=not args.no_sbert, target_low=args.target,
    )
    print(report.to_markdown(rep) if args.format == "md" else report.to_json(rep))


def cmd_score(args):
    corpus = _load_corpus(args.corpus)
    must = [m.strip() for m in args.must.split(",") if m.strip()]
    # score komutu için parse_gate=None → 1.0 (basit skor, auto-parse yok)
    pg = args.parse_gate if args.parse_gate is not None else 1.0
    res = scoring.ats_match_score(
        _read(args.jd), _read(args.cv), must,
        corpus_texts=corpus, parse_gate=pg, use_sbert=not args.no_sbert,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))


def cmd_parse(args):
    res = jd_parser.parse_jd(_read(args.jd))
    print(json.dumps(res, ensure_ascii=False, indent=2))


def cmd_bank(args):
    bank = evidence_bank.parse_bank(_read(args.framework))
    from dataclasses import asdict
    print(json.dumps([asdict(e) for e in bank], ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ats_engine", description="ATS-Friendly-CV-Modules Engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("report", help="6 alanlık tam rapor")
    r.add_argument("--jd", required=True)
    r.add_argument("--framework", required=True, help="etiketli Framework CV / kanıt bankası")
    r.add_argument("--cv", default=None, help="opsiyonel mevcut CV (teşhis modu)")
    r.add_argument("--corpus", default=None)
    r.add_argument("--parse-gate", type=float, default=None,
                   help="ParseGate skoru (0-1). Verilmezse otomatik hesaplanır.")
    r.add_argument("--target", type=float, default=75.0)
    r.add_argument("--no-sbert", action="store_true")
    r.add_argument("--format", choices=["json", "md"], default="md")
    r.set_defaults(func=cmd_report)

    s = sub.add_parser("score", help="yalnızca hibrit skor")
    s.add_argument("--jd", required=True)
    s.add_argument("--cv", required=True)
    s.add_argument("--must", default="")
    s.add_argument("--corpus", default=None)
    s.add_argument("--parse-gate", type=float, default=None,
                   help="ParseGate skoru (0-1). Verilmezse 1.0 kullanılır.")
    s.add_argument("--no-sbert", action="store_true")
    s.set_defaults(func=cmd_score)

    pa = sub.add_parser("parse", help="7 katmanlı JD ayrıştırma")
    pa.add_argument("--jd", required=True)
    pa.set_defaults(func=cmd_parse)

    b = sub.add_parser("bank", help="Framework CV → kanıt bankası")
    b.add_argument("--framework", required=True)
    b.set_defaults(func=cmd_bank)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except CLIInputError as e:
        print(f"Girdi hatası: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # kasıtlı geniş yakalama: CLI'nin son hata sınırı,
        # motor katmanındaki (report.py/scoring.py) typed error sözleşmesinin
        # dışına sızan HERHANGİ bir beklenmeyen hatayı burada durdurup kullanıcıya
        # ham traceback yerine tek satır + net exit code döndürüyoruz.
        print(f"Beklenmeyen dahili hata: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
