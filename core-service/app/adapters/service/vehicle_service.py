from typing import List, Optional
from ...domain.vehicle import Vehicle
from ...ports.vehicle_repository import VehicleRepository
from ...ports.vehicle_service import VehicleService as VehicleServicePort

class VehicleService(VehicleServicePort):
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def create_vehicle(self, vehicle: Vehicle) -> Vehicle:
        vehicle.validate()
        return self.repository.save(vehicle)

    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.repository.find_by_id(vehicle_id)

    def get_vehicles(self) -> List[Vehicle]:
        return self.repository.find_all()

    def get_available_vehicles(self) -> List[Vehicle]:
        return self.repository.find_available()

    def update_vehicle(self, vehicle_id: int, **kwargs) -> Optional[Vehicle]:
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return None
        vehicle.update(**kwargs)
        return self.repository.update(vehicle)

    def delete_vehicle(self, vehicle_id: int) -> bool:
        return self.repository.delete(vehicle_id)

    def mark_vehicle_as_sold(self, vehicle_id: int) -> Optional[Vehicle]:
        vehicle = self.get_vehicle(vehicle_id)
        if not vehicle:
            return None
        vehicle.mark_as_sold()
        return self.repository.update(vehicle) 