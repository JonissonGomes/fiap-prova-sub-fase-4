# Vehicle Management System

## Visão Geral
Este projeto implementa um sistema de gerenciamento de veículos com dois serviços principais:
- Core Service: Gerencia o cadastro e status dos veículos
- Sales Service: Gerencia as vendas e reservas de veículos

## Estrutura do Projeto
```
.
├── core-service/                 # Serviço principal de gerenciamento de veículos
│   ├── app/
│   │   ├── adapters/            # Adaptadores para interfaces externas
│   │   │   ├── api/             # Endpoints da API
│   │   │   └── repository/      # Repositórios de dados
│   │   ├── domain/              # Regras de negócio e modelos
│   │   └── main.py              # Ponto de entrada do serviço
│   ├── tests/                   # Testes do core-service
│   └── requirements.txt         # Dependências do core-service
│
├── sales-service/               # Serviço de gerenciamento de vendas
│   ├── app/
│   │   ├── adapters/            # Adaptadores para interfaces externas
│   │   │   ├── api/             # Endpoints da API
│   │   │   └── repository/      # Repositórios de dados
│   │   ├── domain/              # Regras de negócio e modelos
│   │   └── main.py              # Ponto de entrada do serviço
│   ├── tests/                   # Testes do sales-service
│   └── requirements.txt         # Dependências do sales-service
│
├── docker-compose.yml           # Configuração dos containers
├── Makefile                     # Comandos de desenvolvimento
└── README.md                    # Documentação do projeto
```

## Arquitetura
O sistema segue uma arquitetura de microsserviços com os seguintes componentes:

### Core Service
- Gerencia o cadastro e status dos veículos
- Implementa regras de negócio relacionadas a veículos
- Expõe API REST para gerenciamento de veículos
- Persiste dados no MongoDB

### Sales Service
- Gerencia o processo de vendas
- Implementa regras de negócio relacionadas a vendas
- Expõe API REST para gerenciamento de vendas
- Persiste dados no MongoDB
- Comunica-se com o Core Service via HTTP

### Banco de Dados
- MongoDB para persistência de dados
- Coleções separadas para veículos e vendas
- Índices para otimização de consultas

### Comunicação entre Serviços
- HTTP/REST para comunicação síncrona
- Webhooks para eventos assíncronos
- Circuit breaker para resiliência

## Repositórios

### Core Service
- **VehicleRepository**: Interface para operações CRUD de veículos
- **MongoDBVehicleRepository**: Implementação concreta usando MongoDB
  - Suporta operações assíncronas
  - Implementa índices para otimização
  - Tratamento de erros e retry policies

### Sales Service
- **SaleRepository**: Interface para operações CRUD de vendas
- **MongoDBSaleRepository**: Implementação concreta usando MongoDB
  - Suporta operações assíncronas
  - Implementa índices para otimização
  - Tratamento de erros e retry policies
  - Validação de dados e integridade referencial

## Testes

### Cobertura de Testes
O projeto mantém uma cobertura de testes acima de 80% para garantir a qualidade do código. Os testes são organizados em:

#### Testes de Domínio
- Validação de regras de negócio
- Testes de modelos e entidades
- Testes de exceções personalizadas

#### Testes de Serviço
- Testes de casos de sucesso
- Testes de casos de erro
- Testes de integração com repositórios

#### Testes de API
- Testes de endpoints
- Testes de validação de dados
- Testes de casos de erro HTTP

#### Testes de Repositório
- Testes de operações CRUD
- Testes de conexão com banco de dados
- Testes de tratamento de erros

### Executando os Testes
```bash
# Instalar dependências
make install

# Executar testes com cobertura
make test-coverage

# Executar testes específicos
pytest tests/test_sale_controller.py -v
pytest tests/test_sale_service.py -v
pytest tests/test_sale_repository.py -v
```

## Segurança
O sistema implementa as seguintes medidas de segurança:

