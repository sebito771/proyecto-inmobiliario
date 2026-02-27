from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.usuario import UsuarioServices
from app.repo.usuario import UsuarioRepository

def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioServices:
    """Provee una instancia del servicio lista para usar en los endpoints."""
    repo = UsuarioRepository(db)
    return UsuarioServices(repo)