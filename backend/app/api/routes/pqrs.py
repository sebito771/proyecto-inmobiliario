from fastapi import APIRouter, Depends
from app.schemas.pqrs import PQRSCreate, PQRS, EstadoPqrsEnum
from app.services.pqrs import PqrsServices
from app.api.dependencies import get_pqrs_service


router = APIRouter(tags=["pqrs"])


@router.post("/create", response_model=PQRS)
def create_pqrs(pqrs: PQRSCreate, usuario_id: int, services: PqrsServices = Depends(get_pqrs_service)):
    return services.create(pqrs, usuario_id)


@router.get("/user/{usuario_id}", response_model=list[PQRS])
def list_user_pqrs(usuario_id: int, services: PqrsServices = Depends(get_pqrs_service)):
    return services.list_by_user(usuario_id)


@router.get("/{pqrs_id}", response_model=PQRS)
def get_pqrs(pqrs_id: int, services: PqrsServices = Depends(get_pqrs_service)):
    return services.get(pqrs_id)


@router.put("/update-status")
def update_status(pqrs_id: int, estado: EstadoPqrsEnum, services: PqrsServices = Depends(get_pqrs_service)):
    return services.update_status(pqrs_id, estado)
