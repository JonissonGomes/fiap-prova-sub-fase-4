from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

class MongoDBSettings(BaseSettings):
    """Configurações do MongoDB."""
    url: str = "mongodb://localhost:27017"
    db_name: str = "sales_db"
    collection: str = "sales"

    class Config:
        env_prefix = "MONGODB_"
        env_file = ".env"

class MongoDB:
    """Classe para gerenciar a conexão com o MongoDB."""
    def __init__(self):
        self.settings = MongoDBSettings()
        self.client = None

    async def connect(self):
        """Estabelece conexão com o MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.settings.url)
            # Testa a conexão
            await self.client.admin.command('ping')
        except Exception as e:
            raise Exception(f"Erro ao conectar ao MongoDB: {str(e)}")

    async def disconnect(self):
        """Fecha a conexão com o MongoDB."""
        if self.client:
            self.client.close() 