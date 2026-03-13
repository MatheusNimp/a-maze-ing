.PHONY: install run debug clean lint lint-strict build

VENV := .venv
PY := $(VENV)/bin/python
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

FLAKE8_EXCLUDE := .venv,venv,__pycache__,.mypy_cache,.pytest_cache,dist,build,tests

install: $(VENV)/bin/activate
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e '.[dev]'

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	@test -f $(VENV)/bin/python || (echo "Error: venv python not found"; exit 1)
	@$(VENV)/bin/python -m ensurepip --upgrade >/dev/null 2>&1 || true
	@$(VENV)/bin/python -m pip --version >/dev/null 2>&1 || ( \
		echo "Error: pip is missing inside the venv."; \
		echo "Ubuntu/Debian: sudo apt install -y python3-venv python3-pip"; \
		echo "macOS: brew install python"; \
		exit 1 \
	)

run: $(VENV)/bin/activate
	$(PY) a_maze_ing.py config_default.txt

debug: $(VENV)/bin/activate
	$(PY) -m pdb a_maze_ing.py config_default.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist build $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: $(VENV)/bin/activate
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE)
	$(MYPY) . --exclude '^tests/' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)/bin/activate
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE)
	$(MYPY) . --exclude '^tests/' --strict

build: $(VENV)/bin/activate
	$(PY) -m pip install -U build
	$(PY) -m build