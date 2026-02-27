from app.repo.base_repo import BaseRepository
from app.models.compra import Compra as CompraModel

class CompraRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(CompraModel, db)
