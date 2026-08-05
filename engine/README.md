# ats_engine — 2.0.0-alpha.1

Evidence-first CV analysis contract alpha. It is not a commercial ATS pass or hiring-outcome
predictor.

```bash
pip install -e .
pip install -e ".[dev]"

ats-engine ingest --document cv.docx
ats-engine parse --jd job.txt
ats-engine report --jd job.txt --framework framework.md --cv cv.txt --format json --no-sbert
ats-engine score --jd job.txt --cv cv.txt --must "SAP,Incoterms" --no-sbert
```

Exit codes: `0=success`, `2=invalid input`, `3=internal error`, `4=blocking/review`.

Public Python contracts live in `ats_engine/contracts.py`; language-neutral closed Draft
2020-12 schemas and golden payloads live in repository `schemas/v2/`. Binary ingestion is in
`ingestion.py`, G0–G4 orchestration in `decision.py`, and evidence-bound changes in
`safe_synthesis.py`.

```bash
pytest -q tests
ruff check ats_engine tests
ruff format --check ats_engine tests
mypy ats_engine
```

See repository `docs/limitations.md` before interpreting any diagnostic.
