PYTHON=uv run python
TEST=uv run pytest
LINT=uv run ruff check src tests
FORMAT=uv run ruff check --fix src tests

.PHONY: run test lint format docker-build docker-run

run:
	$(PYTHON) -m src.main

test:
	$(TEST)

lint:
	$(LINT)

format:
	$(FORMAT)

docker-build:
	docker build -t cineville-csv-processor .

docker-run:
	docker run --rm -v "$(PWD)/data:/app/data" -v "$(PWD)/output:/app/output" cineville-csv-processor
