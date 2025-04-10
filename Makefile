.PHONY: install setup up down test test-core test-sales logs clean run stop mongodb mongodb-logs core sales core-logs sales-logs lint type-check rebuild status restart

# Instalação e Configuração
install:
	@echo "Building Docker images..."
	docker-compose build

setup:
	@echo "Setting up environment..."
	cp .env.example .env
	@echo "Environment setup complete. Please edit .env with your configuration."
	@echo "Now run 'make install' to build the Docker images"

# Desenvolvimento
up:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Showing logs..."
	docker-compose logs -f

down:
	@echo "Stopping development environment..."
	docker-compose down

restart:
	@echo "Restarting development environment..."
	@echo "Stopping services..."
	docker-compose down
	@echo "Starting services..."
	docker-compose up -d
	@echo "Showing logs..."
	docker-compose logs -f

# Testes
test:
	@echo "Running all tests..."
	docker-compose run --rm dev-core pytest -v
	docker-compose run --rm dev-sales pytest -v

test-core:
	@echo "Running core-service tests..."
	docker-compose run --rm dev-core pytest -v

test-sales:
	@echo "Running sales-service tests..."
	docker-compose run --rm dev-sales pytest -v

# Logs
logs:
	@echo "Showing logs..."
	docker-compose logs -f

# Limpeza
clean:
	@echo "Cleaning environment..."
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

# Produção
run:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d

stop:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.prod.yml down

# Banco de Dados
mongodb:
	@echo "Starting MongoDB..."
	docker-compose up -d mongodb

mongodb-logs:
	@echo "Showing MongoDB logs..."
	docker-compose logs -f mongodb

# Serviços Individuais
core:
	@echo "Starting core-service..."
	docker-compose up -d core-service

sales:
	@echo "Starting sales-service..."
	docker-compose up -d sales-service

core-logs:
	@echo "Showing core-service logs..."
	docker-compose logs -f core-service

sales-logs:
	@echo "Showing sales-service logs..."
	docker-compose logs -f sales-service

# Qualidade de Código
lint:
	@echo "Running linters..."
	docker-compose run --rm dev-core black core-service/
	docker-compose run --rm dev-core flake8 core-service/
	docker-compose run --rm dev-sales black sales-service/
	docker-compose run --rm dev-sales flake8 sales-service/

type-check:
	@echo "Running type checking..."
	docker-compose run --rm dev-core mypy core-service/
	docker-compose run --rm dev-sales mypy sales-service/

# Manutenção
rebuild:
	@echo "Rebuilding containers..."
	docker-compose build --no-cache

status:
	@echo "Checking services status..."
	docker-compose ps 