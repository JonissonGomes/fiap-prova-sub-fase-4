from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ...domain.vehicle import VehicleStatus

class VehicleBase(BaseModel):
    brand: str = Field(..., description="Marca do veículo")
    model: str = Field(..., description="Modelo do veículo")
    year: int = Field(..., description="Ano do veículo")
    color: str = Field(..., description="Cor do veículo")
    price: float = Field(..., description="Preço do veículo")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    price: Optional[float] = None

class VehicleResponse(VehicleBase):
    id: int
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 