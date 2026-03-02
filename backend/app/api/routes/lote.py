from fastapi import  Depends, APIRouter
from app.services.lote import LoteServices
from app.schemas.lote import LoteSell , LoteCreate , LoteUpdate , Lote
from app.api.dependencies import get_lote_service




router = APIRouter( tags=["lotes"])

@router.post("/buy")
def buy_lote(sell: LoteSell, services: LoteServices = Depends(get_lote_service)):
     vnt=services.buy_lote(sell)
     if vnt:
          return {"message":"buy lote successful"}
     

@router.post("/create")
def create_lote(lote: LoteCreate, services: LoteServices = Depends(get_lote_service)):
     return services.create_lote(lote)

@router.put("/update")
def update_lote(lote_id: int, updates: LoteUpdate, services: LoteServices = Depends(get_lote_service)):
     return services.update_lote(lote_id, updates)

@router.delete("/delete")
def delete_lote(lote_id:int ,services: LoteServices = Depends(get_lote_service)):
     return services.delete_lote(lote_id)

@router.get("/list",response_model=list[Lote])
def list_lotes(services: LoteServices= Depends(get_lote_service)):
     return services.list_lotes()



                
