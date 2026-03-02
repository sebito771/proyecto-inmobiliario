from fastapi import APIRouter, Depends
from app.schemas.compra import DetalleCompraCreate, DetalleCompra
from app.services.detalle_compra import DetalleCompraServices
from app.api.dependencies import get_detalle_compra_service


router = APIRouter(tags=["detalle_compra"])


@router.get("/{detalle_id}", response_model=DetalleCompra)
def get_detalle(detalle_id: int, services: DetalleCompraServices = Depends(get_detalle_compra_service)):
    return services.get(detalle_id)


@router.get("/compra/{compra_id}", response_model=list[DetalleCompra])
def list_by_compra(compra_id: int, services: DetalleCompraServices = Depends(get_detalle_compra_service)):
    return services.list_by_compra(compra_id)


@router.post("/create", response_model=DetalleCompra)
def create_detalle(detalle: DetalleCompraCreate, services: DetalleCompraServices = Depends(get_detalle_compra_service)):
    return services.create(detalle)
