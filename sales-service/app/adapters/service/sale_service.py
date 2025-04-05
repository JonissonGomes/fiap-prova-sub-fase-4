from typing import List, Optional
from ...domain.sale import Sale
from ...ports.sale_repository import SaleRepository
from ...ports.sale_service import SaleService as SaleServicePort

class SaleService(SaleServicePort):
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def create_sale(self, sale: Sale) -> Sale:
        sale.validate()
        return self.repository.save(sale)

    def get_sale(self, sale_id: int) -> Optional[Sale]:
        return self.repository.find_by_id(sale_id)

    def get_sales(self) -> List[Sale]:
        return self.repository.find_all()

    def get_pending_sales(self) -> List[Sale]:
        return self.repository.find_pending()

    def get_paid_sales(self) -> List[Sale]:
        return self.repository.find_paid()

    def update_payment_status(self, payment_code: str, status: str) -> Optional[Sale]:
        sale = self.repository.find_by_payment_code(payment_code)
        if not sale:
            return None
            
        if status == "paid":
            sale.mark_as_paid()
        elif status == "cancelled":
            sale.mark_as_cancelled()
        else:
            raise ValueError("Status de pagamento inválido")
            
        return self.repository.update(sale) 