from app.repo.base_repo import BaseRepository
from app.models.detalle_compra import DetalleCompra as DetalleModel



class DetalleRepository(BaseRepository):
    def __init__(self,db):
        super().__init__(DetalleModel, db)

    
    def get_by_compra_id(self,compra_id):
        return self.db.query(DetalleModel).filter(DetalleModel.compra_id == compra_id).all()
    
    def get_by_lote_id(self, lote_id):
        return self.db.query(DetalleModel).filter(DetalleModel.lote_id == lote_id).all()