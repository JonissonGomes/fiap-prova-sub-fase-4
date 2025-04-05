from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .endpoints import router as sale_router
from ..repository.sqlalchemy_sale_repository import SQLAlchemySaleRepository
from ..service.sale_service import SaleService
from ..repository.models import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Service", description="API para gerenciamento de vendas")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    repository = SQLAlchemySaleRepository(db)
    return SaleService(repository)

app.include_router(sale_router, prefix="/api/v1/sales", tags=["sales"], dependencies=[Depends(get_sale_service)]) 