from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoPqrsEnum(str, Enum):
    PETICION = 'Peticion'
    QUEJA = 'Queja'
    RECLAMO = 'Reclamo'
    SUGERENCIA = 'Sugerencia'


class EstadoPqrsEnum(str, Enum):
    PENDIENTE = 'Pendiente'
    EN_PROCESO = 'En proceso'
    CERRADO = 'Cerrado'


class PQRSBase(BaseModel):
    tipo: TipoPqrsEnum
    descripcion: str

    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError('La descripción no puede estar vacía')
        if len(v) < 10:
            raise ValueError('La descripción debe tener al menos 10 caracteres')
        if len(v) > 500:
            raise ValueError('La descripción no puede exceder 500 caracteres')
        return v.strip()


class PQRSCreate(PQRSBase):
    pass


class PQRS(PQRSBase):
    id: int
    usuario_id: int
    estado: EstadoPqrsEnum = EstadoPqrsEnum.PENDIENTE
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)