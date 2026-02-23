import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
from typing import Generator


# 1. Asegurar el protocolo correcto para MySQL
url = settings.DATABASE_URL 
DATABASE_URL = os.getenv("DATABASE_URL", url)

# 2. Engine con Pool de Conexiones
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,  # Recicla conexiones cada hora para evitar cortes de MySQL
    pool_pre_ping=True,  # Verifica si la conexión está viva antes de usarla (MUY RECOMENDADO)
    echo=False           # Cambia a True si quieres ver el SQL real en consola (debug)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Base(DeclarativeBase):
    pass