"""
Modelos do banco de dados
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from app.domain.sale import SaleStatus

Base = declarative_base()

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, nullable=False)
    buyer_cpf = Column(String(11), nullable=False)
    sale_date = Column(DateTime, nullable=False)
    status = Column(SQLEnum(SaleStatus), default=SaleStatus.PENDING)
    payment_id = Column(String, nullable=True)
    payment_date = Column(DateTime, nullable=True) 