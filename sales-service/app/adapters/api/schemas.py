from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ...domain.sale import PaymentStatus

class SaleBase(BaseModel):
    vehicle_id: int = Field(..., description="ID do veículo")
    buyer_cpf: str = Field(..., description="CPF do comprador")
    price: float = Field(..., description="Preço da venda")
    payment_code: str = Field(..., description="Código do pagamento")

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    payment_status: Optional[PaymentStatus] = None

class SaleResponse(SaleBase):
    id: int
    payment_status: PaymentStatus
    sale_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 