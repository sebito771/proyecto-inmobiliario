from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services import UsuarioServices , LoteServices
from app.repo import UsuarioRepository , LoteRepository , CompraRepository , DetalleRepository , EtapaRepository




def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioServices:
    """Provee una instancia del servicio lista para usar en los endpoints."""
    repo = UsuarioRepository(db)
    return UsuarioServices(repo)

def get_lote_service(db: Session = Depends(get_db)) -> LoteServices:
    repo= LoteRepository(db)
    user_repo= UsuarioRepository(db)
    compra_repo= CompraRepository(db)
    detalle_repo= DetalleRepository(db)
    etapa_repo= EtapaRepository(db)
    return LoteServices(repo,user_repo,compra_repo,detalle_repo,etapa_repo,db)