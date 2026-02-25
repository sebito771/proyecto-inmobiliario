from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str
    rol_id: int

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None

class UsuarioInDB(UsuarioBase):
    id: int
    fecha_registro: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class Usuario(UsuarioInDB):
    pass