from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="Sales Service API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Métodos permitidos
    allow_headers=["*"],  # Permite todos os headers
    expose_headers=["*"]  # Expõe todos os headers na resposta
)

app.include_router(router, prefix="/api/v1") 