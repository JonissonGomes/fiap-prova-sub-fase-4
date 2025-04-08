"""
Implementação do repositório de vendas
"""
from sqlalchemy.orm import Session
from app.ports.sale_repository import SaleRepositoryPort
from app.domain.sale import Sale
from app.adapters.database.models import Sale as SaleModel

class SaleRepository(SaleRepositoryPort):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, sale: Sale) -> Sale:
        db_sale = SaleModel(**sale.model_dump())
        self.db.add(db_sale)
        self.db.commit()
        self.db.refresh(db_sale)
        return Sale.model_validate(db_sale)
    
    def get_by_id(self, sale_id: int) -> Sale:
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return None
        return Sale.model_validate(db_sale)
    
    def get_by_payment_id(self, payment_id: str) -> Sale:
        db_sale = self.db.query(SaleModel).filter(SaleModel.payment_id == payment_id).first()
        if not db_sale:
            return None
        return Sale.model_validate(db_sale)
    
    def update(self, sale: Sale) -> Sale:
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale.id).first()
        if not db_sale:
            return None
        
        for key, value in sale.model_dump().items():
            setattr(db_sale, key, value)
        
        self.db.commit()
        self.db.refresh(db_sale)
        return Sale.model_validate(db_sale)
    
    def list_by_status(self, status: str) -> list[Sale]:
        db_sales = self.db.query(SaleModel).filter(SaleModel.status == status).all()
        return [Sale.model_validate(sale) for sale in db_sales] 