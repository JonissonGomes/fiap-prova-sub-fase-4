import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.adapters.api.main import app
from app.adapters.api.dependencies import get_db
from app.adapters.repository.models import Base, VehicleModel
from app.domain.vehicle import Vehicle, VehicleStatus

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
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

async def test_create_vehicle(client):
    response = await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )
    assert response.status_code == 200
    assert response.json()["brand"] == "Toyota"
    assert response.json()["model"] == "Corolla"
    assert response.json()["year"] == 2022
    assert response.json()["color"] == "Prata"
    assert response.json()["price"] == 100000.0
    assert response.json()["status"] == "AVAILABLE"

async def test_get_vehicle(client):
    # Primeiro, criar um veículo
    create_response = await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )
    assert create_response.status_code == 200
    vehicle_id = create_response.json()["id"]

    # Depois, buscar o veículo
    response = await client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["brand"] == "Toyota"
    assert response.json()["model"] == "Corolla"
    assert response.json()["year"] == 2022
    assert response.json()["color"] == "Prata"
    assert response.json()["price"] == 100000.0
    assert response.json()["status"] == "AVAILABLE"

async def test_get_vehicles(client):
    # Primeiro, criar um veículo
    await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )

    # Depois, buscar todos os veículos
    response = await client.get("/vehicles/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["brand"] == "Toyota"
    assert response.json()[0]["model"] == "Corolla"
    assert response.json()[0]["year"] == 2022
    assert response.json()[0]["color"] == "Prata"
    assert response.json()[0]["price"] == 100000.0
    assert response.json()[0]["status"] == "AVAILABLE"

async def test_get_available_vehicles(client):
    # Primeiro, criar um veículo disponível
    await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )

    # Depois, buscar veículos disponíveis
    response = await client.get("/vehicles/available")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "AVAILABLE"

async def test_update_vehicle(client):
    # Primeiro, criar um veículo
    create_response = await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )
    assert create_response.status_code == 200
    vehicle_id = create_response.json()["id"]

    # Depois, atualizar o veículo
    response = await client.put(
        f"/vehicles/{vehicle_id}",
        json={
            "brand": "Honda",
            "model": "Civic",
            "year": 2023,
            "color": "Preto",
            "price": 110000.0,
            "status": "AVAILABLE"
        }
    )
    assert response.status_code == 200
    assert response.json()["brand"] == "Honda"
    assert response.json()["model"] == "Civic"
    assert response.json()["year"] == 2023
    assert response.json()["color"] == "Preto"
    assert response.json()["price"] == 110000.0
    assert response.json()["status"] == "AVAILABLE"

async def test_delete_vehicle(client):
    # Primeiro, criar um veículo
    create_response = await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )
    assert create_response.status_code == 200
    vehicle_id = create_response.json()["id"]

    # Depois, deletar o veículo
    response = await client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Veículo removido com sucesso"

    # Verificar se o veículo foi realmente deletado
    get_response = await client.get(f"/vehicles/{vehicle_id}")
    assert get_response.status_code == 404

async def test_mark_vehicle_as_sold(client):
    # Primeiro, criar um veículo
    create_response = await client.post(
        "/vehicles/",
        json={
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "color": "Prata",
            "price": 100000.0,
            "status": "AVAILABLE"
        }
    )
    assert create_response.status_code == 200
    vehicle_id = create_response.json()["id"]

    # Depois, marcar o veículo como vendido
    response = await client.post(f"/vehicles/{vehicle_id}/mark-as-sold")
    assert response.status_code == 200
    assert response.json()["status"] == "SOLD"

    # Tentar marcar como vendido novamente deve falhar
    response = await client.post(f"/vehicles/{vehicle_id}/mark-as-sold")
    assert response.status_code == 400
    assert response.json()["detail"] == "Veículo já está vendido" 