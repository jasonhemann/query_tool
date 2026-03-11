.PHONY: sync format lint lint-fix typecheck test coverage check build clean

UV ?= uv
PYTHON_VERSION ?= 3.13

sync:
	$(UV) sync --python $(PYTHON_VERSION) --group dev

format:
	$(UV) run --python $(PYTHON_VERSION) ruff format src tests

lint:
	$(UV) run --python $(PYTHON_VERSION) ruff check src tests

lint-fix:
	$(UV) run --python $(PYTHON_VERSION) ruff check src tests --fix

typecheck:
	$(UV) run --python $(PYTHON_VERSION) basedpyright

test:
	$(UV) run --python $(PYTHON_VERSION) pytest -q

coverage:
	@echo "Coverage target (warn-only in wave 1): 80%"
	-$(UV) run --python $(PYTHON_VERSION) pytest --cov=src/query_tool --cov-report=term-missing -q

check: lint typecheck test

build:
	$(UV) run --python $(PYTHON_VERSION) pyinstaller --onefile --name query_tool src/query_tool/__main__.py

clean:
	rm -rf .venv __pycache__ */__pycache__ .pytest_cache .ruff_cache dist build *.egg-info *.spec
