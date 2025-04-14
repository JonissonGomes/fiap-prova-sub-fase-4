# Sistema de Vendas - Frontend

Frontend do sistema de gerenciamento de veículos, vendas e pagamentos.

## Tecnologias Utilizadas

- React
- TypeScript
- Material-UI
- React Router
- Axios

## Pré-requisitos

- Node.js (versão 14 ou superior)
- npm (gerenciador de pacotes do Node.js)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VEHICLES_SERVICE_URL=http://localhost:8001
REACT_APP_SALES_SERVICE_URL=http://localhost:8002
REACT_APP_PAYMENTS_SERVICE_URL=http://localhost:8003
```

## Execução

1. Inicie o servidor de desenvolvimento:
```bash
npm start
```

2. Acesse a aplicação no navegador:
```
http://localhost:3000
```

## Scripts Disponíveis

- `npm start`: Inicia o servidor de desenvolvimento
- `npm test`: Executa os testes
- `npm run build`: Cria a versão de produção
- `npm run lint`: Executa o linter
- `npm run format`: Formata o código

## Estrutura do Projeto

```
frontend/
├── public/              # Arquivos estáticos
├── src/
│   ├── components/      # Componentes reutilizáveis
│   ├── pages/          # Páginas da aplicação
│   ├── services/       # Serviços de API
│   ├── types/          # Definições de tipos
│   ├── App.tsx         # Componente principal
│   └── index.tsx       # Ponto de entrada
├── package.json        # Dependências e scripts
└── tsconfig.json       # Configuração do TypeScript
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

3. Envie para o repositório:
```bash
git push origin feature/nova-feature
```

4. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT. 