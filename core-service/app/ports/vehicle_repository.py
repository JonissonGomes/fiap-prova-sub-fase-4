from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.vehicle import Vehicle

class VehicleRepository(ABC):
    @abstractmethod
    def save(self, vehicle: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        pass

    @abstractmethod
    def find_all(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def find_available(self) -> List[Vehicle]:
        pass

    @abstractmethod
    def update(self, vehicle: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    def delete(self, vehicle_id: int) -> bool:
        pass 