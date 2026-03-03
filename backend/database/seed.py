from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta

# =========================
# CONFIGURACIÓN
# =========================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# =========================
# SEED
# =========================
with engine.connect() as conn:
    with conn.begin():

        # ROLES
        conn.execute(text("""
            INSERT INTO roles (nombre) VALUES 
            ('Administrador'),
            ('Cliente')
        """))

        # USUARIOS (con hash real)
        admin_password = hash_password("admin123")
        juan_password = hash_password("juan123")
        maria_password = hash_password("maria123")

        conn.execute(text("""
            INSERT INTO usuarios 
            (nombre, email, password, rol_id, activo, is_verified)
            VALUES
            (:n1, :e1, :p1, 1, TRUE, TRUE),
            (:n2, :e2, :p2, 2, TRUE, TRUE),
            (:n3, :e3, :p3, 2, TRUE, TRUE)
        """), {
            "n1": "Admin Sistema",
            "e1": "admin@inmobiliaria.com",
            "p1": admin_password,
            "n2": "Juan Perez",
            "e2": "juan@email.com",
            "p2": juan_password,
            "n3": "Maria Lopez",
            "e3": "maria@email.com",
            "p3": maria_password,
        })

        # ETAPAS
        conn.execute(text("""
            INSERT INTO etapas (nombre, descripcion) VALUES
            ('Lanzamiento','Inicio oficial del proyecto'),
            ('Preventa','Venta anticipada de lotes'),
            ('Construccion','Etapa de construcción'),
            ('Entrega','Entrega formal al propietario')
        """))

        # LOTES
        conn.execute(text("""
            INSERT INTO lotes (area_m2, ubicacion, valor, etapa_id) VALUES
            (120,'Sector Norte',45000000,1),
            (150,'Sector Sur',60000000,2),
            (180,'Sector Este',75000000,3),
            (200,'Sector Oeste',90000000,4)
        """))

        # COMPRAS
        fecha_exp = datetime.now() + timedelta(days=30)

        conn.execute(text("""
            INSERT INTO compras (usuario_id, total, pendiente, fecha_expiracion)
            VALUES
            (2,45000000,45000000,:fecha_exp),
            (3,60000000,60000000,:fecha_exp)
        """), {"fecha_exp": fecha_exp})

        # DETALLE COMPRA
        conn.execute(text("""
            INSERT INTO detalle_compra (compra_id, lote_id, precio) VALUES
            (1,1,45000000),
            (2,2,60000000)
        """))

        # ACTUALIZAR LOTES
        conn.execute(text("""
            UPDATE lotes SET estado='Vendido' WHERE id IN (1,2)
        """))

        # PAGOS
        conn.execute(text("""
            INSERT INTO pagos (compra_id, valor_pagado, comprobante) VALUES
            (1,10000000,'pago1.pdf'),
            (1,15000000,'pago2.pdf'),
            (2,20000000,'pago3.pdf')
        """))

        # PQRS
        conn.execute(text("""
            INSERT INTO pqrs (usuario_id, tipo, descripcion) VALUES
            (2,'Peticion','Solicito informacion sobre mi saldo'),
            (3,'Queja','No he recibido mi comprobante')
        """))

print("🌱 Base de datos sembrada correctamente con contraseñas seguras")