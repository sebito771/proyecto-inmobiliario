from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str
    rol_id: int
    # 'activo' no se expone al cliente; siempre comienza en False

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None  # permite activar/desactivar manualmente

class UsuarioInDB(UsuarioBase):
    id: int
    fecha_registro: datetime
    activo: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )


class Usuario(UsuarioInDB):
    pass