### Autenticação
- JWT para autenticação de usuários
- Tokens com expiração configurável
- Refresh tokens para renovação

### Autorização
- RBAC (Role-Based Access Control)
- Roles: admin, seller, viewer
- Permissões granulares por recurso

### Proteção de Dados
- Criptografia de dados sensíveis
- Mascaramento de CPF em logs
- Validação de entrada de dados

### Segurança da API
- Rate limiting por IP/usuário
- Validação de payloads
- Sanitização de inputs
- Proteção contra SQL injection
- CORS configurado

## Monitoramento
O sistema implementa as seguintes ferramentas de monitoramento:

### Logs
- Logs estruturados em JSON
- Níveis de log configuráveis
- Rotação de logs
- Agregação de logs

### Métricas
- Prometheus para coleta de métricas
- Grafana para visualização
- Alertas configuráveis

### Rastreamento
- OpenTelemetry para tracing
- Correlação de IDs
- Tempo de resposta por endpoint

## Deploy
O sistema pode ser implantado de duas formas:

### Desenvolvimento
```bash
# Instalar dependências
make install

# Iniciar serviços
make up

# Acessar APIs
http://localhost:8000/docs  # Core Service
http://localhost:8001/docs  # Sales Service
```

### Produção
```bash
# Construir imagens
docker-compose build

# Iniciar serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f
```

## Status dos Veículos
Os veículos podem ter os seguintes status:
- `DISPONÍVEL`: Veículo disponível para venda
- `RESERVADO`: Veículo reservado
- `VENDIDO`: Veículo vendido

## Status de Pagamento
As vendas podem ter os seguintes status de pagamento:
- `PENDENTE`: Pagamento pendente
- `PAGO`: Pagamento realizado
- `CANCELADA`: Pagamento cancelado

## Rotas da API

### Core Service (http://localhost:8000)

#### Veículos
- **Criar Veículo**
  ```bash
  curl -X POST http://localhost:8000/vehicles/ \
    -H "Content-Type: application/json" \
    -d '{
      "brand": "Toyota",
      "model": "Corolla",
      "year": 2023,
      "color": "Prata",
      "price": 120000.00,
      "status": "DISPONÍVEL"
    }'
  ```

- **Listar Todos os Veículos**
  ```bash
  curl -X GET http://localhost:8000/vehicles/
  ```

- **Listar Veículos Disponíveis**
  ```bash
  curl -X GET http://localhost:8000/vehicles/available/
  ```

- **Listar Veículos Reservados**
  ```bash
  curl -X GET http://localhost:8000/vehicles/reserved/
  ```

- **Listar Veículos Vendidos**
  ```bash
  curl -X GET http://localhost:8000/vehicles/sold/
  ```

- **Obter Veículo por ID**
  ```bash
  curl -X GET http://localhost:8000/vehicles/{vehicle_id}
  ```

- **Atualizar Veículo**
  ```bash
  curl -X PUT http://localhost:8000/vehicles/{vehicle_id} \
    -H "Content-Type: application/json" \
    -d '{
      "brand": "Toyota",
      "model": "Corolla",
      "year": 2023,
      "color": "Prata",
      "price": 125000.00,
      "status": "DISPONÍVEL"
    }'
  ```

- **Deletar Veículo**
  ```bash
  curl -X DELETE http://localhost:8000/vehicles/{vehicle_id}
  ```

#### Gerenciamento de Status

- **Marcar Veículo como Disponível**
  ```bash
  curl -X POST http://localhost:8000/vehicles/{vehicle_id}/mark-as-available
  ```

- **Marcar Veículo como Reservado**
  ```bash
  curl -X POST http://localhost:8000/vehicles/{vehicle_id}/mark-as-reserved
  ```

- **Marcar Veículo como Vendido**
  ```bash
  curl -X POST http://localhost:8000/vehicles/{vehicle_id}/mark-as-sold
  ```

### Sales Service (http://localhost:8001)

