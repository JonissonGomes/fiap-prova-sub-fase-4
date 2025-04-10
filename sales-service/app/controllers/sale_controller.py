from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

from app.services.sale_service import SaleService
from app.adapters.mongodb_sale_repository import MongoDBSaleRepository
from app.schemas.sale_schema import (
    SaleCreate,
    SaleResponse,
    SaleUpdate,
    PaymentStatus
)
from app.domain.sale import Sale
from app.infrastructure.mongodb_config import MongoDB, MongoDBSettings
from app.services.sale_service_impl import SaleServiceImpl

router = APIRouter(tags=["sales"])

async def get_repository():
    mongodb = MongoDB()
    await mongodb.connect()
    return MongoDBSaleRepository(
        mongodb.client,
        mongodb.settings.db_name,
        mongodb.settings.collection
    )

async def get_service(repository: MongoDBSaleRepository = Depends(get_repository)):
    return SaleServiceImpl(repository)

@router.post("/sales", response_model=SaleResponse)
async def create_sale(
    sale: SaleCreate,
    service: SaleServiceImpl = Depends(get_service)
):
    """Cria uma nova venda."""
    try:
        domain_sale = Sale(
            vehicle_id=sale.vehicle_id,
            buyer_cpf=sale.buyer_cpf,
            sale_price=sale.sale_price,
            payment_code=sale.payment_code,
            payment_status=sale.payment_status
        )
        created_sale = await service.create_sale(domain_sale)
        return SaleResponse.from_domain(created_sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar venda: {str(e)}")

@router.get("/sales/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Obtém uma venda pelo ID."""
    try:
        sale = await service.get_sale(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return SaleResponse.from_domain(sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar venda: {str(e)}")

@router.get("/sales", response_model=List[SaleResponse])
async def get_sales(service: SaleServiceImpl = Depends(get_service)):
    """Lista todas as vendas."""
    try:
        sales = await service.get_all_sales()
        return [SaleResponse.from_domain(sale) for sale in sales]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vendas: {str(e)}")

@router.get("/sales/status/{status}", response_model=List[SaleResponse])
async def get_sales_by_status(status: PaymentStatus, service: SaleServiceImpl = Depends(get_service)):
    """Lista vendas por status."""
    try:
        sales = await service.get_sales_by_status(status)
        return [SaleResponse.from_domain(sale) for sale in sales]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vendas por status: {str(e)}")

@router.put("/sales/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: str,
    sale: SaleUpdate,
    service: SaleServiceImpl = Depends(get_service)
):
    """Atualiza uma venda existente."""
    try:
        domain_sale = Sale(
            id=sale_id,
            vehicle_id=sale.vehicle_id,
            buyer_cpf=sale.buyer_cpf,
            sale_price=sale.sale_price,
            payment_code=sale.payment_code,
            payment_status=sale.payment_status
        )
        updated_sale = await service.update_sale(domain_sale)
        return SaleResponse.from_domain(updated_sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar venda: {str(e)}")

@router.delete("/sales/{sale_id}")
async def delete_sale(
    sale_id: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Remove uma venda."""
    try:
        success = await service.delete_sale(sale_id)
        if not success:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return {"message": "Venda removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover venda: {str(e)}")

@router.patch("/sales/{sale_id}/payment-status", response_model=SaleResponse)
async def update_payment_status(
    sale_id: str,
    payment_status: PaymentStatus,
    service: SaleServiceImpl = Depends(get_service)
):
    """Atualiza o status de pagamento de uma venda."""
    try:
        updated_sale = await service.update_payment_status(sale_id, payment_status)
        if not updated_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Notifica o serviço principal sobre a mudança de status
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "http://core-service:8000/vehicles/sale-status",
                    json={
                        "vehicle_id": updated_sale.vehicle_id,
                        "status": payment_status
                    }
                )
            except Exception as e:
                print(f"Erro ao notificar o serviço principal: {e}")
        
        return updated_sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar status de pagamento: {str(e)}") 