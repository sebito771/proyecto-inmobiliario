from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Lote(Base):
    __tablename__ = 'lotes'

    id = Column(Integer, primary_key=True, index=True)
    area_m2 = Column(Integer, nullable=False)
    ubicacion = Column(String(150), nullable=False)
    valor = Column(Numeric(12, 2), nullable=False)
    estado = Column(Enum('Disponible', 'Reservado', 'Vendido', name='estado_enum'), default='Disponible')
    etapa_id = Column(Integer, ForeignKey('etapas.id'), nullable=False)

    etapa = relationship("Etapa", back_populates="lotes")