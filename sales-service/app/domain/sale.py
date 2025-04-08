from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from enum import Enum
import re
from pydantic import BaseModel, Field

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class SaleStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"

@dataclass
class Sale:
    id: Optional[int] = None
    vehicle_id: int = 0
    buyer_cpf: str = ""
    price: float = 0.0
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_code: Optional[str] = None
    sale_date: datetime = datetime.now(UTC)
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)
    status: SaleStatus = SaleStatus.PENDING
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None

    def mark_as_paid(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            self.payment_status = PaymentStatus.PAID
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Venda não está com status reservado")

    def mark_as_cancelled(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            self.payment_status = PaymentStatus.CANCELLED
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Venda não está com status reservado")

    def validate(self) -> None:
        if not self.vehicle_id:
            raise ValueError("ID do veículo é obrigatório")
        
        cpf = re.sub(r'[^\d]', '', self.buyer_cpf)
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido")
        
        if self.price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if not self.payment_code or not self.payment_code.strip():
            raise ValueError("Código de pagamento é obrigatório")
        
        if not isinstance(self.payment_status, PaymentStatus):
            raise ValueError("Status de pagamento inválido")

class SaleBase(BaseModel):
    vehicle_id: str = Field(..., description="ID do veículo vendido")
    buyer_cpf: str = Field(..., description="CPF do comprador")
    sale_date: datetime = Field(default_factory=datetime.now, description="Data da venda")
    status: SaleStatus = Field(default=SaleStatus.PENDING, description="Status da venda")

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: str = Field(..., description="ID da venda")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação")
    updated_at: datetime = Field(default_factory=datetime.now, description="Data de atualização")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 