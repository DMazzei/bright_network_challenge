NAME := bright_network_challenge


.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  lint        run the code linters"
	@echo "  test        run all the tests"
	@echo "  linters     run pre-commit linters"
	@echo "  run         run the algorithm"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

.PHONY: install
install:
	poetry run python -m spacy download en_core_web_sm
	poetry install

.PHONY: test
test:
	poetry run pytest -vv

.PHONY: linters
linters:
	poetry run pre-commit run --all-files

.PHONY: run
run:
	poetry run python main.py
