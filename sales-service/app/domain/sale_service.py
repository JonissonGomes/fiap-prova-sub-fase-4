from typing import List, Optional
from app.domain.sale import Sale, SaleCreate, SaleStatus
from app.ports.sale_repository import SaleRepository
import httpx

class SaleService:
    def __init__(self, repository: SaleRepository):
        self.repository = repository
        self.core_service_url = "http://core-service:8000"

    async def create_sale(self, sale: SaleCreate) -> Sale:
        # Verifica se o veículo existe e está disponível
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.core_service_url}/vehicles/{sale.vehicle_id}")
            if response.status_code == 404:
                raise ValueError("Veículo não encontrado")
            
            vehicle = response.json()
            if vehicle["status"] != "AVAILABLE":
                raise ValueError("Veículo não está disponível para venda")

        # Cria a venda
        sale_data = Sale(**sale.model_dump())
        return await self.repository.save(sale_data)

    async def get_sale(self, sale_id: str) -> Optional[Sale]:
        return await self.repository.find_by_id(sale_id)

    async def list_sales(self, status: Optional[SaleStatus] = None) -> List[Sale]:
        return await self.repository.find_all(status)

    async def update_sale_status(self, sale_id: str, status: SaleStatus) -> Sale:
        sale = await self.repository.find_by_id(sale_id)
        if not sale:
            raise ValueError("Venda não encontrada")

        sale.status = status
        updated_sale = await self.repository.update(sale)

        # Se o pagamento foi aprovado, marca o veículo como vendido
        if status == SaleStatus.APPROVED:
            async with httpx.AsyncClient() as client:
                await client.post(f"{self.core_service_url}/vehicles/{sale.vehicle_id}/mark-as-sold")

        return updated_sale

    async def list_vehicles_for_sale(self) -> List[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.core_service_url}/vehicles/available/")
            vehicles = response.json()
            return sorted(vehicles, key=lambda x: x["price"])

    async def list_sold_vehicles(self) -> List[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.core_service_url}/vehicles/sold/")
            vehicles = response.json()
            return sorted(vehicles, key=lambda x: x["price"]) 