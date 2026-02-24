from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Pago(Base):
    __tablename__ = 'pagos'

    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey('compras.id'), nullable=False)
    fecha_pago = Column(TIMESTAMP, nullable=False)
    valor_pagado = Column(Numeric(12, 2), nullable=False)
    comprobante = Column(String(255), nullable=True)

    compra = relationship("Compra", back_populates="pagos")