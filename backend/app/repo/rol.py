from app.repo.base_repo import BaseRepository
from app.models.rol import Rol as RolModel


class RolRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(RolModel, db)

    def find_by_name(self, nombre: str):
        """Busca un rol por su nombre."""
        return self.db.query(RolModel).filter(RolModel.nombre == nombre).first()
