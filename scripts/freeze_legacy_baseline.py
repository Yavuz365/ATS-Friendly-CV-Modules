#!/usr/bin/env python3
"""Freeze a historical repository baseline without modifying its source.

The command creates a git archive, attempts an isolated wheel/sdist build from the
exact archived tree, records environment/tool output and writes SHA256SUMS. A build
failure is preserved as NON_REPRODUCIBLE instead of repairing historical code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def _run(command: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_checksums(output: Path) -> None:
    candidates = sorted(
        path for path in output.rglob("*") if path.is_file() and path.name != "SHA256SUMS.txt"
    )
    lines = [f"{_sha256(path)}  {path.relative_to(output).as_posix()}" for path in candidates]
    (output / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _verify_commit(repo: Path, commit: str) -> str:
    resolved = _run(["git", "rev-parse", f"{commit}^{{commit}}"], cwd=repo).stdout.strip()
    if resolved != commit:
        raise SystemExit(f"Commit mismatch: requested {commit}, resolved {resolved}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--commit", default="3b6cce1e4c2919146752590f7bece4ae2812a8f5")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    resolved = _verify_commit(repo, args.commit)

    source_archive = output / f"source-{resolved}.tar.gz"
    archive_bytes = _run(["git", "archive", "--format=tar", resolved], cwd=repo).stdout
    # text mode cannot safely preserve tar bytes; use a direct binary subprocess for archive output.
    with source_archive.open("wb") as handle:
        subprocess.run(
            ["git", "archive", "--format=tar", resolved],
            cwd=repo,
            stdout=handle,
            check=True,
        )
    with tempfile.TemporaryDirectory(prefix="ats-baseline-") as temp_dir:
        temp = Path(temp_dir)
        with tarfile.open(source_archive, "r:") as archive:
            archive.extractall(temp, filter="data")

        build_root = temp / "engine"
        artifact_dir = output / "artifacts"
        artifact_dir.mkdir(exist_ok=True)
        command = [sys.executable, "-m", "build", "--sdist", "--wheel", "--outdir", str(artifact_dir)]
        build = _run(command, cwd=build_root, check=False)

    status = "REPRODUCIBLE" if build.returncode == 0 and any(artifact_dir.iterdir()) else "NON_REPRODUCIBLE"
    report = {
        "schema_version": "1.0.0",
        "repository": "Yavuz365/ATS-Friendly-CV-Modules",
        "commit": resolved,
        "status": status,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_archive": source_archive.name,
        "build_command": command,
        "build_exit_code": build.returncode,
        "build_stdout": build.stdout,
        "build_stderr": build.stderr,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "git": _run(["git", "--version"]).stdout.strip(),
            "source_date_epoch": os.environ.get("SOURCE_DATE_EPOCH"),
        },
        "policy": "Historical source was not modified. Build failure remains NON_REPRODUCIBLE.",
    }
    (output / "reproduction-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "SOURCE_COMMIT.txt").write_text(resolved + "\n", encoding="utf-8")
    _write_checksums(output)
    print(json.dumps({"status": status, "output": str(output)}, ensure_ascii=False))
    return 0 if status == "REPRODUCIBLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
