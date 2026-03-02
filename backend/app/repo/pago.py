from app.repo.base_repo import BaseRepository
from app.models.pago import Pago as PagoModel


class PagoRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(PagoModel, db)
