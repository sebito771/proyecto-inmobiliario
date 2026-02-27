from app.repo.base_repo import BaseRepository
from app.models.detalle_compra import DetalleCompra as DetalleModel



class DetalleRepository(BaseRepository):
    def __init__(self,db):
        super().__init__(DetalleModel, db)