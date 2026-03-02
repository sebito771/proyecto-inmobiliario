from fastapi import HTTPException
from app.repo import RolRepository
from app.models.rol import Rol as RolModel
from app.schemas.usuario import RolCreate


class RolServices:
    def __init__(self, repo: RolRepository):
        self.repo = repo

    def list_all(self):
        """Retorna todos los roles disponibles."""
        return self.repo.list()

    def get(self, rol_id: int):
        """Obtiene un rol por ID."""
        rol = self.repo.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol not found")
        return rol

    def create(self, datos: RolCreate):
        """Crea un nuevo rol."""
        existe = self.repo.find_by_name(datos.nombre)
        if existe:
            raise HTTPException(status_code=400, detail="Rol already exists")
        
        nuevo = RolModel(nombre=datos.nombre)
        return self.repo.create(nuevo)
