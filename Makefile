PACKAGE = app
PYTHON = python3.10
TESTS = tests
WEB_APP = web_app
PYTEST_OPTS =
VENV = venv
VENV_BIN = $(VENV)/bin
VENV_PRE_COMMIT_BIN = $(VENV).pre-commit/bin
VENV_LINT_BIN = $(VENV).lint/bin
VENV_WEB_APP_BIN = venv.web_app/bin

_web_app_requirements_txt := $(WEB_APP)/requirements.txt

venv: requirements.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_BIN)/pip install -r $<


venv.web_app: $(_web_app_requirements_txt)
	rm -rf $@
	virtualenv --python=$(PYTHON) $@
	$(VENV_WEB_APP_BIN)/pip install -U pip
	$(VENV_WEB_APP_BIN)/pip install -r $<


venv.pre-commit:
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_PRE_COMMIT_BIN)/pip install pre-commit

venv.lint: requirements.txt requirements.lint.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_LINT_BIN)/pip install -r requirements.txt
	$(VENV_LINT_BIN)/pip install -r requirements.lint.txt

.PHONY: update-requirements
update-requirements: packages.txt
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install -r $<
	$(VENV_BIN)/pip freeze > requirements.txt


.PHONY: update-requirements-web-app
update-requirements-web-app: $(WEB_APP)/packages.txt
	rm -rf venv.web_app
	virtualenv --python=$(PYTHON) venv.web_app
	$(VENV_WEB_APP_BIN)/pip install -U pip
	$(VENV_WEB_APP_BIN)/pip install -r $<
	$(VENV_WEB_APP_BIN)/pip freeze > $(_web_app_requirements_txt)
	touch venv.web_app


.PHONY: pre-commit-install
pre-commit-install: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit install

.PHONY: pre-commit-autoupdate
pre-commit-autoupdate: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit autoupdate

.PHONY: pre-commit-run-all
pre-commit-run-all: venv.pre-commit
	$(VENV_PRE_COMMIT_BIN)/pre-commit run --all-files

.PHONY: lint-black
lint-black: venv.lint
	$(VENV_LINT_BIN)/black --check --diff $(PACKAGE) $(TESTS) $(WEB_APP)

.PHONY: lint-ruff
lint-ruff: venv.lint
	$(VENV_LINT_BIN)/ruff check $(PACKAGE) $(TESTS) $(WEB_APP)

.PHONY: lint-mypy
lint-mypy: venv.lint
	$(VENV_LINT_BIN)/mypy $(PACKAGE)

.PHONY: lint
lint: lint-black lint-ruff lint-mypy

.PHONY: ruff-fix
ruff-fix: venv.lint
	$(VENV_LINT_BIN)/ruff --fix $(PACKAGE) $(TESTS) $(WEB_APP)

.PHONY: black-fix
black-fix: venv.lint
	$(VENV_LINT_BIN)/black $(PACKAGE) $(TESTS) $(WEB_APP)

.PHONY: test
test: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) $(TESTS)

.PHONY: test-coverage
test-coverage: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) --cov=$(PACKAGE) --cov-report=term $(TESTS)

.PHONY: test-real
test-real: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) -m real $(TESTS)

.PHONY: run
run: venv
	$(PYTHON) manage.py runserver

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f `find . -type f -name '*.egg-info' `
	rm -rf coverage
	rm -rf .coverage
	rm -rf */.pytest_cache
	rm -rf cover
	rm -rf htmlcov
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf venv
	rm -rf venv.pre-commit
	rm -rf venv.lint


.PHONY: help
help:
	@echo "Available targets:"
	@echo
	@echo "venv                   		- Create virtual environment and install project dependencies."
	@echo "venv.pre-commit        		- Create virtual environment and install pre-commit hooks."
	@echo "venv.lint              		- Create virtual environment and install linting dependencies."
	@echo "update-requirements    		- Update project dependencies and requirements.txt."
	@echo "update-requirements-web-app  - Update web app dependencies and requirements.txt."
	@echo "pre-commit-install     		- Install and configure pre-commit hooks."
	@echo "pre-commit-autoupdate  		- Update pre-commit hooks."
	@echo "pre-commit-run-all     		- Run all configured pre-commit hooks."
	@echo "lint-black             		- Lint the code using the Black code formatter."
	@echo "lint-ruff              		- Lint the code using the Ruff linter."
	@echo "lint-mypy              		- Lint the code using the MyPy static type checker."
	@echo "lint                   		- Run all linting targets (lint-black, lint-ruff, lint-mypy)."
	@echo "black-fix              		- Automatically fix issues using the Black linter."
	@echo "ruff-fix               		- Automatically fix issues using the Ruff linter."
	@echo "test                   		- Run tests using pytest."
	@echo "test-coverage          		- Run tests with code coverage analysis using pytest."
	@echo "test-real              		- Run tests marked with the 'real' marker."
	@echo "run                    		- Start the application using Uvicorn with auto-reloading."
	@echo "clean                  		- Remove temporary and generated files and directories."
