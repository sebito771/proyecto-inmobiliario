from sqlalchemy import Column, Integer, String
from app.database.connection import Base
from sqlalchemy.orm import relationship



class Etapa(Base):
    __tablename__ = 'etapas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String, nullable=True) # Usamos String para el tipo TEXT

    # Relación inversa: Una etapa tiene muchos lotes 🏡
    lotes = relationship("Lote", back_populates="etapa")