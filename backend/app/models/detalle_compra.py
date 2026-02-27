from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.connection import Base

class DetalleCompra(Base):
    __tablename__ = 'detalle_compra'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey('compras.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lote_id = Column(Integer, ForeignKey('lotes.id', ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    precio = Column(Numeric(12, 2), nullable=False)

    # Relaciones para navegar fácilmente entre objetos
    compra = relationship("Compra", back_populates="detalle_compra")
    lote = relationship("Lote")