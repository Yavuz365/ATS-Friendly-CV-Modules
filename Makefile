.PHONY: install dev demo test score lint typecheck format format-check check package-check clean

install:
	cd engine && pip install -e . --break-system-packages
dev:
	cd engine && pip install -e ".[dev]" --break-system-packages
demo:
	cd engine && python examples/run_demo.py
test:
	cd engine && python -m pytest tests/ -v
score:
	cd engine && python -m ats_engine.cli report --jd examples/sample_jd_foreign_trade.txt --framework examples/framework_cv.md --cv examples/sample_cv.txt --no-sbert --format md
lint:
	cd engine && python -m ruff check ats_engine/ tests/
# A10 fix: mypy [tool.mypy] altında yapılandırılmıştı ama hiçbir make hedefi
# çalıştırmıyordu (CI de öyle) — artık `make check`'in bir parçası.
typecheck:
	cd engine && python -m mypy --cache-dir=.mypy_cache_v2 ats_engine
format:
	cd engine && python -m ruff format ats_engine/ tests/
format-check:
	cd engine && python -m ruff format --check ats_engine/ tests/
DIST_DIR ?= dist/2.0.0a2
package-check:
	python -m build engine --sdist --wheel --outdir $(DIST_DIR)
	python scripts/verify_wheel.py $(DIST_DIR)/*.whl
check: lint format-check typecheck test
clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} + ; find . -name '*.pyc' -delete
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
	find . -type d -name '*.egg-info' -prune -exec rm -rf {} +
