from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class CompraBase(BaseModel):
    usuario_id: int
    total: Decimal
    estado: Optional[str] = 'Activa'

class CompraCreate(CompraBase):
    pass

class CompraUpdate(CompraBase):
    pass

class Compra(CompraBase):
    id: int
    fecha_compra: datetime

    model_config = ConfigDict(from_attributes=True)

    