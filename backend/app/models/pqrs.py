from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.connection import Base

class PQR(Base):
    __tablename__ = 'pqrs'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    tipo = Column(Enum('Peticion', 'Queja', 'Reclamo', 'Sugerencia'), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(Enum('Pendiente', 'En proceso', 'Cerrado'), default='Pendiente')
    fecha_creacion = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    usuario = relationship("Usuario", back_populates="pqrs")