from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator

from app.adapters.repository.database import SessionLocal
from app.adapters.repository.sqlalchemy_sale_repository import SQLAlchemySaleRepository
from app.adapters.service.sale_service import SaleServiceImpl
from app.ports.sale_service import SaleService

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    repository = SQLAlchemySaleRepository(db)
    return SaleServiceImpl(repository) 