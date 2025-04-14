# Sistema de Vendas de Veículos da FIAP

## Visão Geral
Serviço responsável pelo gerenciamento de veículos, incluindo cadastro, atualização e controle de status.

## Status dos Veículos
- DISPONÍVEL: Veículo disponível para venda
- RESERVADO: Veículo reservado para uma venda em andamento
- VENDIDO: Veículo vendido (status automático após confirmação de pagamento)

## Fluxo de Status
1. Veículo é cadastrado com status DISPONÍVEL
2. Ao ser selecionado para venda, status muda para RESERVADO
3. Após confirmação de pagamento, status muda automaticamente para VENDIDO
4. Em caso de cancelamento, status volta para DISPONÍVEL

## Endpoints
- GET /vehicles - Lista todos os veículos
- GET /vehicles/{id} - Obtém um veículo específico
- POST /vehicles - Cria um novo veículo
- PUT /vehicles/{id} - Atualiza um veículo
- PATCH /vehicles/{id}/status - Atualiza o status de um veículo
- DELETE /vehicles/{id} - Remove um veículo

## Requisitos
- Python 3.8+
- FastAPI
- MongoDB
- Pydantic
- Motor

## Instalação
1. Instale as dependências: `pip install -r requirements.txt`
2. Configure as variáveis de ambiente no arquivo `.env`
3. Execute o serviço: `uvicorn app.main:app --reload`

## Comandos de Execução

### Desenvolvimento
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor de desenvolvimento
uvicorn app.main:app --reload

# Iniciar com configurações específicas
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Construir a imagem
docker build -t vehicle-service .

# Executar o container
docker run -p 8000:8000 vehicle-service

# Executar com variáveis de ambiente
docker run -p 8000:8000 \
  -e MONGODB_URL=mongodb://localhost:27017 \
  -e MONGODB_DB=vehicle_db \
  vehicle-service
```

### Docker Compose
```bash
# Iniciar o serviço com os outros serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f

# Parar os serviços
docker-compose down
```

### Testes
```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/

# Executar testes específicos
pytest tests/test_vehicles.py

# Executar testes com relatório HTML
pytest --cov=app --cov-report=html tests/
```

### Qualidade de Código
```bash
# Executar linter
flake8 app tests

# Verificar tipos
mypy app tests

# Formatar código
black app tests

# Verificar imports
isort app tests
```

## Estrutura do Projeto
```
app/
  ├── main.py        # Configuração do FastAPI
  ├── models/        # Modelos do MongoDB
  ├── schemas/       # Schemas Pydantic
  ├── services/      # Lógica de negócio
  ├── controllers/   # Controladores da API
  └── utils/         # Funções utilitárias
``` 