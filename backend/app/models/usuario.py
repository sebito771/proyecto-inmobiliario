from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP , Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False, default=2)
    fecha_registro = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    # El back_populates apunta al NOMBRE DEL ATRIBUTO en la clase Rol
    rol = relationship("Rol", back_populates="usuarios")
    
    # Asegúrate de que Compra también tenga back_populates="usuario" (minúscula)
    compras = relationship("Compra", back_populates="usuario")
    pqrs = relationship("PQR", back_populates="usuario")