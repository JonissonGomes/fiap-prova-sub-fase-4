import pytest
import pytest_asyncio
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.domain.sale import Sale, PaymentStatus
from app.adapters.mongodb_sale_repository import MongoDBSaleRepository

@pytest_asyncio.fixture
async def mongo_client():
    client = AsyncIOMotorClient("mongodb://sales-mongodb:27017")
    yield client
    await client.drop_database("test_db")

@pytest_asyncio.fixture
async def repository(mongo_client):
    db = mongo_client["test_db"]
    repo = MongoDBSaleRepository(db)
    try:
        yield repo
    finally:
        await db.drop_collection("sales")

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

@pytest.mark.asyncio
async def test_save_sale(repository, mock_sale):
    saved_sale = await repository.save(mock_sale)
    assert saved_sale.vehicle_id == mock_sale.vehicle_id
    assert saved_sale.buyer_cpf == mock_sale.buyer_cpf
    assert saved_sale.sale_price == mock_sale.sale_price
    assert saved_sale.payment_code == mock_sale.payment_code
    assert saved_sale.payment_status == mock_sale.payment_status

@pytest.mark.asyncio
async def test_find_by_id(repository, mock_sale):
    saved_sale = await repository.save(mock_sale)
    found_sale = await repository.find_by_id(saved_sale.id)
    assert found_sale is not None
    assert found_sale.id == saved_sale.id
    assert found_sale.vehicle_id == saved_sale.vehicle_id
    assert found_sale.buyer_cpf == saved_sale.buyer_cpf
    assert found_sale.sale_price == saved_sale.sale_price
    assert found_sale.payment_code == saved_sale.payment_code
    assert found_sale.payment_status == saved_sale.payment_status

@pytest.mark.asyncio
async def test_find_by_id_not_found(repository):
    found_sale = await repository.find_by_id(str(ObjectId()))
    assert found_sale is None

@pytest.mark.asyncio
async def test_find_all(repository, mock_sale):
    await repository.save(mock_sale)
    sales = await repository.find_all()
    assert len(sales) == 1
    assert sales[0].vehicle_id == mock_sale.vehicle_id
    assert sales[0].buyer_cpf == mock_sale.buyer_cpf
    assert sales[0].sale_price == mock_sale.sale_price
    assert sales[0].payment_code == mock_sale.payment_code
    assert sales[0].payment_status == mock_sale.payment_status

@pytest.mark.asyncio
async def test_find_by_status(repository, mock_sale):
    await repository.save(mock_sale)
    sales = await repository.find_by_status(PaymentStatus.PENDING)
    assert len(sales) == 1
    assert sales[0].payment_status == PaymentStatus.PENDING

@pytest.mark.asyncio
async def test_find_by_payment_code(repository, mock_sale):
    await repository.save(mock_sale)
    found_sale = await repository.find_by_payment_code(mock_sale.payment_code)
    assert found_sale is not None
    assert found_sale.payment_code == mock_sale.payment_code

@pytest.mark.asyncio
async def test_find_by_payment_code_not_found(repository):
    found_sale = await repository.find_by_payment_code("non_existent_code")
    assert found_sale is None

@pytest.mark.asyncio
async def test_update_sale(repository, mock_sale):
    saved_sale = await repository.save(mock_sale)
    saved_sale.vehicle_id = "updated_vehicle_id"
    saved_sale.buyer_cpf = "98765432100"
    saved_sale.sale_price = 60000.0
    saved_sale.payment_code = "updated_payment_code"
    saved_sale.payment_status = PaymentStatus.PAID

    updated_sale = await repository.update(saved_sale)
    assert updated_sale is not None
    assert updated_sale.vehicle_id == "updated_vehicle_id"
    assert updated_sale.buyer_cpf == "98765432100"
    assert updated_sale.sale_price == 60000.0
    assert updated_sale.payment_code == "updated_payment_code"
    assert updated_sale.payment_status == PaymentStatus.PAID

@pytest.mark.asyncio
async def test_update_sale_not_found(repository, mock_sale):
    mock_sale.id = str(ObjectId())
    updated_sale = await repository.update(mock_sale)
    assert updated_sale is None

@pytest.mark.asyncio
async def test_delete_sale(repository, mock_sale):
    saved_sale = await repository.save(mock_sale)
    success = await repository.delete(saved_sale.id)
    assert success is True
    found_sale = await repository.find_by_id(saved_sale.id)
    assert found_sale is None

@pytest.mark.asyncio
async def test_delete_sale_not_found(repository):
    success = await repository.delete(str(ObjectId()))
    assert success is False

@pytest.mark.asyncio
async def test_find_by_vehicle_id(repository, mock_sale):
    await repository.save(mock_sale)
    found_sale = await repository.find_by_vehicle_id(mock_sale.vehicle_id)
    assert found_sale is not None
    assert found_sale.vehicle_id == mock_sale.vehicle_id

@pytest.mark.asyncio
async def test_find_by_vehicle_id_not_found(repository):
    found_sale = await repository.find_by_vehicle_id("non_existent_vehicle")
    assert found_sale is None