#### Vendas
- **Criar Venda**
  ```bash
  curl -X POST http://localhost:8001/sales/ \
    -H "Content-Type: application/json" \
    -d '{
      "vehicle_id": "123",
      "buyer_cpf": "12345678901",
      "sale_price": 120000.00,
      "payment_code": "PAY123"
    }'
  ```

- **Listar Vendas**
  ```bash
  # Listar todas as vendas
  curl -X GET http://localhost:8001/sales/

  # Listar vendas por status
  curl -X GET "http://localhost:8001/sales/status/PENDENTE" # PAGO, CANCELADO
  ```

- **Obter Venda por ID**
  ```bash
  curl -X GET http://localhost:8001/sales/{sale_id}
  ```

- **Obter Venda por Código de Pagamento**
  ```bash
  curl -X GET http://localhost:8001/sales/payment/{payment_code}
  ```

- **Atualizar Venda**
  ```bash
  curl -X PUT http://localhost:8001/sales/{sale_id} \
    -H "Content-Type: application/json" \
    -d '{
      "sale_price": 125000.00
    }'
  ```

- **Deletar Venda**
  ```bash
  curl -X DELETE http://localhost:8001/sales/{sale_id}
  ```

#### Gerenciamento de Status de Pagamento

- **Marcar Venda como Pendente**
  ```bash
  curl -X PATCH http://localhost:8001/sales/{sale_id}/mark-as-pending
  ```

- **Marcar Venda como Paga**
  ```bash
  curl -X PATCH http://localhost:8001/sales/{sale_id}/mark-as-paid
  ```

- **Marcar Venda como Cancelada**
  ```bash
  curl -X PATCH http://localhost:8001/sales/{sale_id}/mark-as-canceled
  ```

- **Webhook de Pagamento**
  ```bash
  curl -X POST http://localhost:8001/sales/webhook/payment \
    -H "Content-Type: application/json" \
    -d '{
      "payment_code": "HONDA4321",
      "status": "PAGO",
      "vehicle_id": "67f6dc9d1fd405347d2231e3"
    }'
  ```

## Exemplos de Uso

### Fluxo Completo de Venda

1. **Criar um Veículo**
   ```bash
   curl -X POST http://localhost:8000/vehicles/ \
     -H "Content-Type: application/json" \
     -d '{
       "brand": "Toyota",
       "model": "Corolla",
       "year": 2023,
       "color": "Prata",
       "price": 120000.00,
       "status": "DISPONÍVEL"
     }'
   ```

2. **Verificar Veículos Disponíveis**
   ```bash
   curl -X GET http://localhost:8001/sales/vehicles/available
   ```

3. **Criar uma Venda**
   ```bash
   curl -X POST http://localhost:8001/sales/ \
     -H "Content-Type: application/json" \
     -d '{
       "vehicle_id": "123",
       "buyer_cpf": "12345678901",
       "sale_date": "2024-03-20T10:00:00Z"
     }'
   ```

4. **Simular Webhook de Pagamento Aprovado**
   ```bash
   curl -X POST http://localhost:8001/sales/webhook/payment \
     -H "Content-Type: application/json" \
     -d '{
       "payment_id": "123",
       "status": "PAGO"
     }'
   ```

5. **Verificar Veículos Vendidos**
   ```bash
   curl -X GET http://localhost:8001/sales/vehicles/sold
   ```

### Fluxo de Reserva

1. **Criar um Veículo**
   ```bash
   curl -X POST http://localhost:8000/vehicles/ \
     -H "Content-Type: application/json" \
     -d '{
       "brand": "Honda",
       "model": "Civic",
       "year": 2023,
       "color": "Preto",
       "price": 110000.00,
       "status": "DISPONÍVEL"
     }'
   ```

2. **Marcar como Reservado**
   ```bash
   curl -X POST http://localhost:8000/vehicles/{vehicle_id}/mark-as-reserved
   ```

3. **Verificar Veículos Reservados**
   ```bash
   curl -X GET http://localhost:8000/vehicles/reserved/
   ```

