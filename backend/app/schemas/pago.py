from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal

class PagoBase(BaseModel):
    compra_id: int
    valor_pagado: Decimal
    comprobante: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class Pago(PagoBase):
    id: int
    fecha_pago: datetime

    model_config = ConfigDict(from_attributes=True)