from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from ...domain.sale import Sale, PaymentStatus

class SaleBase(BaseModel):
    vehicle_id: int
    customer_cpf: str
    price: float
    payment_code: str

    @validator('customer_cpf')
    def validate_cpf(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

    @validator('payment_code')
    def validate_payment_code(cls, v):
        if not v:
            raise ValueError('Código de pagamento é obrigatório')
        return v

class SaleCreate(SaleBase):
    def to_domain(self) -> Sale:
        return Sale(
            vehicle_id=self.vehicle_id,
            customer_cpf=self.customer_cpf,
            price=self.price,
            payment_code=self.payment_code
        )

class SaleUpdate(BaseModel):
    payment_status: PaymentStatus

    def to_domain(self) -> Sale:
        return Sale(
            payment_status=self.payment_status
        )

class SaleResponse(SaleBase):
    id: int
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, sale: Sale) -> 'SaleResponse':
        return cls(
            id=sale.id,
            vehicle_id=sale.vehicle_id,
            customer_cpf=sale.customer_cpf,
            price=sale.price,
            payment_code=sale.payment_code,
            payment_status=sale.payment_status,
            created_at=sale.created_at,
            updated_at=sale.updated_at
        ) 