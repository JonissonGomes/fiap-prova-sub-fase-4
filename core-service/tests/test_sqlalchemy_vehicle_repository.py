import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from app.adapters.repository.models import Base, VehicleModel
from app.adapters.repository.sqlalchemy_vehicle_repository import SQLAlchemyVehicleRepository
from app.domain.vehicle import Vehicle, VehicleStatus

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def repository(db_session):
    return SQLAlchemyVehicleRepository(db_session)

def test_save_vehicle(repository):
    # Arrange
    vehicle = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status="AVAILABLE"
    )

    # Act
    saved_vehicle = repository.save(vehicle)

    # Assert
    assert saved_vehicle.id is not None
    assert saved_vehicle.brand == "Toyota"
    assert saved_vehicle.model == "Corolla"
    assert saved_vehicle.year == 2022
    assert saved_vehicle.color == "Prata"
    assert saved_vehicle.price == 100000.0
    assert saved_vehicle.status == "AVAILABLE"
    assert isinstance(saved_vehicle.created_at, datetime)
    assert isinstance(saved_vehicle.updated_at, datetime)

def test_find_by_id(repository):
    # Arrange
    vehicle = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status="AVAILABLE"
    )
    saved_vehicle = repository.save(vehicle)

    # Act
    found_vehicle = repository.find_by_id(saved_vehicle.id)

    # Assert
    assert found_vehicle is not None
    assert found_vehicle.id == saved_vehicle.id
    assert found_vehicle.brand == "Toyota"
    assert found_vehicle.model == "Corolla"
    assert found_vehicle.year == 2022
    assert found_vehicle.color == "Prata"
    assert found_vehicle.price == 100000.0
    assert found_vehicle.status == "AVAILABLE"

def test_find_by_id_not_found(repository):
    # Act
    found_vehicle = repository.find_by_id(999)

    # Assert
    assert found_vehicle is None

def test_find_all(repository):
    # Arrange
    vehicles = [
        Vehicle(
            brand="Toyota",
            model="Corolla",
            year=2022,
            color="Prata",
            price=100000.0,
            status="AVAILABLE"
        ),
        Vehicle(
            brand="Honda",
            model="Civic",
            year=2023,
            color="Preto",
            price=110000.0,
            status="SOLD"
        )
    ]
    for vehicle in vehicles:
        repository.save(vehicle)

    # Act
    found_vehicles = repository.find_all()

    # Assert
    assert len(found_vehicles) == 2
    assert found_vehicles[0].brand == "Toyota"
    assert found_vehicles[1].brand == "Honda"

def test_find_available(repository):
    # Arrange
    vehicles = [
        Vehicle(
            brand="Toyota",
            model="Corolla",
            year=2022,
            color="Prata",
            price=100000.0,
            status="AVAILABLE"
        ),
        Vehicle(
            brand="Honda",
            model="Civic",
            year=2023,
            color="Preto",
            price=110000.0,
            status="SOLD"
        )
    ]
    for vehicle in vehicles:
        repository.save(vehicle)

    # Act
    available_vehicles = repository.find_available()

    # Assert
    assert len(available_vehicles) == 1
    assert available_vehicles[0].brand == "Toyota"
    assert available_vehicles[0].status == "AVAILABLE"

def test_update_vehicle(repository):
    # Arrange
    vehicle = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status="AVAILABLE"
    )
    saved_vehicle = repository.save(vehicle)

    # Act
    updated_vehicle = Vehicle(
        id=saved_vehicle.id,
        brand="Honda",
        model="Civic",
        year=2023,
        color="Preto",
        price=110000.0,
        status="AVAILABLE",
        created_at=saved_vehicle.created_at
    )
    result = repository.update(updated_vehicle)

    # Assert
    assert result.id == saved_vehicle.id
    assert result.brand == "Honda"
    assert result.model == "Civic"
    assert result.year == 2023
    assert result.color == "Preto"
    assert result.price == 110000.0
    assert result.status == "AVAILABLE"

def test_update_vehicle_not_found(repository):
    # Arrange
    vehicle = Vehicle(
        id=999,
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status="AVAILABLE"
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Veículo não encontrado"):
        repository.update(vehicle)

def test_delete_vehicle(repository):
    # Arrange
    vehicle = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status="AVAILABLE"
    )
    saved_vehicle = repository.save(vehicle)

    # Act
    repository.delete(saved_vehicle.id)

    # Assert
    found_vehicle = repository.find_by_id(saved_vehicle.id)
    assert found_vehicle is None

def test_delete_vehicle_not_found(repository):
    # Act & Assert
    with pytest.raises(ValueError, match="Veículo não encontrado"):
        repository.delete(999) 