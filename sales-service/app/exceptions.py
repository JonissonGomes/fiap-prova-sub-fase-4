class SaleNotFoundError(Exception):
    """Exceção lançada quando uma venda não é encontrada."""
    def __init__(self, sale_id: str):
        self.sale_id = sale_id
        self.message = f"Venda com ID {sale_id} não encontrada"
        super().__init__(self.message) 