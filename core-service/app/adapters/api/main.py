from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .endpoints import router as vehicle_router
from ..repository.sqlalchemy_vehicle_repository import SQLAlchemyVehicleRepository
from ..service.vehicle_service import VehicleService
from ..repository.models import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Core Service", description="API para gerenciamento de veículos")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_vehicle_service(db: Session = Depends(get_db)) -> VehicleService:
    repository = SQLAlchemyVehicleRepository(db)
    return VehicleService(repository)

app.include_router(vehicle_router, prefix="/api/v1/vehicles", tags=["vehicles"], dependencies=[Depends(get_vehicle_service)]) 