from sqlalchemy.orm import Session
from typing import List, Optional
from ...domain.sale import Sale, PaymentStatus
from ...ports.sale_repository import SaleRepository
from .models import SaleModel

class SQLAlchemySaleRepository(SaleRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, sale: Sale) -> Sale:
        sale.validate()
        db_sale = SaleModel(
            vehicle_id=sale.vehicle_id,
            buyer_cpf=sale.buyer_cpf,
            price=sale.price,
            payment_status=sale.payment_status,
            payment_code=sale.payment_code
        )
        self.session.add(db_sale)
        self.session.commit()
        self.session.refresh(db_sale)
        return self._to_domain(db_sale)

    def find_by_id(self, sale_id: int) -> Optional[Sale]:
        db_sale = self.session.query(SaleModel).filter(SaleModel.id == sale_id).first()
        return self._to_domain(db_sale) if db_sale else None

    def find_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        db_sale = self.session.query(SaleModel).filter(SaleModel.payment_code == payment_code).first()
        return self._to_domain(db_sale) if db_sale else None

    def find_all(self) -> List[Sale]:
        db_sales = self.session.query(SaleModel).all()
        return [self._to_domain(sale) for sale in db_sales]

    def find_pending(self) -> List[Sale]:
        db_sales = self.session.query(SaleModel).filter(
            SaleModel.payment_status == PaymentStatus.PENDING
        ).all()
        return [self._to_domain(sale) for sale in db_sales]

    def find_paid(self) -> List[Sale]:
        db_sales = self.session.query(SaleModel).filter(
            SaleModel.payment_status == PaymentStatus.PAID
        ).all()
        return [self._to_domain(sale) for sale in db_sales]

    def update(self, sale: Sale) -> Optional[Sale]:
        db_sale = self.session.query(SaleModel).filter(SaleModel.id == sale.id).first()
        if db_sale:
            for key, value in sale.__dict__.items():
                if key != 'id' and hasattr(db_sale, key):
                    setattr(db_sale, key, value)
            self.session.commit()
            self.session.refresh(db_sale)
            return self._to_domain(db_sale)
        return None

    def _to_domain(self, db_sale: SaleModel) -> Sale:
        return Sale(
            id=db_sale.id,
            vehicle_id=db_sale.vehicle_id,
            buyer_cpf=db_sale.buyer_cpf,
            price=db_sale.price,
            payment_status=db_sale.payment_status,
            payment_code=db_sale.payment_code,
            sale_date=db_sale.sale_date,
            created_at=db_sale.created_at,
            updated_at=db_sale.updated_at
        ) 