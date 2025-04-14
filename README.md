# Sistema de Vendas de Veículos da FIAP

Sistema completo para gerenciamento de veículos, vendas e pagamentos.

## Visão Geral
O sistema é composto por três serviços principais:
1. **Serviço de Veículos**: Gerenciamento de veículos e seus status
2. **Serviço de Vendas**: Gerenciamento de vendas e status de pagamento
3. **Frontend**: Interface web para interação com os serviços

## Arquitetura
```
.
├── frontend/           # Interface web (React + TypeScript)
├── vehicle-service/    # Serviço de veículos (Python + FastAPI)
├── sales-service/      # Serviço de vendas (Python + FastAPI)
└── docker-compose.yml  # Configuração dos containers
```

## Pré-requisitos
- Docker
- Docker Compose
- Make
- Node.js (para desenvolvimento local do frontend)
- Python 3.8+ (para desenvolvimento local dos serviços)

## Execução do Projeto

### 1. Instalação Inicial
```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]

# Configurar ambiente
make setup

# Instalar dependências
make install
```

### 2. Configuração do Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=vehicle_db

# Serviços
VEHICLE_SERVICE_URL=http://localhost:8000
SALES_SERVICE_URL=http://localhost:8001
PAYMENTS_SERVICE_URL=http://localhost:8002

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VEHICLES_SERVICE_URL=http://localhost:8001
REACT_APP_SALES_SERVICE_URL=http://localhost:8002
REACT_APP_PAYMENTS_SERVICE_URL=http://localhost:8003
```

### 3. Execução dos Serviços
```bash
# Configura os ambientes
make setup

# Instala todas as dependências
make install

# Iniciar todos os serviços
make up

# Iniciar apenas o banco de dados das aplicações
make mongodb

# Iniciar apenas o serviço de veículos
make core

# Iniciar apenas o serviço de vendas
make sales

# Verificar status dos serviços
make status

# Verificar logs
make logs

# Verificar logs específicos
make core-logs    # Logs do serviço de veículos
make sales-logs   # Logs do serviço de vendas
make mongodb-logs # Logs do MongoDB

# Parar todos os serviços
make down

# Parar serviços sem remover volumes
make stop

# Reiniciar serviços
make restart
```

### 4. Testes
```bash
# Executar todos os testes
make test

# Executar testes específicos
make test-core    # Testes do serviço de veículos
make test-sales   # Testes do serviço de vendas

# Executar cobertura de testes
make coverage           # Cobertura de todos os serviços
make coverage-core     # Cobertura do serviço de veículos
make coverage-sales    # Cobertura do serviço de vendas
make coverage-report   # Gerar relatório HTML de cobertura
```

### 5. Qualidade de Código
```bash
# Executar linter
make lint

# Verificar tipos
make type-check
```

### 6. Manutenção
```bash
# Limpar ambiente (remove volumes)
make clean

# Limpar banco de dados específico
make clean-core-db    # Limpar banco do serviço de veículos
make clean-sales-db   # Limpar banco do serviço de vendas

# Reconstruir containers
make rebuild
```

## Acessando os Serviços

### Serviço de Veículos
- Porta: 8000
- Documentação: http://localhost:8000/docs
- Status dos veículos:
  - DISPONÍVEL: Veículo disponível para venda
  - RESERVADO: Veículo reservado para uma venda
  - VENDIDO: Veículo vendido

### Serviço de Vendas
- Porta: 8001
- Documentação: http://localhost:8001/docs
- Status de pagamento:
  - PENDING: Pagamento pendente
  - PAID: Pagamento confirmado
  - CANCELLED: Venda cancelada

### Frontend
- Porta: 3000
- URL: http://localhost:3000

## Fluxo de Venda
1. Selecione um veículo disponível
2. Preencha os dados do comprador e pagamento
3. Ao criar a venda:
   - O veículo é automaticamente marcado como RESERVADO
   - A venda é criada com status PENDENTE
4. Após confirmação do pagamento:
   - O veículo é marcado como VENDIDO
   - A venda é atualizada para status PAGO
5. Se a venda for cancelada:
   - O veículo volta para DISPONÍVEL
   - A venda é atualizada para status CANCELADA

## Contribuição
1. Crie uma branch para sua feature:
```bash
git checkout -b feature/nova-feature
```

2. Faça commit das suas alterações:
```bash
git commit -m "feat: adiciona nova feature"
```

3. Envie para o repositório:
```bash
git push origin feature/nova-feature
```

4. Crie um Pull Request

## Licença
Este projeto está licenciado sob a licença MIT.

## Documentação da API

O sistema possui três serviços principais, cada um com sua própria documentação OpenAPI:

### Core Service (Veículos)
- **URL Base**: http://localhost:8000
- **Documentação**: `/app/adapters/api/openapi.json`
- **Endpoints Principais**:
  - CRUD de veículos
  - Gerenciamento de status (disponível, reservado, vendido)
  - Listagem por status

### Sales Service (Vendas)
- **URL Base**: http://localhost:8001
- **Documentação**: `/app/adapters/api/openapi.json`
- **Endpoints Principais**:
  - CRUD de vendas
  - Gerenciamento de status de pagamento
  - Busca por veículo ou código de pagamento
  - Listagem por status

### Payment Service (Pagamentos)
- **URL Base**: http://localhost:8002
- **Documentação**: `/app/adapters/api/openapi.json`
- **Endpoints Principais**:
  - CRUD de pagamentos
  - Gerenciamento de status
  - Busca por código de pagamento
  - Listagem por status

Para visualizar a documentação interativa, você pode usar ferramentas como:
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc) 

