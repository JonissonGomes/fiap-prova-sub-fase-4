from typing import List, Optional
from app.domain.sale import Sale
from app.ports.sale_service import SaleService
from app.ports.sale_repository import SaleRepository
from app.exceptions import SaleNotFoundError
from datetime import datetime
from app.schemas.sale_schema import PaymentStatus

class SaleServiceImpl(SaleService):
    """Implementação do serviço de vendas."""

    def __init__(self, repository: SaleRepository):
        self.repository = repository

    async def create_sale(self, sale: Sale) -> Sale:
        """Cria uma nova venda."""
        try:
            # Salva a venda no repositório
            saved_sale = await self.repository.save(sale)
            return saved_sale
        except Exception as e:
            raise ValueError(f"Erro ao criar venda: {str(e)}")

    async def get_sale(self, sale_id: str) -> Sale:
        """Obtém uma venda pelo ID."""
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)
        return sale

    async def get_sale_by_vehicle_id(self, vehicle_id: str) -> Optional[Sale]:
        """Obtém uma venda pelo ID do veículo."""
        return await self.repository.find_by_vehicle_id(vehicle_id)

    async def get_sale_by_payment_code(self, payment_code: str) -> Sale:
        """Obtém uma venda pelo código de pagamento."""
        sale = await self.repository.find_by_payment_code(payment_code)
        if not sale:
            raise SaleNotFoundError(payment_code)
        return sale

    async def get_all_sales(self) -> List[Sale]:
        """Lista todas as vendas."""
        return await self.repository.find_all()

    async def get_sales_by_status(self, status: PaymentStatus) -> List[Sale]:
        """Lista vendas por status."""
        return await self.repository.find_by_status(status)

    async def update_sale(self, sale: Sale) -> Sale:
        """Atualiza uma venda."""
        updated_sale = await self.repository.update(sale)
        if not updated_sale:
            raise SaleNotFoundError(sale.id)
        return updated_sale

    async def delete_sale(self, sale_id: str) -> bool:
        """Remove uma venda."""
        success = await self.repository.delete(sale_id)
        if not success:
            raise SaleNotFoundError(sale_id)
        return success

    async def update_payment_status(self, sale_id: str, status: PaymentStatus) -> Sale:
        """Atualiza o status de pagamento de uma venda."""
        sale = await self.get_sale(sale_id)
        sale.payment_status = status
        return await self.update_sale(sale) 