from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.domain.sale import Sale
from app.ports.sale_repository import SaleRepository
from datetime import datetime

class MongoDBSaleRepository(SaleRepository):
    """Implementação do repositório de vendas usando MongoDB."""

    def __init__(self, client: AsyncIOMotorClient, db_name: str = "sales_db", collection_name: str = "sales"):
        self.client = client
        self.db = client[db_name]
        self.collection = self.db[collection_name]

    async def save(self, sale: Sale) -> Sale:
        """Salva uma venda no MongoDB."""
        sale_dict = sale.to_dict()
        if sale_dict.get("id"):
            sale_dict["_id"] = ObjectId(sale_dict.pop("id"))
        else:
            sale_dict["_id"] = ObjectId()

        await self.collection.insert_one(sale_dict)
        return Sale.from_dict(sale_dict)

    async def find_by_id(self, sale_id: str) -> Optional[Sale]:
        """Busca uma venda pelo ID."""
        sale_dict = await self.collection.find_one({"_id": ObjectId(sale_id)})
        if sale_dict:
            return Sale.from_dict(sale_dict)
        return None

    async def find_by_vehicle_id(self, vehicle_id: str) -> Optional[Sale]:
        """Busca uma venda pelo ID do veículo."""
        sale_dict = await self.collection.find_one({"vehicle_id": vehicle_id})
        if sale_dict:
            return Sale.from_dict(sale_dict)
        return None

    async def find_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        """Busca uma venda pelo código de pagamento."""
        sale_dict = await self.collection.find_one({"payment_code": payment_code})
        if sale_dict:
            return Sale.from_dict(sale_dict)
        return None

    async def find_all(self) -> List[Sale]:
        """Lista todas as vendas."""
        sales = []
        async for sale_dict in self.collection.find():
            sales.append(Sale.from_dict(sale_dict))
        return sales

    async def find_by_status(self, status: str) -> List[Sale]:
        """Lista vendas por status."""
        sales = []
        async for sale_dict in self.collection.find({"payment_status": status}):
            sales.append(Sale.from_dict(sale_dict))
        return sales

    async def update(self, sale: Sale) -> Sale:
        """Atualiza uma venda."""
        sale_dict = sale.to_dict()
        sale_id = ObjectId(sale_dict.pop("id"))
        sale_dict["updated_at"] = datetime.now()

        result = await self.collection.update_one(
            {"_id": sale_id},
            {"$set": sale_dict}
        )
        if result.modified_count == 0:
            return None

        updated_sale = await self.collection.find_one({"_id": sale_id})
        return Sale.from_dict(updated_sale)

    async def delete(self, sale_id: str) -> bool:
        """Remove uma venda."""
        result = await self.collection.delete_one({"_id": ObjectId(sale_id)})
        return result.deleted_count > 0 