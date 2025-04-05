import pytest
from datetime import datetime, UTC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.domain.sale import Sale, PaymentStatus
from app.adapters.repository.sqlalchemy_sale_repository import SQLAlchemySaleRepository
from app.adapters.repository.models import Base, SaleModel

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
def repository(db_session):
    return SQLAlchemySaleRepository(db_session)

def test_save_sale(repository):
    # Setup
    sale = Sale(
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )

    # Execute
    result = repository.save(sale)

    # Assert
    assert result.id is not None
    assert result.vehicle_id == 1
    assert result.buyer_cpf == "12345678900"
    assert result.price == 120000.00
    assert result.payment_status == PaymentStatus.PENDING
    assert result.payment_code == "PAY123"

def test_find_by_id(repository):
    # Setup
    sale = Sale(
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )
    saved_sale = repository.save(sale)

    # Execute
    result = repository.find_by_id(saved_sale.id)

    # Assert
    assert result is not None
    assert result.id == saved_sale.id
    assert result.vehicle_id == 1
    assert result.buyer_cpf == "12345678900"
    assert result.price == 120000.00
    assert result.payment_status == PaymentStatus.PENDING
    assert result.payment_code == "PAY123"

def test_find_by_id_not_found(repository):
    # Execute
    result = repository.find_by_id(999)

    # Assert
    assert result is None

def test_find_by_payment_code(repository):
    # Setup
    sale = Sale(
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )
    repository.save(sale)

    # Execute
    result = repository.find_by_payment_code("PAY123")

    # Assert
    assert result is not None
    assert result.vehicle_id == 1
    assert result.buyer_cpf == "12345678900"
    assert result.price == 120000.00
    assert result.payment_status == PaymentStatus.PENDING
    assert result.payment_code == "PAY123"

def test_find_by_payment_code_not_found(repository):
    # Execute
    result = repository.find_by_payment_code("INVALID")

    # Assert
    assert result is None

def test_find_all(repository):
    # Setup
    sales = [
        Sale(
            vehicle_id=1,
            buyer_cpf="12345678900",
            price=120000.00,
            payment_status=PaymentStatus.PENDING,
            payment_code="PAY123"
        ),
        Sale(
            vehicle_id=2,
            buyer_cpf="98765432100",
            price=110000.00,
            payment_status=PaymentStatus.PAID,
            payment_code="PAY456"
        )
    ]
    for sale in sales:
        repository.save(sale)

    # Execute
    result = repository.find_all()

    # Assert
    assert len(result) == 2
    assert result[0].vehicle_id == 1
    assert result[0].buyer_cpf == "12345678900"
    assert result[0].price == 120000.00
    assert result[0].payment_status == PaymentStatus.PENDING
    assert result[0].payment_code == "PAY123"
    assert result[1].vehicle_id == 2
    assert result[1].buyer_cpf == "98765432100"
    assert result[1].price == 110000.00
    assert result[1].payment_status == PaymentStatus.PAID
    assert result[1].payment_code == "PAY456"

def test_find_pending(repository):
    # Setup
    sales = [
        Sale(
            vehicle_id=1,
            buyer_cpf="12345678900",
            price=120000.00,
            payment_status=PaymentStatus.PENDING,
            payment_code="PAY123"
        ),
        Sale(
            vehicle_id=2,
            buyer_cpf="98765432100",
            price=110000.00,
            payment_status=PaymentStatus.PAID,
            payment_code="PAY456"
        )
    ]
    for sale in sales:
        repository.save(sale)

    # Execute
    result = repository.find_pending()

    # Assert
    assert len(result) == 1
    assert result[0].vehicle_id == 1
    assert result[0].buyer_cpf == "12345678900"
    assert result[0].price == 120000.00
    assert result[0].payment_status == PaymentStatus.PENDING
    assert result[0].payment_code == "PAY123"

def test_find_paid(repository):
    # Setup
    sales = [
        Sale(
            vehicle_id=1,
            buyer_cpf="12345678900",
            price=120000.00,
            payment_status=PaymentStatus.PENDING,
            payment_code="PAY123"
        ),
        Sale(
            vehicle_id=2,
            buyer_cpf="98765432100",
            price=110000.00,
            payment_status=PaymentStatus.PAID,
            payment_code="PAY456"
        )
    ]
    for sale in sales:
        repository.save(sale)

    # Execute
    result = repository.find_paid()

    # Assert
    assert len(result) == 1
    assert result[0].vehicle_id == 2
    assert result[0].buyer_cpf == "98765432100"
    assert result[0].price == 110000.00
    assert result[0].payment_status == PaymentStatus.PAID
    assert result[0].payment_code == "PAY456"

def test_update(repository):
    # Setup
    sale = Sale(
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )
    saved_sale = repository.save(sale)
    saved_sale.price = 130000.00
    saved_sale.payment_status = PaymentStatus.PAID

    # Execute
    result = repository.update(saved_sale)

    # Assert
    assert result is not None
    assert result.id == saved_sale.id
    assert result.vehicle_id == 1
    assert result.buyer_cpf == "12345678900"
    assert result.price == 130000.00
    assert result.payment_status == PaymentStatus.PAID
    assert result.payment_code == "PAY123"

def test_update_not_found(repository):
    # Setup
    sale = Sale(
        id=999,
        vehicle_id=1,
        buyer_cpf="12345678900",
        price=120000.00,
        payment_status=PaymentStatus.PENDING,
        payment_code="PAY123"
    )

    # Execute
    result = repository.update(sale)

    # Assert
    assert result is None 