import pytest
from pydantic import ValidationError
from datetime import datetime, UTC
from app.domain.vehicle import Vehicle, VehicleStatus

def test_create_vehicle():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.brand == "Toyota"
    assert vehicle.model == "Corolla"
    assert vehicle.year == 2022
    assert vehicle.color == "Prata"
    assert vehicle.price == 100000.0
    assert vehicle.status == VehicleStatus.AVAILABLE

def test_create_vehicle_with_id():
    # Arrange
    vehicle_data = {
        "id": "1",
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.id == "1"
    assert vehicle.brand == "Toyota"
    assert vehicle.model == "Corolla"
    assert vehicle.year == 2022
    assert vehicle.color == "Prata"
    assert vehicle.price == 100000.0
    assert vehicle.status == VehicleStatus.AVAILABLE

def test_create_vehicle_with_dates():
    # Arrange
    now = datetime.now(UTC)
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE,
        "created_at": now,
        "updated_at": now
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.created_at == now
    assert vehicle.updated_at == now

def test_validate_year_valid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.year == 2022

def test_validate_year_invalid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 1800,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Vehicle(**vehicle_data)

    # Verifica se a mensagem esperada está no erro
    assert "Ano inválido" in str(exc_info.value)

def test_validate_price_valid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.price == 100000.0

def test_validate_price_invalid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 0.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Vehicle(**vehicle_data)

    assert "Preço deve ser maior que zero" in str(exc_info.value)

def test_mark_as_sold():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }
    vehicle = Vehicle(**vehicle_data)

    # Act
    vehicle.mark_as_sold()

    # Assert
    assert vehicle.status == VehicleStatus.SOLD
    assert vehicle.updated_at is not None

def test_mark_as_sold_already_sold():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.SOLD
    }
    vehicle = Vehicle(**vehicle_data)

    # Act & Assert
    with pytest.raises(ValueError, match="Veículo já está vendido"):
        vehicle.mark_as_sold()

def test_mark_as_pending():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }
    vehicle = Vehicle(**vehicle_data)

    # Act
    vehicle.mark_as_pending()

    # Assert
    assert vehicle.status == VehicleStatus.RESERVED
    assert vehicle.updated_at is not None

def test_mark_as_pending_already_pending():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.RESERVED
    }
    vehicle = Vehicle(**vehicle_data)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        vehicle.mark_as_pending()

    assert "Veículo já está reservado" in str(exc_info.value)

def test_update():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }
    vehicle = Vehicle(**vehicle_data)

    # Act
    vehicle.update(brand="Honda", model="Civic")

    # Assert
    assert vehicle.brand == "Honda"
    assert vehicle.model == "Civic"
    assert vehicle.updated_at is not None

def test_validate_color_valid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": " Azul  ",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.color == "Azul"


def test_validate_color_invalid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "   ",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Vehicle(**vehicle_data)

    assert "Cor é obrigatória" in str(exc_info.value)

def test_validate_brand_valid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Azul",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.brand == "Toyota"

def test_validate_brand_invalid():
    vehicle_data = {
        "brand": " ",
        "model": "Corolla",
        "year": 2022,
        "color": "Preto",
        "price": 95000.0,
        "status": VehicleStatus.AVAILABLE
    }

    with pytest.raises(ValidationError) as exc_info:
        Vehicle(**vehicle_data)

    assert "Marca é obrigatória" in str(exc_info.value)


def test_validate_model_valid():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Azul",
        "price": 100000.0,
        "status": VehicleStatus.AVAILABLE
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.model == "Corolla"

def test_validate_model_invalid():
    # Arrange
    model = ""
    
    # Act & Assert
    with pytest.raises(ValueError, match="Modelo é obrigatório"):
        Vehicle.validate_model(model)

def test_mark_as_available():
    # Arrange
    vehicle = Vehicle(
        id="1",
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status=VehicleStatus.RESERVED
    )
    
    # Act
    vehicle.mark_as_available()
    
    # Assert
    assert vehicle.status == VehicleStatus.AVAILABLE

def test_mark_as_available_already_available():
    # Arrange
    vehicle = Vehicle(
        id="1",
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status=VehicleStatus.AVAILABLE
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Veículo já está disponível"):
        vehicle.mark_as_available()

def test_update_with_invalid_data():
    # Arrange
    vehicle = Vehicle(
        id="1",
        brand="Toyota",
        model="Corolla",
        year=2022,
        color="Prata",
        price=100000.0,
        status=VehicleStatus.AVAILABLE
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Ano inválido"):
        vehicle.update(year=1800)
    
    with pytest.raises(ValueError, match="Preço inválido"):
        vehicle.update(price=-1000)
    
    with pytest.raises(ValueError, match="Cor é obrigatória"):
        vehicle.update(color="")
    
    with pytest.raises(ValueError, match="Marca é obrigatória"):
        vehicle.update(brand="")
    
    with pytest.raises(ValueError, match="Modelo é obrigatório"):
        vehicle.update(model="") 