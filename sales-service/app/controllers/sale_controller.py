from venv import logger
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId

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
from app.exceptions import SaleNotFoundError

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
        # Cria o objeto de domínio
        domain_sale = Sale(
            id=str(ObjectId()),
            vehicle_id=sale.vehicle_id,
            buyer_cpf=sale.buyer_cpf,
            sale_price=sale.sale_price,
            payment_code=sale.payment_code,
            payment_status=sale.payment_status
        )
        
        # Salva a venda
        created_sale = await service.create_sale(domain_sale)
        
        # Converte para o schema de resposta
        return SaleResponse.from_domain(created_sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar venda: {str(e)}")

@router.get("/sales/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: str, service: SaleService = Depends(get_service)):
    # Verifica se é um ObjectId válido
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    try:
        return await service.get_sale(sale_id)
    except SaleNotFoundError:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

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

@router.get("/sales/payment/{payment_code}", response_model=SaleResponse)
async def get_sale_by_payment_code(
    payment_code: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Obtém uma venda pelo código de pagamento."""
    try:
        sale = await service.get_sale_by_payment_code(payment_code)
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return SaleResponse.from_domain(sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar venda: {str(e)}")

@router.put("/sales/{sale_id}", response_model=SaleResponse)
async def update_sale(sale_id: str, sale_update: SaleUpdate, service=Depends(get_service)):
    if not ObjectId.is_valid(sale_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    updated_sale = await service.update_sale(sale_id, sale_update)
    
    if not updated_sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    return SaleResponse.from_domain(updated_sale)

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

@router.patch("/sales/{sale_id}/mark-as-canceled", response_model=SaleResponse)
async def mark_sale_as_open(
    sale_id: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Marca uma venda como Em aberta."""
    try:
        updated_sale = await service.update_payment_status(sale_id, PaymentStatus.CANCELLED)
        if not updated_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Notifica o serviço principal sobre a mudança de status
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "http://core-service:8000/vehicles/sale-status",
                    json={
                        "vehicle_id": updated_sale.vehicle_id,
                        "status": PaymentStatus.CANCELLED
                    }
                )
            except Exception as e:
                print(f"Erro ao notificar o serviço principal: {e}")
        
        return SaleResponse.from_domain(updated_sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao marcar venda como Em aberta: {str(e)}")

@router.patch("/sales/{sale_id}/mark-as-pending", response_model=SaleResponse)
async def mark_sale_as_pending(
    sale_id: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Marca uma venda como Pendente."""
    try:
        updated_sale = await service.update_payment_status(sale_id, PaymentStatus.PENDING)
        if not updated_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Notifica o serviço principal sobre a mudança de status
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "http://core-service:8000/vehicles/sale-status",
                    json={
                        "vehicle_id": updated_sale.vehicle_id,
                        "status": PaymentStatus.PENDING
                    }
                )
            except Exception as e:
                print(f"Erro ao notificar o serviço principal: {e}")
        
        return SaleResponse.from_domain(updated_sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao marcar venda como Pendente: {str(e)}")

@router.patch("/sales/{sale_id}/mark-as-paid", response_model=SaleResponse)
async def mark_sale_as_paid(
    sale_id: str,
    service: SaleServiceImpl = Depends(get_service)
):
    """Marca uma venda como Pago."""
    try:
        updated_sale = await service.update_payment_status(sale_id, PaymentStatus.PAID)
        if not updated_sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        # Notifica o serviço principal sobre a mudança de status
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "http://core-service:8000/vehicles/sale-status",
                    json={
                        "vehicle_id": updated_sale.vehicle_id,
                        "status": PaymentStatus.PAID
                    }
                )
            except Exception as e:
                print(f"Erro ao notificar o serviço principal: {e}")
        
        return SaleResponse.from_domain(updated_sale)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao marcar venda como Pago: {str(e)}")

@router.post("/sales/webhook/payment", response_model=SaleResponse)
async def payment_webhook(
    payment_data: dict,
    service: SaleServiceImpl = Depends(get_service)
):
    """Webhook para atualização de status de pagamento."""
    try:
        logger.info(f"Recebido webhook de pagamento: {payment_data}")
        
        payment_code = payment_data.get("payment_code")
        status = payment_data.get("status")
        vehicle_id = payment_data.get("vehicle_id")

        if not all([payment_code, status, vehicle_id]):
            raise HTTPException(
                status_code=400,
                detail="Dados de pagamento incompletos. São necessários: payment_code, status e vehicle_id"
            )

        # Valida o status
        try:
            logger.info(f"Tentando converter status: {status}")
            payment_status = PaymentStatus(status.upper())
            logger.info(f"Status convertido com sucesso: {payment_status}")
        except ValueError:
            logger.error(f"Status inválido: {status}")
            raise HTTPException(
                status_code=400,
                detail="Status de pagamento inválido. Valores aceitos: PAGO, PENDENTE, CANCELADO"
            )

        # Busca a venda pelo código de pagamento
        logger.info(f"Buscando venda pelo código de pagamento: {payment_code}")
        sale = await service.get_sale_by_payment_code(payment_code)
        if not sale:
            logger.error(f"Venda não encontrada para o código: {payment_code}")
            raise HTTPException(status_code=404, detail="Venda não encontrada para o código de pagamento fornecido")
        
        logger.info(f"Venda encontrada: {sale.id}")

        # Atualiza o status da venda usando o ID
        logger.info(f"Atualizando status da venda {sale.id} para {payment_status}")
        updated_sale = await service.update_payment_status(sale.id, payment_status)
        if not updated_sale:
            logger.error(f"Erro ao atualizar status da venda {sale.id}")
            raise HTTPException(status_code=404, detail="Erro ao atualizar status da venda")

        # Notifica o serviço principal sobre a mudança de status
        logger.info(f"Notificando core-service sobre mudança de status do veículo {vehicle_id}")
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    "http://core-service:8000/vehicles/sale-status",
                    json={
                        "vehicle_id": vehicle_id,
                        "status": payment_status.value
                    }
                )
                logger.info("Notificação enviada com sucesso")
            except Exception as e:
                logger.error(f"Erro ao notificar o serviço principal: {e}")
                # Não interrompe o fluxo se falhar a notificação
                pass

        return SaleResponse.from_domain(updated_sale)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao processar webhook de pagamento: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar webhook de pagamento: {str(e)}"
        ) 