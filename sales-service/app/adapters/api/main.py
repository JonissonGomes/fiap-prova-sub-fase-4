from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

from app.controllers.sale_controller import router as sale_router
from app.infrastructure.mongodb_config import MongoDB
from app.adapters.mongodb_sale_repository import MongoDBSaleRepository
from app.services.sale_service_impl import SaleServiceImpl

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI(title="Sales Service API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização das dependências
repository = None
service = None

@app.get("/health")
async def health_check():
    """Endpoint para verificar a saúde do serviço."""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    global repository, service
    try:
        logger.info("Iniciando o serviço...")
        # Conecta ao MongoDB
        mongodb = MongoDB()
        await mongodb.connect()
        logger.info("Conectado ao MongoDB com sucesso!")
        
        # Inicializa o repositório e o serviço
        repository = MongoDBSaleRepository(
            mongodb.client,
            mongodb.settings.db_name,
            mongodb.settings.collection
        )
        service = SaleServiceImpl(repository)
        logger.info("Serviço inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar o serviço: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao inicializar o serviço: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    if repository and repository.client:
        await repository.client.close()
        logger.info("Conexão com MongoDB fechada.")

# Inclui as rotas
app.include_router(sale_router, tags=["sales"]) 