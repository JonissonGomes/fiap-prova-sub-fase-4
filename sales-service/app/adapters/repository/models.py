from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, UTC
from ...domain.sale import PaymentStatus
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sales.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SaleModel(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, index=True)
    buyer_cpf = Column(String, index=True)
    price = Column(Float)
    payment_status = Column(Enum(PaymentStatus))
    payment_code = Column(String, unique=True, index=True)
    sale_date = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)) 