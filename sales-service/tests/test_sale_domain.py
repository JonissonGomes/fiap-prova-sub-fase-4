import pytest
from datetime import datetime
from bson import ObjectId
from app.domain.sale import Sale
from app.schemas.sale_schema import PaymentStatus

@pytest.fixture
def sale_data():
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

@pytest.fixture
def sale(sale_data):
    return Sale(**sale_data)

def test_sale_creation(sale, sale_data):
    assert sale.id == sale_data["id"]
    assert sale.vehicle_id == sale_data["vehicle_id"]
    assert sale.buyer_cpf == sale_data["buyer_cpf"]
    assert sale.sale_price == sale_data["sale_price"]
    assert sale.payment_code == sale_data["payment_code"]
    assert sale.payment_status == sale_data["payment_status"]
    assert sale.created_at == sale_data["created_at"]
    assert sale.updated_at == sale_data["updated_at"]

def test_sale_creation_with_defaults():
    sale = Sale(
        vehicle_id="test_vehicle_id",
        buyer_cpf="12345678900",
        sale_price=50000.0,
        payment_code="test_payment_code"
    )
    assert sale.id is None
    assert sale.vehicle_id == "test_vehicle_id"
    assert sale.buyer_cpf == "12345678900"
    assert sale.sale_price == 50000.0
    assert sale.payment_code == "test_payment_code"
    assert sale.payment_status == PaymentStatus.PENDING
    assert sale.created_at is not None
    assert sale.updated_at is not None

def test_sale_update(sale):
    new_data = {
        "vehicle_id": "new_vehicle_id",
        "buyer_cpf": "98765432100",
        "sale_price": 60000.0,
        "payment_code": "new_payment_code",
        "payment_status": PaymentStatus.PAID
    }
    sale.update(**new_data)
    assert sale.vehicle_id == new_data["vehicle_id"]
    assert sale.buyer_cpf == new_data["buyer_cpf"]
    assert sale.sale_price == new_data["sale_price"]
    assert sale.payment_code == new_data["payment_code"]
    assert sale.payment_status == new_data["payment_status"]
    assert sale.updated_at > sale.created_at

def test_sale_to_dict(sale, sale_data):
    sale_dict = sale.to_dict()
    assert sale_dict["id"] == sale_data["id"]
    assert sale_dict["vehicle_id"] == sale_data["vehicle_id"]
    assert sale_dict["buyer_cpf"] == sale_data["buyer_cpf"]
    assert sale_dict["sale_price"] == sale_data["sale_price"]
    assert sale_dict["payment_code"] == sale_data["payment_code"]
    assert sale_dict["payment_status"] == sale_data["payment_status"]
    assert sale_dict["created_at"] == sale_data["created_at"]
    assert sale_dict["updated_at"] == sale_data["updated_at"]

def test_sale_from_dict(sale_data):
    sale = Sale.from_dict(sale_data)
    assert sale.id == sale_data["id"]
    assert sale.vehicle_id == sale_data["vehicle_id"]
    assert sale.buyer_cpf == sale_data["buyer_cpf"]
    assert sale.sale_price == sale_data["sale_price"]
    assert sale.payment_code == sale_data["payment_code"]
    assert sale.payment_status == sale_data["payment_status"]
    assert sale.created_at == sale_data["created_at"]
    assert sale.updated_at == sale_data["updated_at"]

