from typing import List, Optional
from ...domain.sale import Sale, PaymentStatus
from ...ports.sale_repository import SaleRepository
from ...ports.sale_service import SaleService as SaleServicePort

class SaleServiceImpl(SaleServicePort):
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def create_sale(self, sale: Sale) -> Sale:
        sale.validate()
        return self.repository.save(sale)

    def get_sale(self, sale_id: int) -> Optional[Sale]:
        return self.repository.find_by_id(sale_id)

    def get_sale_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        return self.repository.find_by_payment_code(payment_code)

    def get_all_sales(self) -> List[Sale]:
        return self.repository.find_all()

    def get_pending_sales(self) -> List[Sale]:
        sales = self.repository.find_pending()
        return sales

    def get_paid_sales(self) -> List[Sale]:
        sales = self.repository.find_paid()
        return sales

    def update_sale(self, sale: Sale) -> Optional[Sale]:
        return self.repository.update(sale)

    def mark_as_paid(self, sale_id: int) -> Optional[Sale]:
        sale = self.repository.find_by_id(sale_id)
        if not sale:
            return None
            
        if sale.payment_status == PaymentStatus.PAID:
            raise ValueError("Venda não está com status reservado")
            
        sale.mark_as_paid()
        return self.repository.update(sale)

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