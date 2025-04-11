from fastapi import HTTPException, status

class SaleNotFoundError(HTTPException):
    """Exceção lançada quando uma venda não é encontrada."""
    def __init__(self, sale_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venda com ID {sale_id} não encontrada"
        ) 