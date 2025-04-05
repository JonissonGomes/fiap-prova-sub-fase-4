from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ...domain.sale import Sale
from ...ports.sale_service import SaleService
from .schemas import SaleCreate, SaleResponse, SaleUpdate

router = APIRouter()

@router.post("/", response_model=SaleResponse)
async def create_sale(sale: SaleCreate, service: SaleService = Depends()):
    try:
        return service.create_sale(sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(sale_id: int, service: SaleService = Depends()):
    sale = service.get_sale(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale

@router.get("/", response_model=List[SaleResponse])
async def get_sales(service: SaleService = Depends()):
    return service.get_sales()

@router.get("/pending/", response_model=List[SaleResponse])
async def get_pending_sales(service: SaleService = Depends()):
    return service.get_pending_sales()

@router.get("/paid/", response_model=List[SaleResponse])
async def get_paid_sales(service: SaleService = Depends()):
    return service.get_paid_sales()

@router.put("/{payment_code}/status", response_model=SaleResponse)
async def update_payment_status(payment_code: str, status: str, service: SaleService = Depends()):
    try:
        return service.update_payment_status(payment_code, status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 