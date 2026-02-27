from app.repo.base_repo import BaseRepository
from app.models import lote as LoteModel


class LoteRepository(BaseRepository):
    def __init__(self,db):
        super().__init__(LoteModel, db)
 
