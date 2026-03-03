from app.repo.base_repo import BaseRepository
from app.models.compra import Compra as CompraModel

class CompraRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(CompraModel, db)

    def get_expired_active(self, fecha_expiracion):
        return self.db.query(CompraModel).filter(
            CompraModel.fecha_expiracion < fecha_expiracion,
            CompraModel.estado == "Activa"
        ).all()

    def get_by_usuario_id(self, usuario_id: int):
        """Obtiene todas las compras de un usuario específico."""
        return self.db.query(CompraModel).filter(
            CompraModel.usuario_id == usuario_id
        ).all()

