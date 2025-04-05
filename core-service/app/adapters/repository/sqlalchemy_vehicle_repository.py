from sqlalchemy.orm import Session
from typing import List, Optional
from ...domain.vehicle import Vehicle
from ...ports.vehicle_repository import VehicleRepository
from .models import VehicleModel

class SQLAlchemyVehicleRepository(VehicleRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, vehicle: Vehicle) -> Vehicle:
        vehicle.validate()
        db_vehicle = VehicleModel(
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            color=vehicle.color,
            price=vehicle.price,
            status=vehicle.status
        )
        self.session.add(db_vehicle)
        self.session.commit()
        self.session.refresh(db_vehicle)
        return self._to_domain(db_vehicle)

    def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        db_vehicle = self.session.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        return self._to_domain(db_vehicle) if db_vehicle else None

    def find_all(self) -> List[Vehicle]:
        db_vehicles = self.session.query(VehicleModel).all()
        return [self._to_domain(vehicle) for vehicle in db_vehicles]

    def find_available(self) -> List[Vehicle]:
        db_vehicles = self.session.query(VehicleModel).filter(
            VehicleModel.status == Vehicle.status.AVAILABLE
        ).all()
        return [self._to_domain(vehicle) for vehicle in db_vehicles]

    def update(self, vehicle: Vehicle) -> Vehicle:
        db_vehicle = self.session.query(VehicleModel).filter(VehicleModel.id == vehicle.id).first()
        if db_vehicle:
            for key, value in vehicle.__dict__.items():
                if key != 'id' and hasattr(db_vehicle, key):
                    setattr(db_vehicle, key, value)
            self.session.commit()
            self.session.refresh(db_vehicle)
            return self._to_domain(db_vehicle)
        return None

    def delete(self, vehicle_id: int) -> bool:
        db_vehicle = self.session.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if db_vehicle:
            self.session.delete(db_vehicle)
            self.session.commit()
            return True
        return False

    def _to_domain(self, db_vehicle: VehicleModel) -> Vehicle:
        return Vehicle(
            id=db_vehicle.id,
            brand=db_vehicle.brand,
            model=db_vehicle.model,
            year=db_vehicle.year,
            color=db_vehicle.color,
            price=db_vehicle.price,
            status=db_vehicle.status,
            created_at=db_vehicle.created_at,
            updated_at=db_vehicle.updated_at
        ) 