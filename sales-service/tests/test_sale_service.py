import pytest
from datetime import datetime
from app.domain.sale import Sale
from app.schemas.sale_schema import PaymentStatus
from app.services.sale_service_impl import SaleServiceImpl
from app.exceptions import SaleNotFoundError
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_sale():
    return Sale(
        id="test_id",
        vehicle_id="test_vehicle_id",
        buyer_cpf="12345678900",
        sale_price=50000.0,
        payment_code="test_payment_code",
        payment_status=PaymentStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def mock_repository():
    mock = AsyncMock()
    mock.find_by_vehicle_id.return_value = None
    mock.save.return_value = None
    mock.find_by_id.return_value = None
    mock.find_all.return_value = []
    mock.find_by_status.return_value = []
    mock.find_by_payment_code.return_value = None
    mock.update.return_value = None
    mock.delete.return_value = True
    return mock

@pytest.fixture
def sale_service(mock_repository):
    return SaleServiceImpl(mock_repository)

@pytest.mark.asyncio
async def test_create_sale(sale_service, mock_sale, mock_repository):
    mock_repository.save.return_value = mock_sale
    result = await sale_service.create_sale(mock_sale)
    assert result == mock_sale
    mock_repository.save.assert_called_once_with(mock_sale)

@pytest.mark.asyncio
async def test_get_sale(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    result = await sale_service.get_sale("test_id")
    assert result == mock_sale
    mock_repository.find_by_id.assert_called_once_with("test_id")

@pytest.mark.asyncio
async def test_get_sale_not_found(sale_service, mock_repository):
    mock_repository.find_by_id.return_value = None
    with pytest.raises(SaleNotFoundError):
        await sale_service.get_sale("nonexistent_id")
    mock_repository.find_by_id.assert_called_once_with("nonexistent_id")

@pytest.mark.asyncio
async def test_get_all_sales(sale_service, mock_sale, mock_repository):
    mock_repository.find_all.return_value = [mock_sale]
    result = await sale_service.get_all_sales()
    assert result == [mock_sale]
    mock_repository.find_all.assert_called_once()

@pytest.mark.asyncio
async def test_get_sales_by_status(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_status.return_value = [mock_sale]
    result = await sale_service.get_sales_by_status(PaymentStatus.PENDING)
    assert result == [mock_sale]
    mock_repository.find_by_status.assert_called_once_with(PaymentStatus.PENDING)

@pytest.mark.asyncio
async def test_get_sale_by_payment_code(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_payment_code.return_value = mock_sale
    result = await sale_service.get_sale_by_payment_code("test_payment_code")
    assert result == mock_sale
    mock_repository.find_by_payment_code.assert_called_once_with("test_payment_code")

@pytest.mark.asyncio
async def test_update_sale(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.find_by_vehicle_id.return_value = None
    mock_repository.update.return_value = mock_sale
    result = await sale_service.update_sale(mock_sale)
    assert result == mock_sale
    mock_repository.update.assert_called_once_with(mock_sale)

@pytest.mark.asyncio
async def test_delete_sale(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.delete.return_value = True
    result = await sale_service.delete_sale("test_id")
    assert result is True
    mock_repository.delete.assert_called_once_with("test_id")

@pytest.mark.asyncio
async def test_update_sale_status(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.update.return_value = mock_sale
    result = await sale_service.update_payment_status("test_id", PaymentStatus.PAID)
    assert result == mock_sale
    mock_repository.update.assert_called_once()

@pytest.mark.asyncio
async def test_mark_sale_as_paid(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.update.return_value = mock_sale
    result = await sale_service.mark_sale_as_paid("test_id")
    assert result == mock_sale
    mock_repository.update.assert_called_once()

@pytest.mark.asyncio
async def test_mark_sale_as_pending(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.update.return_value = mock_sale
    result = await sale_service.mark_sale_as_pending("test_id")
    assert result == mock_sale
    mock_repository.update.assert_called_once()

@pytest.mark.asyncio
async def test_mark_sale_as_canceled(sale_service, mock_sale, mock_repository):
    mock_repository.find_by_id.return_value = mock_sale
    mock_repository.update.return_value = mock_sale
    result = await sale_service.mark_sale_as_canceled("test_id")
    assert result == mock_sale
    mock_repository.update.assert_called_once() 