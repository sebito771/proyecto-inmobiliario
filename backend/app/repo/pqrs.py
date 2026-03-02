from app.repo.base_repo import BaseRepository
from app.models.pqrs import PQR as PQRModel


class PqrsRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(PQRModel, db)

    def list_by_usuario(self, usuario_id: int):
        """Retorna todos los registros PQRS creados por un usuario determinado."""
        return self.db.query(PQRModel).filter(PQRModel.usuario_id == usuario_id).all()