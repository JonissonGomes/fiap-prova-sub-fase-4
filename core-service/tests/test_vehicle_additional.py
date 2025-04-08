import pytest
from pydantic import ValidationError
from datetime import datetime, UTC
from app.domain.vehicle import Vehicle, VehicleStatus

def test_validate_vehicle_with_minimal_data():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0
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
    assert vehicle.created_at is not None
    assert vehicle.updated_at is not None

def test_validate_vehicle_with_invalid_year_future():
    # Arrange
    current_year = datetime.now(UTC).year
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": current_year + 2,
        "color": "Prata",
        "price": 100000.0
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        Vehicle(**vehicle_data)

def test_validate_vehicle_with_invalid_price_negative():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": -100000.0
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Vehicle(**vehicle_data)
    assert "Preço deve ser maior que zero" in str(exc_info.value)

def test_validate_vehicle_with_invalid_color_empty():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "",
        "price": 100000.0
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        Vehicle(**vehicle_data)

def test_validate_vehicle_with_invalid_brand_empty():
    # Arrange
    vehicle_data = {
        "brand": "",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        Vehicle(**vehicle_data)

def test_validate_vehicle_with_invalid_model_empty():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        Vehicle(**vehicle_data)

def test_validate_vehicle_with_whitespace_in_fields():
    # Arrange
    vehicle_data = {
        "brand": " Toyota ",
        "model": " Corolla ",
        "year": 2022,
        "color": " Prata ",
        "price": 100000.0
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.brand == "Toyota"
    assert vehicle.model == "Corolla"
    assert vehicle.color == "Prata"

def test_validate_vehicle_with_special_characters():
    # Arrange
    vehicle_data = {
        "brand": "Toyota!@#",
        "model": "Corolla$%^",
        "year": 2022,
        "color": "Prata&*(",
        "price": 100000.0
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.brand == "Toyota!@#"
    assert vehicle.model == "Corolla$%^"
    assert vehicle.color == "Prata&*("

def test_validate_vehicle_with_max_price():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 999999999.99
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.price == 999999999.99

def test_validate_vehicle_with_min_price():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 0.01
    }

    # Act
    vehicle = Vehicle(**vehicle_data)

    # Assert
    assert vehicle.price == 0.01

def test_validate_vehicle_with_different_status_transitions():
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

    # Act & Assert
    vehicle.mark_as_pending()
    assert vehicle.status == VehicleStatus.RESERVED

    vehicle.mark_as_available()
    assert vehicle.status == VehicleStatus.AVAILABLE

    vehicle.mark_as_pending()
    assert vehicle.status == VehicleStatus.RESERVED

    vehicle.mark_as_sold()
    assert vehicle.status == VehicleStatus.SOLD

def test_validate_vehicle_with_invalid_status_transition():
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

def test_validate_vehicle_with_updated_at_changes():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0
    }
    vehicle = Vehicle(**vehicle_data)
    initial_updated_at = vehicle.updated_at

    # Act
    vehicle.update(brand="Honda")

    # Assert
    assert vehicle.brand == "Honda"
    assert vehicle.updated_at > initial_updated_at

def test_validate_vehicle_with_multiple_updates():
    # Arrange
    vehicle_data = {
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2022,
        "color": "Prata",
        "price": 100000.0
    }
    vehicle = Vehicle(**vehicle_data)

    # Act
    vehicle.update(brand="Honda", model="Civic", color="Preto", price=110000.0)

    # Assert
    assert vehicle.brand == "Honda"
    assert vehicle.model == "Civic"
    assert vehicle.color == "Preto"
    assert vehicle.price == 110000.0 