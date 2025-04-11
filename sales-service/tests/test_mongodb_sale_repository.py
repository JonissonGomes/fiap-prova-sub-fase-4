import pytest
import pytest_asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.domain.sale import Sale
from app.schemas.sale_schema import PaymentStatus
from app.adapters.mongodb_sale_repository import MongoDBSaleRepository
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId

@pytest.fixture
def mock_sale():
    sale_id = ObjectId()
    return Sale(
        id=str(sale_id),
        vehicle_id="test_vehicle_id",
        buyer_cpf="12345678900",
        sale_price=50000.0,
        payment_code="test_payment_code",
        payment_status=PaymentStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def mock_collection():
    mock = AsyncMock()
    mock.find_one.return_value = None
    mock.find.return_value = AsyncMock()
    mock.find.return_value.to_list.return_value = []
    mock.insert_one.return_value = AsyncMock()
    mock.insert_one.return_value.inserted_id = ObjectId()
    mock.update_one.return_value = AsyncMock()
    mock.update_one.return_value.modified_count = 1
    mock.delete_one.return_value = AsyncMock()
    mock.delete_one.return_value.deleted_count = 1
    return mock

@pytest.fixture
def mock_db(mock_collection):
    db = MagicMock()
    db.__getitem__.return_value = mock_collection
    return db

@pytest.fixture
def mock_motor_client(mock_db):
    client = MagicMock()
    client.__getitem__.return_value = mock_db
    return client

@pytest_asyncio.fixture
async def repository(mock_db):
    repo = MongoDBSaleRepository(mock_db)
    return repo

@pytest.mark.asyncio
async def test_save(repository, mock_sale, mock_collection):
    mock_collection.insert_one.return_value.inserted_id = ObjectId()
    result = await repository.save(mock_sale)
    assert result == mock_sale
    mock_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_find_by_id(repository, mock_sale, mock_collection):
    sale_id = ObjectId()
    mock_collection.find_one.return_value = mock_sale.dict()
    result = await repository.find_by_id(str(sale_id))
    assert result == mock_sale
    mock_collection.find_one.assert_called_once_with({"_id": sale_id})

@pytest.mark.asyncio
async def test_find_by_id_not_found(repository, mock_collection):
    sale_id = ObjectId()
    mock_collection.find_one.return_value = None
    result = await repository.find_by_id(str(sale_id))
    assert result is None
    mock_collection.find_one.assert_called_once_with({"_id": sale_id})

@pytest.mark.asyncio
async def test_find_all(repository, mock_sale, mock_collection):
    mock_collection.find.return_value.to_list.return_value = [mock_sale.dict()]
    result = await repository.find_all()
    assert len(result) == 1
    assert result[0] == mock_sale
    mock_collection.find.assert_called_once()

@pytest.mark.asyncio
async def test_find_by_status(repository, mock_sale, mock_collection):
    mock_collection.find.return_value.to_list.return_value = [mock_sale.dict()]
    result = await repository.find_by_status(PaymentStatus.PENDING)
    assert len(result) == 1
    assert result[0] == mock_sale
    mock_collection.find.assert_called_once_with({"payment_status": "PENDENTE"})

@pytest.mark.asyncio
async def test_find_by_payment_code(repository, mock_sale, mock_collection):
    mock_collection.find_one.return_value = mock_sale.dict()
    result = await repository.find_by_payment_code("test_payment_code")
    assert result == mock_sale
    mock_collection.find_one.assert_called_once_with({"payment_code": "test_payment_code"})

@pytest.mark.asyncio
async def test_find_by_vehicle_id(repository, mock_sale, mock_collection):
    mock_collection.find_one.return_value = mock_sale.dict()
    result = await repository.find_by_vehicle_id("test_vehicle_id")
    assert result == mock_sale
    mock_collection.find_one.assert_called_once_with({"vehicle_id": "test_vehicle_id"})

@pytest.mark.asyncio
async def test_update(repository, mock_sale, mock_collection):
    mock_collection.update_one.return_value.modified_count = 1
    mock_collection.find_one.return_value = mock_sale.dict()
    result = await repository.update(mock_sale)
    assert result == mock_sale
    mock_collection.update_one.assert_called_once()

@pytest.mark.asyncio
async def test_delete(repository, mock_collection):
    sale_id = ObjectId()
    mock_collection.delete_one.return_value = AsyncMock()
    mock_collection.delete_one.return_value.deleted_count = 1
    result = await repository.delete(str(sale_id))
    assert result is True
    mock_collection.delete_one.assert_called_once_with({"_id": sale_id})
