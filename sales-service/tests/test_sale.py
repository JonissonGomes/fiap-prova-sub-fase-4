import pytest
from app.schemas.sale_schema import SaleCreate, PaymentStatus

def test_create_sale():
    sale = SaleCreate(
        vehicle_id="test_vehicle_id",
        buyer_cpf="12345678900",
        sale_price=50000.0,
        payment_code="test_payment_code"
    )
    assert sale.payment_status == PaymentStatus.PENDING