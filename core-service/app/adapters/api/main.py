from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dependencies import get_db, get_vehicle_service
from app.adapters.api.endpoints import router as vehicle_router
from app.adapters.repository.database import Base, engine
from app.adapters.service.vehicle_service import VehicleServiceImpl
from app.adapters.repository.sqlalchemy_vehicle_repository import SQLAlchemyVehicleRepository

# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle API")

# Registrar rotas
app.include_router(vehicle_router, prefix="/vehicles", tags=["vehicles"]) 