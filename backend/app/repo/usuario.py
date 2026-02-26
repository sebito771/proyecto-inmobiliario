from app.repo.base_repo import BaseRepository
from app.models.usuario import Usuario as UsuarioModel
from sqlalchemy.orm import Session
from typing import Optional


class UsuarioRepository(BaseRepository[UsuarioModel]):
    def __init__(self, db: Session):
        super().__init__(UsuarioModel, db)
    
    def find_by_email(self, email: str) -> Optional[UsuarioModel]:
        return self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    
    def activate_user(self, usuario_id: int) -> UsuarioModel:
        db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if db_usuario.activo:
            return db_usuario
        db_usuario.activo = True
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

 