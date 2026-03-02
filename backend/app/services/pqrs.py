from fastapi import HTTPException
from app.repo import PqrsRepository, UsuarioRepository
from app.schemas.pqrs import PQRSCreate, EstadoPqrsEnum
from app.models import PQR as PQRModel


class PqrsServices:
    def __init__(self, repo: PqrsRepository, user_repo: UsuarioRepository):
        self.repo = repo
        self.user_repo = user_repo

    def create(self, datos: PQRSCreate, usuario_id: int):
        """Crea una nueva solicitud de PQRS asociada a un usuario."""
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario not found")

        nueva = PQRModel(
            usuario_id=usuario_id,
            tipo=datos.tipo.value,
            descripcion=datos.descripcion,
        )
        return self.repo.create(nueva)

    def list_by_user(self, usuario_id: int):
        """Devuelve todas las PQRS que pertenecen a un usuario."""
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario not found")
        data= self.repo.list_by_usuario(usuario_id)
        if not data:
            return []
        return data

    def get(self, pqrs_id: int):
        pq = self.repo.get_by_id(pqrs_id)
        if not pq:
            raise HTTPException(status_code=404, detail="PQR not found")
        return pq

    def update_status(self, pqrs_id: int, estado: EstadoPqrsEnum):
        pq = self.repo.get_by_id(pqrs_id)
        if not pq:
            raise HTTPException(status_code=404, detail="PQR not found")
        return self.repo.update(pq, {"estado": estado.value})