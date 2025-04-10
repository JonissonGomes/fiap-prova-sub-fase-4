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
        # Verifica se já existe uma venda para o veículo
        existing_sale = await self.repository.find_by_vehicle_id(sale.vehicle_id)
        if existing_sale:
            raise ValueError(f"Já existe uma venda para o veículo {sale.vehicle_id}")

        return await self.repository.save(sale)

    async def get_sale(self, sale_id: str) -> Sale:
        """Obtém uma venda pelo ID."""
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)
        return sale

    async def get_sale_by_vehicle_id(self, vehicle_id: str) -> Optional[Sale]:
        """Obtém uma venda pelo ID do veículo."""
        return await self.repository.find_by_vehicle_id(vehicle_id)

    async def get_all_sales(self) -> List[Sale]:
        """Lista todas as vendas."""
        return await self.repository.find_all()

    async def get_sales_by_status(self, status: PaymentStatus) -> List[Sale]:
        """Lista vendas por status."""
        return await self.repository.find_by_status(status)

    async def update_sale(self, sale: Sale) -> Sale:
        """Atualiza uma venda."""
        existing_sale = await self.repository.find_by_id(sale.id)
        if not existing_sale:
            raise SaleNotFoundError(sale.id)

        # Se o veículo mudou, verifica se já existe uma venda para o novo veículo
        if sale.vehicle_id != existing_sale.vehicle_id:
            vehicle_sale = await self.repository.find_by_vehicle_id(sale.vehicle_id)
            if vehicle_sale:
                raise ValueError(f"Já existe uma venda para o veículo {sale.vehicle_id}")

        return await self.repository.update(sale)

    async def delete_sale(self, sale_id: str) -> bool:
        """Remove uma venda."""
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)
        return await self.repository.delete(sale_id)

    async def update_payment_status(self, sale_id: str, status: PaymentStatus) -> Sale:
        """Atualiza o status de pagamento de uma venda."""
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)

        sale.payment_status = status
        sale.updated_at = datetime.now()
        return await self.repository.update(sale) 