from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ...domain.sale import Sale, PaymentStatus
from ...ports.sale_service import SaleService
from .schemas import SaleCreate, SaleResponse, SaleUpdate
from .dependencies import get_sale_service

router = APIRouter()

@router.post("/", response_model=SaleResponse)
async def create_sale(sale: SaleCreate, service: SaleService = Depends(get_sale_service)):
    try:
        created_sale = service.create_sale(sale.to_domain())
        return SaleResponse.from_domain(created_sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: int, service: SaleService = Depends(get_sale_service)):
    sale = service.get_sale(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return SaleResponse.from_domain(sale)

@router.get("/", response_model=List[SaleResponse])
async def get_sales(service: SaleService = Depends(get_sale_service)):
    sales = service.get_all_sales()
    return [SaleResponse.from_domain(sale) for sale in sales]

@router.get("/pending", response_model=List[SaleResponse])
async def get_pending_sales(service: SaleService = Depends(get_sale_service)):
    try:
        sales = service.get_pending_sales()
        return [SaleResponse.from_domain(sale) for sale in sales]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/paid", response_model=List[SaleResponse])
async def get_paid_sales(service: SaleService = Depends(get_sale_service)):
    try:
        sales = service.get_paid_sales()
        return [SaleResponse.from_domain(sale) for sale in sales]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payment/{payment_code}", response_model=SaleResponse)
async def get_sale_by_payment_code(payment_code: str, service: SaleService = Depends(get_sale_service)):
    sale = service.get_sale_by_payment_code(payment_code)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return SaleResponse.from_domain(sale)

@router.put("/{sale_id}/paid", response_model=SaleResponse)
async def mark_as_paid(sale_id: int, service: SaleService = Depends(get_sale_service)):
    try:
        sale = service.mark_as_paid(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return SaleResponse.from_domain(sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{sale_id}/status", response_model=SaleResponse)
async def update_payment_status(sale_id: int, status: SaleUpdate, service: SaleService = Depends(get_sale_service)):
    try:
        sale = service.get_sale(sale_id)
        if not sale:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        updated_sale = service.update_sale(sale_id, status.to_domain())
        if not updated_sale:
            raise HTTPException(status_code=400, detail="Erro ao atualizar status da venda")
        return SaleResponse.from_domain(updated_sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 