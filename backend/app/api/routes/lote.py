from fastapi import Depends, APIRouter
from app.services.lote import LoteServices
from app.schemas.lote import LoteSell, LoteCreate, LoteUpdate, Lote
from app.api.dependencies import get_lote_service
from app.core.security import RoleChecker

router = APIRouter(tags=["lotes"])
admin_only = RoleChecker(["Administrador"])

@router.post("/buy")
def buy_lote(sell: LoteSell, services: LoteServices = Depends(get_lote_service)):
    vnt = services.buy_lote(sell)
    if vnt:
        return {"message": "buy lote successful"}

@router.post("/create")
def create_lote(
    lote: LoteCreate,
    services: LoteServices = Depends(get_lote_service),
    current=Depends(admin_only),
):
    return services.create_lote(lote)

@router.put("/update/{lote_id}")
def update_lote(
    lote_id: int,
    updates: LoteUpdate,
    services: LoteServices = Depends(get_lote_service),
    current=Depends(admin_only),
):
    return services.update_lote(lote_id, updates)

@router.delete("/delete/{lote_id}")
def delete_lote(
    lote_id: int,
    services: LoteServices = Depends(get_lote_service),
    current=Depends(admin_only),
):
    return services.delete_lote(lote_id)

@router.get("/list", response_model=list[Lote])
def list_lotes(services: LoteServices = Depends(get_lote_service)):
    return services.list_lotes()



                
