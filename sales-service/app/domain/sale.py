from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

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

    def mark_as_paid(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            self.payment_status = PaymentStatus.PAID
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Venda não está com status pendente")

    def mark_as_cancelled(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            self.payment_status = PaymentStatus.CANCELLED
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Venda não está com status pendente")

    def validate(self) -> None:
        if not self.vehicle_id:
            raise ValueError("ID do veículo é obrigatório")
        if not self.buyer_cpf or len(self.buyer_cpf) != 11:
            raise ValueError("CPF inválido")
        if self.price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if not self.payment_code:
            raise ValueError("Código de pagamento é obrigatório") 