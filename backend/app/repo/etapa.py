from app.repo.base_repo import BaseRepository
from app.models.etapas import Etapa as EtapaModel



class EtapaRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(EtapaModel,db)