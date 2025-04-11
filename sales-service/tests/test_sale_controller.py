import pytest
import pytest_asyncio
from datetime import datetime
from fastapi import FastAPI
from httpx import AsyncClient
from bson import ObjectId
from app.controllers.sale_controller import router, get_service
from app.domain.sale import Sale, PaymentStatus
from app.schemas.sale_schema import SaleCreate, SaleUpdate, SaleResponse
from app.exceptions import SaleNotFoundError

valid_id = str(ObjectId())

@pytest.fixture
def app(mock_sale_service):
    app = FastAPI()

    async def override_get_service():
        return mock_sale_service

    app.dependency_overrides[get_service] = override_get_service
    app.include_router(router)
    return app

@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_sale():
    return Sale(
        id=str(ObjectId()),
        vehicle_id="test_vehicle_id",
        buyer_cpf="12345678900",
        sale_price=50000.0,
        payment_code="test_payment_code",
        payment_status=PaymentStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def mock_sale_service():
    class MockSaleService:
        async def create_sale(self, sale: Sale) -> Sale:
            return Sale(
                id=str(ObjectId()),
                vehicle_id=sale.vehicle_id,
                buyer_cpf=sale.buyer_cpf,
                sale_price=sale.sale_price,
                payment_code=sale.payment_code,
                payment_status=PaymentStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        async def get_sale(self, sale_id: str) -> Sale:
            return Sale(
                id=sale_id,
                vehicle_id="test_vehicle_id",
                buyer_cpf="12345678900",
                sale_price=50000.0,
                payment_code="test_payment_code",
                payment_status=PaymentStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        async def get_all_sales(self) -> list[Sale]:
            return [
                Sale(
                    id=str(ObjectId()),
                    vehicle_id="test_vehicle_id",
                    buyer_cpf="12345678900",
                    sale_price=50000.0,
                    payment_code="test_payment_code",
                    payment_status=PaymentStatus.PENDING,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            ]

        async def update_sale(self, sale: Sale) -> Sale:
            return sale

        async def delete_sale(self, sale_id: str) -> bool:
            return True

        async def get_sales_by_status(self, status: PaymentStatus) -> list[Sale]:
            return [
                Sale(
                    id=str(ObjectId()),
                    vehicle_id="test_vehicle_id",
                    buyer_cpf="12345678900",
                    sale_price=50000.0,
                    payment_code="test_payment_code",
                    payment_status=status,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            ]

        async def get_sale_by_payment_code(self, payment_code: str) -> Sale:
            return Sale(
                id=str(ObjectId()),
                vehicle_id="test_vehicle_id",
                buyer_cpf="12345678900",
                sale_price=50000.0,
                payment_code=payment_code,
                payment_status=PaymentStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        async def update_payment_status(self, sale_id: str, status: PaymentStatus) -> Sale:
            return Sale(
                id=sale_id,
                vehicle_id="test_vehicle_id",
                buyer_cpf="12345678900",
                sale_price=50000.0,
                payment_code="test_payment_code",
                payment_status=status,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

    return MockSaleService()

@pytest.mark.asyncio
async def test_create_sale(client):
    response = await client.post(
        "/sales",
        json={
            "vehicle_id": "test_vehicle_id",
            "buyer_cpf": "12345678900",
            "sale_price": 50000.0,
            "payment_code": "test_payment_code"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == "test_vehicle_id"
    assert data["buyer_cpf"] == "12345678900"
    assert data["sale_price"] == 50000.0
    assert data["payment_code"] == "test_payment_code"
    assert data["payment_status"] == "PENDENTE"

@pytest.mark.asyncio
async def test_get_sale_success(client):
    response = await client.get(f"/sales/{valid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == valid_id
    assert data["vehicle_id"] == "test_vehicle_id"
    assert data["buyer_cpf"] == "12345678900"
    assert data["sale_price"] == 50000.0
    assert data["payment_code"] == "test_payment_code"
    assert data["payment_status"] == "PENDENTE"

@pytest.mark.asyncio
async def test_get_all_sales(client):
    response = await client.get("/sales")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["vehicle_id"] == "test_vehicle_id"
    assert data[0]["buyer_cpf"] == "12345678900"
    assert data[0]["sale_price"] == 50000.0
    assert data[0]["payment_code"] == "test_payment_code"
    assert data[0]["payment_status"] == "PENDENTE"

@pytest.mark.asyncio
async def test_get_sales_by_status(client):
    response = await client.get("/sales/status/PENDENTE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["payment_status"] == "PENDENTE"

@pytest.mark.asyncio
async def test_get_sale_by_payment_code(client):
    response = await client.get("/sales/payment/test_payment_code")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_code"] == "test_payment_code"

@pytest.mark.asyncio
async def test_update_sale_success(client):
    valid_id = str(ObjectId())
    response = await client.put(
        f"/sales/{valid_id}",
        json={
            "vehicle_id": "valid_vehicle_id",
            "buyer_cpf": "98765432100",
            "sale_price": 60000.0,
            "payment_code": "updated_payment_code",
            "payment_status": "PAGO"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == "valid_vehicle_id"
    assert data["buyer_cpf"] == "98765432100"
    assert data["sale_price"] == 60000.0
    assert data["payment_code"] == "updated_payment_code"
    assert data["payment_status"] == "PAGO"

@pytest.mark.asyncio
async def test_delete_sale(client):
    response = await client.delete("/sales/test_id")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Venda removida com sucesso"

@pytest.mark.asyncio
async def test_mark_sale_as_canceled(client):
    response = await client.patch("/sales/test_id/mark-as-canceled")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_status"] == "CANCELADA"

@pytest.mark.asyncio
async def test_mark_sale_as_pending(client):
    response = await client.patch("/sales/test_id/mark-as-pending")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_status"] == "PENDENTE"

@pytest.mark.asyncio
async def test_mark_sale_as_paid(client):
    response = await client.patch("/sales/test_id/mark-as-paid")
    assert response.status_code == 200
    data = response.json()
    assert data["payment_status"] == "PAGO"

@pytest.mark.asyncio
async def test_get_sale_not_found(client):
    response = await client.get("/sales/non_existent_id")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "ID inválido"

@pytest.mark.asyncio
async def test_update_sale_not_found(client):
    response = await client.put(
        "/sales/non_existent_id",
        json={
            "vehicle_id": "updated_vehicle_id",
            "buyer_cpf": "98765432100",
            "sale_price": 60000.0,
            "payment_code": "updated_payment_code",
            "payment_status": "PAGO"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "ID inválido"

@pytest.mark.asyncio
async def test_delete_sale_not_found(app):
    class FailingMockSaleService:
        async def delete_sale(self, sale_id: str) -> bool:
            raise SaleNotFoundError("ID inválido")

    async def override_get_service():
        return FailingMockSaleService()

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/sales/non_existent_id")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Venda com ID ID inválido não encontrada"

@pytest.mark.asyncio
async def test_get_sale_by_payment_code_not_found(app):
    class FailingMockSaleService:
        async def get_sale_by_payment_code(self, payment_code: str):
            raise SaleNotFoundError("ID inválido")

    async def override_get_service():
        return FailingMockSaleService()

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/sales/payment/non_existent_code")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Venda com ID ID inválido não encontrada"


@pytest.mark.asyncio
async def test_mark_sale_as_canceled_not_found(app):
    class FailingMockSaleService:
        async def update_payment_status(self, sale_id: str, status: PaymentStatus):
            raise SaleNotFoundError("ID inválido")

    async def override_get_service():
        return FailingMockSaleService()

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch("/sales/non_existent_id/mark-as-canceled")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Venda com ID ID inválido não encontrada"


@pytest.mark.asyncio
async def test_mark_sale_as_pending_not_found(app):
    class FailingMockSaleService:
        async def update_payment_status(self, sale_id: str, status: PaymentStatus):
            raise SaleNotFoundError("ID inválido")

    async def override_get_service():
        return FailingMockSaleService()

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch("/sales/non_existent_id/mark-as-pending")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Venda com ID ID inválido não encontrada"


@pytest.mark.asyncio
async def test_mark_sale_as_paid_not_found(app):
    class FailingMockSaleService:
        async def update_payment_status(self, sale_id: str, status: PaymentStatus):
            raise SaleNotFoundError("ID inválido")

    async def override_get_service():
        return FailingMockSaleService()

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch("/sales/non_existent_id/mark-as-paid")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Venda com ID ID inválido não encontrada"

@pytest.mark.asyncio
async def test_create_sale_invalid_data(client):
    response = await client.post(
        "/sales",
        json={
            "vehicle_id": "",  # Campo vazio
            "buyer_cpf": "123",  # CPF inválido
            "sale_price": -100,  # Preço negativo
            "payment_code": ""  # Código vazio
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_update_sale_invalid_data(client):
    response = await client.put(
        "/sales/test_id",
        json={
            "vehicle_id": "",  # Campo vazio
            "buyer_cpf": "123",  # CPF inválido
            "sale_price": -100,  # Preço negativo
            "payment_code": "",  # Código vazio
            "payment_status": "INVALID_STATUS"  # Status inválido
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data 