from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.domain.sale import Sale
from app.ports.sale_repository import SaleRepository
from datetime import datetime

class MongoDBSaleRepository(SaleRepository):
    COLLECTION_NAME = "sales"

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[self.COLLECTION_NAME]

    async def save(self, sale: Sale) -> Sale:
        sale_dict = sale.to_dict()
        sale_dict["_id"] = ObjectId(sale_dict.pop("id")) if sale_dict.get("id") else ObjectId()
        await self.collection.insert_one(sale_dict)
        return Sale.from_dict(sale_dict)

    async def find_by_id(self, sale_id: str) -> Optional[Sale]:
        sale_dict = await self.collection.find_one({"_id": ObjectId(sale_id)})
        return Sale.from_dict(sale_dict) if sale_dict else None

    async def find_by_vehicle_id(self, vehicle_id: str) -> Optional[Sale]:
        sale_dict = await self.collection.find_one({"vehicle_id": vehicle_id})
        return Sale.from_dict(sale_dict) if sale_dict else None

    async def find_by_payment_code(self, payment_code: str) -> Optional[Sale]:
        sale_dict = await self.collection.find_one({"payment_code": payment_code})
        return Sale.from_dict(sale_dict) if sale_dict else None

    async def find_all(self) -> List[Sale]:
        sales = []
        async for sale_dict in self.collection.find():
            sales.append(Sale.from_dict(sale_dict))
        return sales

    async def find_by_status(self, status: str) -> List[Sale]:
        sales = []
        async for sale_dict in self.collection.find({"payment_status": status}):
            sales.append(Sale.from_dict(sale_dict))
        return sales

    async def update(self, sale: Sale) -> Optional[Sale]:
        sale_dict = sale.to_dict()
        sale_id = ObjectId(sale_dict.pop("id"))
        sale_dict["updated_at"] = datetime.now()

        result = await self.collection.update_one({"_id": sale_id}, {"$set": sale_dict})
        if result.modified_count == 0:
            return None

        updated_sale = await self.collection.find_one({"_id": sale_id})
        return Sale.from_dict(updated_sale)

    async def delete(self, sale_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(sale_id)})
        return result.deleted_count > 0
