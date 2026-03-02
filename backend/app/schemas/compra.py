from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class DetalleCompraBase(BaseModel):
    compra_id: int
    lote_id: int
    precio: Decimal


class DetalleCompraCreate(DetalleCompraBase):
    pass


class DetalleCompra(DetalleCompraBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


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

    