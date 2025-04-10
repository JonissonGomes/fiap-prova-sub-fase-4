from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

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

class SaleCreate(SaleBase):
    """Schema para criação de venda."""
    pass

class SaleUpdate(SaleBase):
    """Schema para atualização de venda."""
    pass

class SaleResponse(SaleBase):
    """Schema para resposta de venda."""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

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