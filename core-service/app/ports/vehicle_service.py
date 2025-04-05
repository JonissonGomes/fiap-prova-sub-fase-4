from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.vehicle import Vehicle

class VehicleService(ABC):
    @abstractmethod
    def create_vehicle(self, vehicle: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        pass

    @abstractmethod
    def get_vehicles(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def get_available_vehicles(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def update_vehicle(self, vehicle_id: int, **kwargs) -> Optional[Vehicle]:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> bool:
        pass

    @abstractmethod
    def mark_vehicle_as_sold(self, vehicle_id: int) -> Optional[Vehicle]:
        pass 