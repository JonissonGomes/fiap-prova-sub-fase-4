from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Optional
from enum import Enum

class VehicleStatus(Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    PENDING = "pending"

@dataclass
class Vehicle:
    id: Optional[int] = None
    brand: str = ""
    model: str = ""
    year: int = 0
    color: str = ""
    price: float = 0.0
    status: VehicleStatus = VehicleStatus.AVAILABLE
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)

    def mark_as_sold(self) -> None:
        if self.status == VehicleStatus.AVAILABLE:
            self.status = VehicleStatus.SOLD
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Veículo não está disponível para venda")

    def mark_as_pending(self) -> None:
        if self.status == VehicleStatus.AVAILABLE:
            self.status = VehicleStatus.PENDING
            self.updated_at = datetime.now(UTC)
        else:
            raise ValueError("Veículo não está disponível para venda")

    def update(self, **kwargs) -> None:
        if self.status != VehicleStatus.AVAILABLE:
            raise ValueError("Não é possível atualizar um veículo que não está disponível")
            
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now(UTC)

    def validate(self) -> None:
        if not self.brand:
            raise ValueError("Marca é obrigatória")
        if not self.model:
            raise ValueError("Modelo é obrigatório")
        if self.year < 1900 or self.year > datetime.now(UTC).year:
            raise ValueError("Ano inválido")
        if not self.color:
            raise ValueError("Cor é obrigatória")
        if self.price <= 0:
            raise ValueError("Preço deve ser maior que zero") 