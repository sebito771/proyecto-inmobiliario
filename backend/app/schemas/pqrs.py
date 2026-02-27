from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PQRSBase(BaseModel):
    tipo: str
    descripcion: str

class PQRSCreate(PQRSBase):
    pass


class PQRS(PQRSBase):
    id: int
    usuario_id: int
    estado: Optional[str] = 'Pendiente'
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)