FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Instala o pacote em modo de desenvolvimento
RUN pip install -e .

# Se estiver rodando testes, use o .env.test
ARG ENV_FILE=.env
COPY ${ENV_FILE} .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 