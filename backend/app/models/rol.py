from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)

    # El back_populates apunta al NOMBRE DEL ATRIBUTO en la clase Usuario
    usuarios = relationship("Usuario", back_populates="rol")