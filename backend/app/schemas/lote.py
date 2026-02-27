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

class LoteUpdate(LoteBase):
    valor: Optional[Decimal] = None
    estado: Optional[str] = None


class Lote(LoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)