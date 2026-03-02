from fastapi import APIRouter, Depends
from app.schemas.usuario import RolCreate, Rol
from app.services.rol import RolServices
from app.api.dependencies import get_rol_service


router = APIRouter(tags=["roles"])


@router.get("/list", response_model=list[Rol])
def list_roles(services: RolServices = Depends(get_rol_service)):
    return services.list_all()


@router.get("/{rol_id}", response_model=Rol)
def get_rol(rol_id: int, services: RolServices = Depends(get_rol_service)):
    return services.get(rol_id)


@router.post("/create", response_model=Rol)
def create_rol(rol: RolCreate, services: RolServices = Depends(get_rol_service)):
    return services.create(rol)
