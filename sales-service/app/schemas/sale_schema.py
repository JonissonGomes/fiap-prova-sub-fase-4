from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDENTE"
    PAID = "PAGO"
    CANCELLED = "CANCELADO"

class SaleBase(BaseModel):
    """Schema base para vendas."""
    vehicle_id: str = Field(..., description="ID do veículo")
    buyer_cpf: str = Field(..., description="CPF do comprador")
    sale_price: float = Field(..., gt=0, description="Preço da venda")
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_code: Optional[str] = Field(None, description="Código de pagamento")

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
    id: str = Field(..., description="ID da venda")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")

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