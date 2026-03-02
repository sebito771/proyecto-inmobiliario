from app.repo.base_repo import BaseRepository
from app.models.lote import Lote as LoteModel


class LoteRepository(BaseRepository):
    def __init__(self,db):
        super().__init__(LoteModel, db)
  
    def list_filtered(self, estado: str = None, etapa_id: int = None):
        query = self.db.query(LoteModel)
        if estado:
            query = query.filter(LoteModel.estado == estado)
        if etapa_id:
            query = query.filter(LoteModel.etapa_id == etapa_id)
        return query
    
 
