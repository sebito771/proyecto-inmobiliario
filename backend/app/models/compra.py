from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum
from datetime import datetime

class CompraEstado(enum.Enum):
    Activa = "Activa"
    Pagada = "Pagada"
    Cancelada = "Cancelada"

class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_compra = Column(DateTime, default=datetime.utcnow)
    total = Column(Numeric(12, 2), nullable=False)
    estado = Column(Enum(CompraEstado), default=CompraEstado.Activa)

    usuario = relationship("Usuario", back_populates="compras")
    detalle_compra = relationship("DetalleCompra", back_populates="compra")