from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional

from app.domain.sale import Sale, SaleCreate, SaleStatus
from app.domain.sale_service import SaleService

router = APIRouter(
    tags=["sales"],
    responses={
        404: {"description": "Venda não encontrada"},
        400: {"description": "Requisição inválida"}
    }
)

def get_sale_service() -> SaleService:
    from app.adapters.api.main import app
    return app.sale_service

@router.post(
    "/",
    response_model=Sale,
    status_code=status.HTTP_201_CREATED,
    summary="Criar venda",
    description="Cria uma nova venda com os dados fornecidos. O veículo deve estar disponível para venda.",
    responses={
        201: {"description": "Venda criada com sucesso"},
        400: {"description": "Dados inválidos fornecidos ou veículo não disponível"},
        404: {"description": "Veículo não encontrado"}
    }
)
async def create_sale(sale: SaleCreate, sale_service: SaleService = Depends(get_sale_service)):
    try:
        return await sale_service.create_sale(sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/",
    response_model=List[Sale],
    summary="Listar vendas",
    description="Retorna uma lista de vendas, opcionalmente filtrada por status.",
    responses={
        200: {"description": "Lista de vendas retornada com sucesso"}
    }
)
async def list_sales(
    status: Optional[SaleStatus] = Query(None, description="Filtrar por status da venda"),
    sale_service: SaleService = Depends(get_sale_service)
):
    return await sale_service.list_sales(status)

@router.get(
    "/{sale_id}",
    response_model=Sale,
    summary="Obter venda por ID",
    description="Retorna os detalhes de uma venda específica pelo seu ID.",
    responses={
        200: {"description": "Venda encontrada"},
        404: {"description": "Venda não encontrada"}
    }
)
async def get_sale(sale_id: str, sale_service: SaleService = Depends(get_sale_service)):
    sale = await sale_service.get_sale(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale

@router.post(
    "/webhook/payment",
    response_model=Sale,
    summary="Webhook de pagamento",
    description="Atualiza o status de uma venda com base no status do pagamento. Se o pagamento for aprovado, o veículo será marcado como vendido.",
    responses={
        200: {"description": "Status da venda atualizado com sucesso"},
        404: {"description": "Venda não encontrada"},
        400: {"description": "Status de pagamento inválido"}
    }
)
async def payment_webhook(
    payment_id: str,
    status: str,
    sale_service: SaleService = Depends(get_sale_service)
):
    try:
        sale_status = SaleStatus.APPROVED if status == "approved" else SaleStatus.CANCELLED
        return await sale_service.update_sale_status(payment_id, sale_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/vehicles/available",
    summary="Listar veículos disponíveis",
    description="Retorna uma lista de veículos disponíveis para venda, ordenada por preço.",
    responses={
        200: {"description": "Lista de veículos disponíveis retornada com sucesso"}
    }
)
async def list_vehicles_for_sale(sale_service: SaleService = Depends(get_sale_service)):
    return await sale_service.list_vehicles_for_sale()

@router.get(
    "/vehicles/sold",
    summary="Listar veículos vendidos",
    description="Retorna uma lista de veículos vendidos, ordenada por preço.",
    responses={
        200: {"description": "Lista de veículos vendidos retornada com sucesso"}
    }
)
async def list_sold_vehicles(sale_service: SaleService = Depends(get_sale_service)):
    return await sale_service.list_sold_vehicles() 