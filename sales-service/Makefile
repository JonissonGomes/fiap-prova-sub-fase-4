.PHONY: install test lint run clean docker-test docker-lint docker-run

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest

lint:
	flake8 app/ tests/

run:
	PYTHONPATH=. uvicorn app.adapters.api.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

docker-test:
	docker-compose run --rm dev-sales

docker-lint:
	docker-compose run --rm dev-sales flake8 app/ tests/

docker-run:
	docker-compose up sales-service 