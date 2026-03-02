from app.repo.base_repo import BaseRepository
from app.models.pago import Pago as PagoModel


class PagoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(PagoModel, db)
    def get_by_compra_id(self, compra_id: int):
        """Retorna todos los pagos de una compra específica."""
        return self.db.query(PagoModel).filter(PagoModel.compra_id == compra_id).all()