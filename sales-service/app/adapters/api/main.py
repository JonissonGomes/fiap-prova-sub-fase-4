from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dependencies import get_db, get_sale_service
from app.adapters.api.endpoints import router as sale_router
from app.adapters.repository.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sale API")

app.include_router(sale_router, prefix="/sales", tags=["sales"]) 