from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional

class VehicleStatus(str, Enum):
    AVAILABLE = "DISPONÍVEL"
    SOLD = "VENDIDO"
    RESERVED = "RESERVADO"

class VehicleBase(BaseModel):
    brand: str = Field(..., description="Marca do veículo")
    model: str = Field(..., description="Modelo do veículo")
    year: int = Field(..., description="Ano do veículo")
    color: str = Field(..., description="Cor do veículo")
    price: float = Field(..., description="Preço do veículo")
    status: VehicleStatus = Field(default=VehicleStatus.AVAILABLE, description="Status do veículo")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    brand: Optional[str] = Field(None, description="Marca do veículo")
    model: Optional[str] = Field(None, description="Modelo do veículo")
    year: Optional[int] = Field(None, description="Ano do veículo")
    color: Optional[str] = Field(None, description="Cor do veículo")
    price: Optional[float] = Field(None, description="Preço do veículo")

class Vehicle(BaseModel):
    id: Optional[str] = None
    brand: str
    model: str
    year: int
    color: str
    price: float
    status: VehicleStatus = VehicleStatus.AVAILABLE
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @validator('year')
    def validate_year(cls, v):
        if v < 1886:
            raise ValueError("Ano inválido")
        if v > datetime.now().year + 1:
            raise ValueError("Ano inválido")
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Preço deve ser maior que zero")
        return v

    @validator('color')
    def validate_color(cls, v):
        if not v or not v.strip():
            raise ValueError("Cor é obrigatória")
        return v.strip()

    @validator('brand')
    def validate_brand(cls, v):
        if not v or not v.strip():
            raise ValueError("Marca é obrigatória")
        return v.strip()

    @validator('model')
    def validate_model(cls, v):
        if not v or not v.strip():
            raise ValueError("Modelo é obrigatório")
        return v.strip()

    def mark_as_sold(self):
        if self.status == VehicleStatus.SOLD:
            raise ValueError("Veículo já está vendido")
        self.status = VehicleStatus.SOLD
        self.updated_at = datetime.now(UTC)

    def mark_as_pending(self):
        if self.status == VehicleStatus.RESERVED:
            raise ValueError("Veículo já está reservado")
        self.status = VehicleStatus.RESERVED
        self.updated_at = datetime.now(UTC)

    def mark_as_available(self):
        if self.status == VehicleStatus.AVAILABLE:
            raise ValueError("Veículo já está disponível")
        self.status = VehicleStatus.AVAILABLE
        self.updated_at = datetime.now(UTC)

    def update(self, **kwargs):
        if 'year' in kwargs and (kwargs['year'] < 1900 or kwargs['year'] > datetime.now().year):
            raise ValueError("Ano inválido")
        if 'price' in kwargs and kwargs['price'] <= 0:
            raise ValueError("Preço inválido")
        if 'color' in kwargs and not kwargs['color']:
            raise ValueError("Cor é obrigatória")
        if 'brand' in kwargs and not kwargs['brand']:
            raise ValueError("Marca é obrigatória")
        if 'model' in kwargs and not kwargs['model']:
            raise ValueError("Modelo é obrigatório")

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.updated_at = datetime.now(UTC)
