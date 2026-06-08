.PHONY: install dev demo test score clean
install:
	cd engine && pip install -e . --break-system-packages
dev:
	cd engine && pip install -e ".[dev]" --break-system-packages
demo:
	cd engine && python examples/run_demo.py
test:
	cd engine && python -m pytest -q
score:
	cd engine && python -m ats_engine.cli report --jd examples/sample_jd_foreign_trade.txt --framework examples/framework_cv.md --cv examples/sample_cv.txt --no-sbert --format md
clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} + ; find . -name '*.pyc' -delete
