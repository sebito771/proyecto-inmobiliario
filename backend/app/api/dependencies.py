from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services import UsuarioServices , LoteServices , PqrsServices , RolServices , DetalleCompraServices
from app.repo import UsuarioRepository , LoteRepository , CompraRepository , DetalleRepository , EtapaRepository , PqrsRepository , RolRepository




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


def get_pqrs_service(db: Session = Depends(get_db)) -> PqrsServices:
    repo = PqrsRepository(db)
    user_repo = UsuarioRepository(db)
    return PqrsServices(repo, user_repo)


def get_rol_service(db: Session = Depends(get_db)) -> RolServices:
    repo = RolRepository(db)
    return RolServices(repo)


def get_detalle_compra_service(db: Session = Depends(get_db)) -> DetalleCompraServices:
    repo = DetalleRepository(db)
    compra_repo = CompraRepository(db)
    lote_repo = LoteRepository(db)
    return DetalleCompraServices(repo, compra_repo, lote_repo)