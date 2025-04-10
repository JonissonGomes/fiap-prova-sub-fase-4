from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SaleBase(BaseModel):
    """Base schema para vendas."""
    vehicle_id: str = Field(..., description="ID do veículo vendido")
    buyer_cpf: str = Field(..., description="CPF do comprador")
    sale_price: float = Field(..., description="Preço da venda")
    payment_code: str = Field(..., description="Código de pagamento")
    payment_status: str = Field(..., description="Status do pagamento")

class SaleCreate(SaleBase):
    """Schema para criação de venda."""
    pass

class SaleUpdate(BaseModel):
    """Schema para atualização de venda."""
    vehicle_id: Optional[str] = Field(None, description="ID do veículo vendido")
    buyer_cpf: Optional[str] = Field(None, description="CPF do comprador")
    sale_price: Optional[float] = Field(None, description="Preço da venda")
    payment_code: Optional[str] = Field(None, description="Código de pagamento")
    payment_status: Optional[str] = Field(None, description="Status do pagamento") 