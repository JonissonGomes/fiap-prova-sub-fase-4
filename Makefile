.PHONY: setup install up down test test-core test-sales logs clean run stop mongodb mongodb-logs core sales core-logs sales-logs lint type-check rebuild status restart clean-sales-db clean-core-db

setup:
	@echo "Configurando ambiente..."
	docker-compose build

install:
	@echo "Instalando dependências..."
	docker-compose run --rm core-service pip install -r requirements.txt
	docker-compose run --rm sales-service pip install -r requirements.txt

up:
	docker-compose up -d
	docker-compose logs -f

down:
	docker-compose down

test:
	@echo "Executando testes..."
	docker-compose run --rm core-service pytest tests/ -v
	docker-compose run --rm sales-service pytest tests/ -v

test-core:
	@echo "Executando testes do core-service..."
	docker-compose run --rm core-service pytest tests/ -v

test-sales:
	@echo "Executando testes do sales-service..."
	docker-compose run --rm sales-service pytest tests/ -v

logs:
	docker-compose logs -f

clean:
	@echo "Limpando ambiente..."
	docker-compose down -v
	docker system prune -f

run:
	docker-compose up

stop:
	docker-compose stop

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

lint:
	@echo "Executando linter..."
	docker-compose run --rm core-service flake8 app/
	docker-compose run --rm sales-service flake8 app/

type-check:
	@echo "Verificando tipos..."
	docker-compose run --rm core-service mypy app/
	docker-compose run --rm sales-service mypy app/

rebuild:
	@echo "Reconstruindo containers..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

status:
	@echo "Status dos serviços:"
	docker-compose ps

restart:
	@echo "Reiniciando serviços..."
	docker-compose restart
	docker-compose logs -f

clean-sales-db:
	@echo "Limpando banco de dados do sales-service..."
	docker-compose exec sales-mongodb mongosh sales_db --eval "db.sales.deleteMany({})"
	@echo "Banco de dados limpo com sucesso!"

clean-core-db:
	@echo "Limpando banco de dados do core-service..."
	docker-compose exec core-mongodb mongosh core_db --eval "db.vehicles.deleteMany({})"
	@echo "Banco de dados limpo com sucesso!" 