# Sistema de Revenda de Veículos

Sistema de revenda de veículos com arquitetura de microsserviços.

## Estrutura do Projeto

O projeto é composto por dois microsserviços principais:

1. **core-service**: Serviço principal responsável pelo cadastro e edição de veículos
2. **sales-service**: Serviço de vendas responsável pela listagem e processamento de vendas

## Requisitos

- Docker
- Docker Compose

## Como Executar

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Execute o projeto:
```bash
docker-compose up --build
```

Os serviços estarão disponíveis em:
- Core Service: http://localhost:8000
- Sales Service: http://localhost:8001

## Documentação da API

A documentação da API estará disponível em:
- Core Service: http://localhost:8000/docs
- Sales Service: http://localhost:8001/docs

## Testes

Para executar os testes:
```bash
docker-compose run core-service pytest
docker-compose run sales-service pytest
```

## CI/CD

O projeto utiliza GitHub Actions para CI/CD. Os testes são executados automaticamente em cada pull request. 