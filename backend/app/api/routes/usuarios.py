from fastapi import APIRouter, Depends
from app.services.usuario import UsuarioServices
from app.schemas.usuario import UsuarioInDB
from app.core.security import RoleChecker
from app.api.dependencies import get_usuario_service

router = APIRouter(tags=["usuarios"])

admin_only = RoleChecker(["Administrador"])


@router.get("/list", response_model=list[UsuarioInDB])
def list_users(
    services: UsuarioServices = Depends(get_usuario_service),
    current=Depends(admin_only),
):
    return services.list_users()


@router.put("/deactivate")
def deactivate_user(
    usuario_id: int,
    services: UsuarioServices = Depends(get_usuario_service),
    current=Depends(admin_only),
):
    return services.desactivar_usuario(usuario_id)
