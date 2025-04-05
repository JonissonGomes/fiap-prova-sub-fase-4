from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ...domain.vehicle import Vehicle
from ...ports.vehicle_service import VehicleService
from .schemas import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter()

@router.post("/", response_model=VehicleResponse)
async def create_vehicle(vehicle: VehicleCreate, service: VehicleService = Depends()):
    try:
        return service.create_vehicle(vehicle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: int, service: VehicleService = Depends()):
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return vehicle

@router.get("/", response_model=List[VehicleResponse])
async def get_vehicles(service: VehicleService = Depends()):
    return service.get_vehicles()

@router.get("/available/", response_model=List[VehicleResponse])
async def get_available_vehicles(service: VehicleService = Depends()):
    return service.get_available_vehicles()

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate, service: VehicleService = Depends()):
    try:
        return service.update_vehicle(vehicle_id, **vehicle.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, service: VehicleService = Depends()):
    if not service.delete_vehicle(vehicle_id):
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return {"message": "Veículo removido com sucesso"}

@router.post("/{vehicle_id}/mark-as-sold", response_model=VehicleResponse)
async def mark_vehicle_as_sold(vehicle_id: int, service: VehicleService = Depends()):
    try:
        return service.mark_vehicle_as_sold(vehicle_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 