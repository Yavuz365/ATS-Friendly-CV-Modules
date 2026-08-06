# Legacy baseline — `3b6cce1e4c2919146752590f7bece4ae2812a8f5`

This directory defines the immutable evidence package required by F0-001. The historical commit is never edited or rebuilt from current source.

## Required artifact package

Run from a full repository clone:

```bash
python scripts/freeze_legacy_baseline.py \
  --commit 3b6cce1e4c2919146752590f7bece4ae2812a8f5 \
  --output dist/baseline/legacy-3b6cce1
```

The package must contain:

- `SOURCE_COMMIT.txt`
- `source-3b6cce1e4c2919146752590f7bece4ae2812a8f5.tar.gz`
- `reproduction-report.json`
- `SHA256SUMS.txt`
- `artifacts/*.whl` and `artifacts/*.tar.gz` only when the exact historical tree builds successfully

## Acceptance rule

`REPRODUCIBLE` means the exact archived tree produced both wheel and sdist without source edits. `NON_REPRODUCIBLE` is also a valid historical finding, but it must preserve build stdout/stderr and must not be rewritten as a successful release.

The generated binary package belongs in the GitHub release/CI artifact store rather than in normal Git history. `SHA256SUMS.txt` is the byte-level chain of custody.