4. **Marcar como Disponível Novamente**
   ```bash
   curl -X POST http://localhost:8000/vehicles/{vehicle_id}/mark-as-available
   ```

## Fluxo de Status
1. Um veículo começa como `DISPONÍVEL` (Disponível)
2. Pode ser marcado como `RESERVADO` (Reservado)
3. Pode voltar para `DISPONÍVEL` (Disponível)
4. Pode ser marcado como `VENDIDO` (Vendido)
5. Uma vez `VENDIDO`, não pode mais mudar de status

## Comandos Make

### Desenvolvimento
- `make install`: Instala as dependências e constrói as imagens Docker
- `make setup`: Configura o ambiente de desenvolvimento
- `make up`: Inicia os serviços
- `make down`: Para os serviços
- `make restart`: Reinicia todos os serviços e mostra os logs
- `make logs`: Mostra os logs dos serviços
- `make clean`: Limpa o ambiente de desenvolvimento

### Testes
- `make test`: Executa todos os testes
- `make test-core`: Executa os testes do core-service
- `make test-sales`: Executa os testes do sales-service

### Banco de Dados
- `make mongodb`: Inicia apenas o MongoDB
- `make mongodb-logs`: Mostra os logs do MongoDB

### Serviços Individuais
- `make core`: Inicia apenas o core-service
- `make sales`: Inicia apenas o sales-service
- `make core-logs`: Mostra os logs do core-service
- `make sales-logs`: Mostra os logs do sales-service

### Qualidade de Código
- `make lint`: Executa os linters
- `make type-check`: Verifica os tipos

### Manutenção
- `make rebuild`: Reconstrói os containers
- `make status`: Verifica o status dos serviços

## API Documentation

### Core Service (http://localhost:8000)

#### Vehicles

##### List Vehicles
```http
GET /vehicles
```

##### Create Vehicle
```http
POST /vehicles
Content-Type: application/json

{
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2023,
  "color": "Silver",
  "price": 120000.00
}
```

##### Get Vehicle
```http
GET /vehicles/{vehicle_id}
```

##### Update Vehicle
```http
PUT /vehicles/{vehicle_id}
Content-Type: application/json

{
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2024,
  "color": "Black",
  "price": 125000.00
}
```

##### Delete Vehicle
```http
DELETE /vehicles/{vehicle_id}
```

### Sales Service (http://localhost:8001)

#### Sales

##### List Sales
```http
GET /sales?status=PENDENTE
```

##### Create Sale
```http
POST /sales
Content-Type: application/json

{
  "vehicle_id": "65f8a1b2c3d4e5f6a7b8c9d0",
  "buyer_cpf": "12345678901",
  "sale_date": "2024-03-20T12:00:00.000Z"
}
```

##### Get Sale
```http
GET /sales/{sale_id}
```

##### Payment Webhook
```http
POST /webhook/payment
Content-Type: application/json

{
  "payment_id": "pay_123456789",
  "status": "PAGO"
}
```

##### List Vehicles for Sale
```http
GET /vehicles?status=available&sort=price
```

##### List Sold Vehicles
```http
GET /vehicles/sold?sort=price
```

## Testando a API

Para testar a API, você pode usar o Insomnia:

1. Importe os arquivos de configuração:
   - `core-service/insomnia.json`
   - `sales-service/insomnia.json`

2. Configure o ambiente:
   - Core Service: http://localhost:8000
   - Sales Service: http://localhost:8001

3. Execute as requisições de exemplo

## Requisitos

- Python 3.11+
- Docker
- Docker Compose
- MongoDB

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Instale as dependências:
```bash
make install
```

## Contribuição

1. Crie uma branch para sua feature:
```bash
git checkout -b feature/nova-feature
```

2. Faça commit das suas alterações:
```bash
git commit -m "feat: adiciona nova feature"
```

3. Push para a branch:
```bash
git push origin feature/nova-feature
```

4. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT. 