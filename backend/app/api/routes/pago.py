from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.schemas.pago import PagoCreate, Pago
from app.services.pago import PagoServices
from app.api.dependencies import get_pago_service
from app.core.security import get_current_user
from app.models.usuario import Usuario as UsuarioModel

router = APIRouter(tags=["pagos"])


@router.post("/register", response_model=Pago)
def register_payment(
    pago: PagoCreate,
    background_tasks: BackgroundTasks,
    services: PagoServices = Depends(get_pago_service),
    current_user: UsuarioModel = Depends(get_current_user),
):
    # solo el propietario de la compra o administrador puede abonar
    compra = services.compra_repo.get_by_id(pago.compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra not found")
    if compra.usuario_id != current_user.id and current_user.rol.nombre != "Administrador":
        raise HTTPException(status_code=403, detail="Not authorized to pay this purchase")

    return services.registrar_abono(pago, background_tasks)


@router.get("/compra/{compra_id}", response_model=list[Pago])
def get_pagos_by_compra(
    compra_id: int,
    services: PagoServices = Depends(get_pago_service),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """Retorna el historial de pagos de una compra."""
    compra = services.compra_repo.get_by_id(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra not found")

    # validar acceso
    if compra.usuario_id != current_user.id and current_user.rol.nombre != "Administrador":
        raise HTTPException(status_code=403, detail="Not authorized to view this purchase")

    return services.repo.get_by_compra_id(compra_id)


@router.get("/resumen/{compra_id}")
def get_resumen_compra(
    compra_id: int,
    services: PagoServices = Depends(get_pago_service),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """Retorna resumen {total_compra, total_pagado, saldo_pendiente}."""
    compra = services.compra_repo.get_by_id(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra not found")

    # validar acceso
    if compra.usuario_id != current_user.id and current_user.rol.nombre != "Administrador":
        raise HTTPException(status_code=403, detail="Not authorized to view this purchase")

    return services.get_resumen_compra(compra_id)

