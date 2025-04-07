.PHONY: install up down test test-core test-sales logs clean run

# Inicializa todos os serviços
install:
	docker-compose build

# Inicia os serviços em modo desenvolvimento
up:
	docker-compose up --build

# Para todos os serviços
down:
	docker-compose down

# Executa todos os testes
test: test-core test-sales

# Executa testes do core-service
test-core:
	docker-compose run --rm --remove-orphans dev-core pytest -v

# Executa testes do sales-service
test-sales:
	docker-compose run --rm --remove-orphans dev-sales pytest -v

# Mostra logs dos serviços
logs:
	docker-compose logs -f

# Limpa containers e volumes
clean:
	docker-compose down -v
	docker system prune -f
	docker-compose run --rm dev-core sh -c "find . -type d -name '__pycache__' -exec rm -rf {} +"
	docker-compose run --rm dev-core sh -c "find . -type f -name '*.pyc' -delete"
	docker-compose run --rm dev-core sh -c "find . -type f -name '*.pyo' -delete"
	docker-compose run --rm dev-core sh -c "find . -type f -name '*.pyd' -delete"
	docker-compose run --rm dev-core sh -c "find . -type f -name '.coverage' -delete"
	docker-compose run --rm dev-core sh -c "find . -type f -name 'coverage.xml' -delete"
	docker-compose run --rm dev-core sh -c "find . -type d -name '.pytest_cache' -exec rm -rf {} +"
	docker-compose run --rm dev-core sh -c "find . -type d -name '.coverage' -exec rm -rf {} +"
	docker-compose run --rm dev-core sh -c "find . -type d -name 'htmlcov' -exec rm -rf {} +"

# Inicia os serviços em modo produção
run:
	docker-compose up --build -d
	docker-compose logs -f 