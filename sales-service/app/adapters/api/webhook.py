"""
Webhook para processamento de pagamentos
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.adapters.repository.sale_repository import SaleRepository
from app.domain.sale import SaleStatus
from app.ports.sale_repository import SaleRepositoryPort
from app.adapters.database import get_db

router = APIRouter()

@router.post("/webhook/payment")
async def payment_webhook(
    payment_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    """
    Webhook para atualização de status de pagamento
    
    Args:
        payment_id: ID do pagamento
        status: Status do pagamento (approved, rejected, pending)
    
    Returns:
        dict: Mensagem de confirmação
    """
    repository: SaleRepositoryPort = SaleRepository(db)
    
    # Busca a venda pelo ID do pagamento
    sale = repository.get_by_payment_id(payment_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    # Atualiza o status da venda
    if status.lower() == "approved":
        sale.status = SaleStatus.COMPLETED
        sale.payment_date = datetime.now()
    elif status.lower() == "rejected":
        sale.status = SaleStatus.CANCELLED
    elif status.lower() == "pending":
        sale.status = SaleStatus.PENDING
    else:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    # Salva as alterações
    repository.update(sale)
    
    return {"message": f"Status da venda atualizado para {sale.status.value}"} 