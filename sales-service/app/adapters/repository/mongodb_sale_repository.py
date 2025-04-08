from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.domain.sale import Sale, SaleStatus
from app.ports.sale_repository import SaleRepository

class MongoDBSaleRepository(SaleRepository):
    COLLECTION_NAME = "sales"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[self.COLLECTION_NAME]

    async def save(self, sale: Sale) -> Sale:
        sale_dict = sale.model_dump()
        sale_dict["_id"] = sale_dict.pop("id")
        await self.collection.insert_one(sale_dict)
        return sale

    async def find_by_id(self, sale_id: str) -> Optional[Sale]:
        sale_dict = await self.collection.find_one({"_id": sale_id})
        if sale_dict:
            return self._to_domain(sale_dict)
        return None

    async def find_all(self, status: Optional[SaleStatus] = None) -> List[Sale]:
        query = {"status": status} if status else {}
        cursor = self.collection.find(query)
        sales = []
        async for sale_dict in cursor:
            sales.append(self._to_domain(sale_dict))
        return sales

    async def update(self, sale: Sale) -> Sale:
        sale_dict = sale.model_dump()
        sale_id = sale_dict.pop("id")
        await self.collection.update_one(
            {"_id": sale_id},
            {"$set": sale_dict}
        )
        return sale

    def _to_domain(self, sale_dict: dict) -> Sale:
        sale_dict["id"] = sale_dict.pop("_id")
        return Sale(**sale_dict) 