.PHONY: install setup up down test test-core test-sales logs clean run stop mongodb mongodb-logs core sales core-logs sales-logs lint type-check rebuild status restart build-sales run-sales test-sales build-core run-core test-core build-all run-all test-all

# Instalação e Configuração
install:
	@echo "Instalando dependências..."
	pip install -r requirements.txt

setup:
	@echo "Configurando ambiente..."
	docker-compose build

# Comandos básicos
up:
	docker-compose up -d

down:
	docker-compose down

test: test-core test-sales
	@echo "Running all tests..."

test-core:
	docker-compose run --rm core-service pytest tests/ -v

test-sales:
	docker-compose run --rm sales-service pytest tests/ -v

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

# Comandos específicos para cada serviço
run:
	docker-compose up

stop:
	docker-compose down

mongodb:
	docker-compose up -d core-mongodb sales-mongodb

mongodb-logs:
	docker-compose logs -f core-mongodb sales-mongodb

core:
	docker-compose up -d core-service

sales:
	docker-compose up -d sales-service

core-logs:
	docker-compose logs -f core-service

sales-logs:
	docker-compose logs -f sales-service

# Comandos de desenvolvimento
lint:
	docker-compose run --rm core-service flake8 .
	docker-compose run --rm sales-service flake8 .

type-check:
	docker-compose run --rm core-service mypy .
	docker-compose run --rm sales-service mypy .

rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

status:
	@echo "Checking services status..."
	docker-compose ps

restart:
	docker-compose restart

# Comandos para o serviço de vendas
build-sales:
	docker-compose build sales-service

run-sales:
	docker-compose up sales-service

# Comandos para o serviço core
build-core:
	docker-compose build core-service

run-core:
	docker-compose up core-service

# Comandos para ambos os serviços
build-all: build-core build-sales

run-all: run-core run-sales

test-all: test-core test-sales 