import pytest
from datetime import datetime
from bson import ObjectId
from app.schemas.sale_schema import (
    SaleCreate,
    SaleUpdate,
    SaleResponse,
    PaymentStatus
)

@pytest.fixture
def sale_create_data():
    return {
        "vehicle_id": "test_vehicle_id",
        "buyer_cpf": "12345678900",
        "sale_price": 50000.0,
        "payment_code": "test_payment_code"
    }

@pytest.fixture
def sale_update_data():
    return {
        "vehicle_id": "new_vehicle_id",
        "buyer_cpf": "98765432100",
        "sale_price": 60000.0,
        "payment_code": "new_payment_code",
        "payment_status": PaymentStatus.PAID
    }

@pytest.fixture
def sale_response_data():
    return {
        "id": str(ObjectId()),
        "vehicle_id": "test_vehicle_id",
        "buyer_cpf": "12345678900",
        "sale_price": 50000.0,
        "payment_code": "test_payment_code",
        "payment_status": PaymentStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

def test_sale_create_validation(sale_create_data):
    sale = SaleCreate(**sale_create_data)
    assert sale.vehicle_id == sale_create_data["vehicle_id"]
    assert sale.buyer_cpf == sale_create_data["buyer_cpf"]
    assert sale.sale_price == sale_create_data["sale_price"]
    assert sale.payment_code == sale_create_data["payment_code"]

def test_sale_create_with_invalid_cpf():
    with pytest.raises(ValueError):
        SaleCreate(
            vehicle_id="test_vehicle_id",
            buyer_cpf="1234567890",  # CPF inválido
            sale_price=50000.0,
            payment_code="test_payment_code"
        )

def test_sale_create_with_negative_price():
    with pytest.raises(ValueError):
        SaleCreate(
            vehicle_id="test_vehicle_id",
            buyer_cpf="12345678900",
            sale_price=-50000.0,
            payment_code="test_payment_code"
        )

def test_sale_create_with_empty_fields():
    with pytest.raises(ValueError):
        SaleCreate(
            vehicle_id="",
            buyer_cpf="12345678900",
            sale_price=50000.0,
            payment_code="test_payment_code"
        )
    
    with pytest.raises(ValueError):
        SaleCreate(
            vehicle_id="test_vehicle_id",
            buyer_cpf="",
            sale_price=50000.0,
            payment_code="test_payment_code"
        )
    
    with pytest.raises(ValueError):
        SaleCreate(
            vehicle_id="test_vehicle_id",
            buyer_cpf="12345678900",
            sale_price=50000.0,
            payment_code=""
        )

def test_sale_update_validation(sale_update_data):
    sale = SaleUpdate(**sale_update_data)
    assert sale.vehicle_id == sale_update_data["vehicle_id"]
    assert sale.buyer_cpf == sale_update_data["buyer_cpf"]
    assert sale.sale_price == sale_update_data["sale_price"]
    assert sale.payment_code == sale_update_data["payment_code"]
    assert sale.payment_status == sale_update_data["payment_status"]

def test_sale_update_with_invalid_status():
    with pytest.raises(ValueError):
        SaleUpdate(
            vehicle_id="test_vehicle_id",
            buyer_cpf="12345678900",
            sale_price=50000.0,
            payment_code="test_payment_code",
            payment_status="INVALID_STATUS"
        )

def test_sale_response_validation(sale_response_data):
    sale = SaleResponse(**sale_response_data)
    assert sale.id == sale_response_data["id"]
    assert sale.vehicle_id == sale_response_data["vehicle_id"]
    assert sale.buyer_cpf == sale_response_data["buyer_cpf"]
    assert sale.sale_price == sale_response_data["sale_price"]
    assert sale.payment_code == sale_response_data["payment_code"]
    assert sale.payment_status == sale_response_data["payment_status"]
    assert sale.created_at == sale_response_data["created_at"]
    assert sale.updated_at == sale_response_data["updated_at"]

def test_sale_response_from_orm(sale_response_data):
    class MockORM:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    orm_obj = MockORM(**sale_response_data)
    sale = SaleResponse.from_orm(orm_obj)
    assert sale.id == sale_response_data["id"]
    assert sale.vehicle_id == sale_response_data["vehicle_id"]
    assert sale.buyer_cpf == sale_response_data["buyer_cpf"]
    assert sale.sale_price == sale_response_data["sale_price"]
    assert sale.payment_code == sale_response_data["payment_code"]
    assert sale.payment_status == sale_response_data["payment_status"]
    assert sale.created_at == sale_response_data["created_at"]
    assert sale.updated_at == sale_response_data["updated_at"]

def test_sale_response_with_mongodb_id():
    class MockORM:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    mongodb_data = {
        "_id": ObjectId(),
        "vehicle_id": "test_vehicle_id",
        "buyer_cpf": "12345678900",
        "sale_price": 50000.0,
        "payment_code": "test_payment_code",
        "payment_status": PaymentStatus.PENDING,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # converte para id string
    mongodb_data["id"] = str(mongodb_data["_id"])
    del mongodb_data["_id"]

    orm_obj = MockORM(**mongodb_data)
    sale = SaleResponse.from_orm(orm_obj)

    assert sale.id == mongodb_data["id"]
    assert "_id" not in sale.dict()