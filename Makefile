.PHONY: help install test clean run

URL ?= https://www.facebook.com/facebook

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  test         Run tests"
	@echo "  clean        Clean temporary files"
	@echo "  run          Run the scraper"

install:
	python3 -m venv .venv
	pip install -r requirements/dev.txt

test:
	pytest tests/ -v --cov=src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

run:
	python3 -m src.main --method selenium --url $(URL)