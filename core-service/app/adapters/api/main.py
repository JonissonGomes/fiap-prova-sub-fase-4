from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.api.endpoints import router

app = FastAPI(title="Vehicle API", version="1.0.0")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router, prefix="/vehicles", tags=["vehicles"]) 