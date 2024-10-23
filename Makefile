NAME := bright_network_challenge


.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  format      reformat code"
	@echo "  lint        run the code linters"
	@echo "  test        run all the tests"
	@echo "  clean       remove *.pyc files and __pycache__ directory"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

# setup:
# 	python3 -m venv .venv
# 	.venv/bin/pip install -r requirements.txt

install:
	poetry run python -m spacy download en_core_web_sm
	poetry install

test:
	poetry run pytest -vv

run:
	poetry run python main.py

