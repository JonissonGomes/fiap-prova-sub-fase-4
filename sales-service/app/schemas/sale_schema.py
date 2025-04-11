from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator, constr

class PaymentStatus(str, Enum):
    PENDING = "PENDENTE"
    PAID = "PAGO"
    CANCELLED = "CANCELADA"

class SaleBase(BaseModel):
    """Schema base para vendas."""
    vehicle_id: str
    buyer_cpf: str
    sale_price: float
    payment_code: str
    payment_status: PaymentStatus = PaymentStatus.PENDING

    @validator('buyer_cpf')
    def validate_cpf(cls, v):
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, v))
        if len(cpf) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return v

class SaleCreate(BaseModel):
    vehicle_id: constr(min_length=1)
    buyer_cpf: constr(min_length=11, max_length=11)
    sale_price: float = Field(gt=0)
    payment_code: constr(min_length=1)
    payment_status: PaymentStatus = PaymentStatus.PENDING

class SaleUpdate(BaseModel):
    vehicle_id: Optional[constr(min_length=1)] = None
    buyer_cpf: Optional[constr(min_length=11, max_length=11)] = None
    sale_price: Optional[float] = Field(default=None, gt=0)
    payment_code: Optional[constr(min_length=1)] = None
    payment_status: Optional[PaymentStatus] = None

class SaleResponse(BaseModel):
    id: str
    vehicle_id: str
    buyer_cpf: str
    sale_price: float
    payment_code: str
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @classmethod
    def from_domain(cls, sale):
        """Converte um objeto de domínio para o schema de resposta."""
        return cls(
            id=str(sale.id),
            vehicle_id=sale.vehicle_id,
            buyer_cpf=sale.buyer_cpf,
            sale_price=sale.sale_price,
            payment_status=sale.payment_status,
            payment_code=sale.payment_code,
            created_at=sale.created_at,
            updated_at=sale.updated_at
        ) 