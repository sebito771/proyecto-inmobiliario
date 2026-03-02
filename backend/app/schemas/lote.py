from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

class LoteBase(BaseModel):
    area_m2: int
    ubicacion: str
    valor: Decimal
    estado: Optional[str] = 'Disponible'
    etapa_id: int

class LoteCreate(LoteBase):
    pass

class LoteUpdate(BaseModel):
    area_m2: Optional[int] = None
    ubicacion: Optional[str] = None
    valor: Optional[Decimal] = None
    estado: Optional[str] = None
    etapa_id: Optional[int] = None


class LoteSell(BaseModel):
    usuario_id: int
    lote_id: list[int]

class Lote(LoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)