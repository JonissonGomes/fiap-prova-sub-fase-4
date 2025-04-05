import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, UTC
from unittest.mock import Mock, patch

from app.adapters.api.main import app
from app.adapters.api.dependencies import get_db, get_sale_service
from app.adapters.repository.models import Base, SaleModel
from app.domain.sale import Sale, PaymentStatus
from app.adapters.repository.sqlalchemy_sale_repository import SQLAlchemySaleRepository
from app.adapters.service.sale_service import SaleServiceImpl

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
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
def mock_repository():
    return Mock(spec=SQLAlchemySaleRepository)

@pytest.fixture
def mock_service(mock_repository):
    service = Mock(spec=SaleServiceImpl)
    service.repository = mock_repository
    return service

@pytest.fixture
def client(db_session, mock_service):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    def override_get_sale_service():
        return mock_service
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_sale_service] = override_get_sale_service
    return TestClient(app)

@pytest.fixture
def sale_data():
    return {
        "vehicle_id": 1,
        "buyer_cpf": "12345678900",
        "price": 120000.00,
        "payment_code": "PAY123",
        "payment_status": "PENDING"
    }

@pytest.fixture
def mock_sale():
    return Sale(
        id=1,
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )

@pytest.fixture
def mock_sale_paid():
    return Sale(
        id=1,
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PAID,
        payment_code="PAY123"
    )

def test_create_sale(client, mock_service, sale_data):
    mock_sale = Sale(
        id=1,
        vehicle_id=sale_data["vehicle_id"],
        buyer_cpf=sale_data["buyer_cpf"],
        price=sale_data["price"],
        payment_status=PaymentStatus.PENDING,
        payment_code=sale_data["payment_code"]
    )
    mock_service.create_sale.return_value = mock_sale
    
    response = client.post("/sales/", json=sale_data)
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == sale_data["vehicle_id"]
    assert data["buyer_cpf"] == sale_data["buyer_cpf"]
    assert data["price"] == sale_data["price"]
    assert data["payment_status"] == "pending"
    assert data["payment_code"] == sale_data["payment_code"]

def test_get_sale(client, mock_service, mock_sale):
    mock_service.get_sale.return_value = mock_sale
    
    response = client.get(f"/sales/{mock_sale.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_sale.id
    assert data["vehicle_id"] == mock_sale.vehicle_id
    assert data["buyer_cpf"] == mock_sale.buyer_cpf
    assert data["price"] == mock_sale.price
    assert data["payment_status"] == "pending"
    assert data["payment_code"] == mock_sale.payment_code

def test_get_sales(client, mock_service, mock_sale):
    mock_service.get_all_sales.return_value = [mock_sale]
    
    response = client.get("/sales/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == mock_sale.id
    assert data[0]["vehicle_id"] == mock_sale.vehicle_id
    assert data[0]["buyer_cpf"] == mock_sale.buyer_cpf
    assert data[0]["price"] == mock_sale.price
    assert data[0]["payment_status"] == "pending"
    assert data[0]["payment_code"] == mock_sale.payment_code

def test_get_sale_not_found(client, mock_service):
    mock_service.get_sale.return_value = None
    
    response = client.get("/sales/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Venda não encontrada"

def test_get_sale_by_payment_code(client, mock_service, mock_sale):
    mock_service.get_sale_by_payment_code.return_value = mock_sale
    
    response = client.get("/sales/payment/PAY123")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_sale.id
    assert data["vehicle_id"] == mock_sale.vehicle_id
    assert data["buyer_cpf"] == mock_sale.buyer_cpf
    assert data["price"] == mock_sale.price
    assert data["payment_status"] == "pending"
    assert data["payment_code"] == mock_sale.payment_code

def test_get_sale_by_payment_code_not_found(client, mock_service):
    mock_service.get_sale_by_payment_code.return_value = None
    
    response = client.get("/sales/payment/INVALID")
    assert response.status_code == 404
    assert response.json()["detail"] == "Venda não encontrada"

def test_get_all_sales(client, mock_service, mock_sale):
    mock_service.get_all_sales.return_value = [mock_sale]
    
    response = client.get("/sales/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == mock_sale.id
    assert data[0]["vehicle_id"] == mock_sale.vehicle_id
    assert data[0]["buyer_cpf"] == mock_sale.buyer_cpf
    assert data[0]["price"] == mock_sale.price
    assert data[0]["payment_status"] == "pending"
    assert data[0]["payment_code"] == mock_sale.payment_code

def test_mark_as_paid(client, mock_service, mock_sale):
    mock_service.mark_as_paid.return_value = mock_sale
    
    response = client.put(f"/sales/{mock_sale.id}/paid")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_sale.id
    assert data["vehicle_id"] == mock_sale.vehicle_id
    assert data["buyer_cpf"] == mock_sale.buyer_cpf
    assert data["price"] == mock_sale.price
    assert data["payment_status"] == "pending"
    assert data["payment_code"] == mock_sale.payment_code

def test_mark_as_paid_not_found(client, mock_service):
    mock_service.mark_as_paid.return_value = None
    
    response = client.put("/sales/999/paid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Venda não encontrada"

def test_mark_as_paid_already_paid(client, mock_service, mock_sale_paid):
    mock_service.get_sale.return_value = mock_sale_paid
    mock_service.mark_as_paid.side_effect = ValueError("Venda não está com status pendente")
    
    response = client.put(f"/sales/{mock_sale_paid.id}/paid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Venda não está com status pendente"

def test_update_payment_status(client, mock_service, mock_sale):
    updated_sale = Sale(
        id=mock_sale.id,
        vehicle_id=mock_sale.vehicle_id,
        buyer_cpf=mock_sale.buyer_cpf,
        price=mock_sale.price,
        payment_status=PaymentStatus.PAID,
        payment_code=mock_sale.payment_code
    )
    mock_service.get_sale.return_value = mock_sale
    mock_service.update_sale.return_value = updated_sale
    
    response = client.put(f"/sales/{mock_sale.id}/status", json={"payment_status": "PAID"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_sale.id
    assert data["vehicle_id"] == mock_sale.vehicle_id
    assert data["buyer_cpf"] == mock_sale.buyer_cpf
    assert data["price"] == mock_sale.price
    assert data["payment_status"] == "paid"
    assert data["payment_code"] == mock_sale.payment_code 