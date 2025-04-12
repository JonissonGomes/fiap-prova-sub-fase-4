import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from datetime import datetime
from bson import ObjectId
from app.controllers.sale_controller import router, get_service
from app.domain.sale import Sale, PaymentStatus
from app.schemas.sale_schema import SaleCreate, SaleUpdate, SaleResponse
from app.exceptions import SaleNotFoundError, InvalidSaleDataError

@pytest.fixture
def mock_sale_service():
    return AsyncMock()

@pytest.fixture
def app(mock_sale_service):
    app = FastAPI()
    
    async def override_get_service():
        return mock_sale_service
    
    app.dependency_overrides[get_service] = override_get_service
    app.include_router(router)
    return app

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_sale_error(client, mock_sale_service):
    mock_sale_service.create_sale.side_effect = Exception("Erro ao criar venda")
    
    response = await client.post(
        "/sales",
        json={
            "vehicle_id": "test_vehicle_id",
            "buyer_cpf": "12345678900",
            "sale_price": 50000.0,
            "payment_code": "test_payment_code"
        }
    )
    
    assert response.status_code == 500

@pytest.mark.asyncio
async def test_get_sale_error(client, mock_sale_service):
    mock_sale_service.get_sale.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.get(f"/sales/{str(ObjectId())}")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_sales_error(client, mock_sale_service):
    mock_sale_service.get_all_sales.side_effect = Exception("Erro ao listar vendas")
    
    response = await client.get("/sales")
    
    assert response.status_code == 500
    assert "Erro ao listar vendas" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_sales_by_status_error(client, mock_sale_service):
    mock_sale_service.get_sales_by_status.side_effect = Exception("Erro ao listar vendas por status")
    
    response = await client.get("/sales/status/PENDENTE")
    
    assert response.status_code == 500
    assert "Erro ao listar vendas por status" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_sale_by_payment_code_error(client, mock_sale_service):
    mock_sale_service.get_sale_by_payment_code.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.get("/sales/payment/test_payment_code")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_delete_sale_error(client, mock_sale_service):
    mock_sale_service.delete_sale.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.delete(f"/sales/{str(ObjectId())}")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_mark_sale_as_canceled_error(client, mock_sale_service):
    mock_sale_service.update_payment_status.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.patch(f"/sales/{str(ObjectId())}/mark-as-canceled")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_mark_sale_as_pending_error(client, mock_sale_service):
    mock_sale_service.update_payment_status.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.patch(f"/sales/{str(ObjectId())}/mark-as-pending")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_mark_sale_as_paid_error(client, mock_sale_service):
    mock_sale_service.update_payment_status.side_effect = SaleNotFoundError("Venda não encontrada")
    
    response = await client.patch(f"/sales/{str(ObjectId())}/mark-as-paid")
    
    assert response.status_code == 404
    assert "Venda não encontrada" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_sale_invalid_data(client):
    response = await client.post(
        "/sales",
        json={
            "vehicle_id": "",  # ID vazio
            "buyer_cpf": "123",  # CPF inválido
            "sale_price": -100.0,  # Preço negativo
            "payment_code": ""  # Código vazio
        }
    )
    
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_update_sale_invalid_data(client):
    response = await client.put(
        f"/sales/{str(ObjectId())}",
        json={
            "sale_price": -100.0  # Preço negativo
        }
    )
    
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_get_sale_invalid_id(client):
    response = await client.get("/sales/invalid_id")
    
    assert response.status_code == 400
    assert "ID inválido" in response.json()["detail"] 