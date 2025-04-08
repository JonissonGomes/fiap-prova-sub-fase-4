from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.sale import Sale

class SaleService(ABC):
    @abstractmethod
    def create_sale(self, sale: Sale) -> Sale:
        pass

    @abstractmethod
    def get_sale(self, sale_id: int) -> Optional[Sale]:
        pass

    @abstractmethod
    def get_sale_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        pass

    @abstractmethod
    def get_all_sales(self) -> List[Sale]:
        pass

    @abstractmethod
    def get_pending_sales(self) -> List[Sale]:
        pass

    @abstractmethod
    def get_paid_sales(self) -> List[Sale]:
        pass

    @abstractmethod
    def update_sale(self, sale: Sale) -> Optional[Sale]:
        pass

    @abstractmethod
    def mark_as_paid(self, sale_id: int) -> Optional[Sale]:
        pass

    @abstractmethod
    def update_payment_status(self, payment_code: str, status: str) -> Optional[Sale]:
        pass 