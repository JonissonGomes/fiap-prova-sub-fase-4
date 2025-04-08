from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.sale import Sale

class SaleRepository(ABC):
    @abstractmethod
    def save(self, sale: Sale) -> Sale:
        pass

    @abstractmethod
    def find_by_id(self, sale_id: int) -> Optional[Sale]:
        pass

    @abstractmethod
    def find_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        pass

    @abstractmethod
    def find_all(self) -> List[Sale]:
        pass

    @abstractmethod
    def find_pending(self) -> List[Sale]:
        pass

    @abstractmethod
    def find_paid(self) -> List[Sale]:
        pass

    @abstractmethod
    def update(self, sale: Sale) -> Sale:
        pass 