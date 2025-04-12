from typing import List, Optional
from app.domain.sale import Sale, PaymentStatus
from app.domain.sale_schema import SaleCreate, SaleUpdate
from app.services.sale_service import SaleService
from app.adapters.mongodb_sale_repository import MongoDBSaleRepository
from datetime import datetime


class SaleServiceImpl(SaleService):
    def __init__(self, repository: MongoDBSaleRepository):
        self.repository = repository

    async def create_sale(self, sale_data: SaleCreate) -> Sale:
        new_sale = Sale(
            vehicle_id=sale_data.vehicle_id,
            buyer_cpf=sale_data.buyer_cpf,
            sale_price=sale_data.sale_price,
            payment_code=sale_data.payment_code,
            payment_status=PaymentStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return await self.repository.save(new_sale)

    async def get_sale(self, sale_id: str) -> Optional[Sale]:
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise Exception("Venda não encontrada")
        return sale

    async def get_sale_by_vehicle_id(self, vehicle_id: str) -> Optional[Sale]:
        sale = await self.repository.find_by_vehicle_id(vehicle_id)
        if not sale:
            raise Exception("Venda não encontrada")
        return sale

    async def get_all_sales(self) -> List[Sale]:
        return await self.repository.find_all()

    async def get_sales_by_status(self, status: str) -> List[Sale]:
        return await self.repository.find_by_status(status)

    async def update_sale(self, sale_id: str, sale_data: SaleUpdate) -> Optional[Sale]:
        existing = await self.repository.find_by_id(sale_id)
        if not existing:
            raise Exception("Venda não encontrada")

        update_fields = sale_data.dict(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(existing, key, value)
        existing.updated_at = datetime.utcnow()
        return await self.repository.update(existing)

    async def delete_sale(self, sale_id: str) -> None:
        result = await self.repository.delete(sale_id)
        if not result:
            raise Exception("Venda não encontrada")

    async def update_payment_status(self, sale_id: str, status: PaymentStatus) -> Optional[Sale]:
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise Exception("Venda não encontrada")
        sale.payment_status = status
        sale.updated_at = datetime.utcnow()
        return await self.repository.update(sale)

    async def get_sale_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        sale = await self.repository.find_by_payment_code(payment_code)
        if not sale:
            raise Exception("Venda não encontrada")
        return sale
