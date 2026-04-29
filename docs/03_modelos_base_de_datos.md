# 03. Modelos de Base de Datos

Definición de tablas, relaciones y lógica central de persistencia mediante **SQLAlchemy**.

## 3.1. Conexión (app.database.connection)
- **Motor**: SQLAlchemy `create_engine`.
- **Reciclaje**: Conexiones se reciclan cada 3600s para evitar cortes (especialmente en MySQL).
- **SessionLocal**: Sesión configurada con `autocommit=False`.

## 3.2. Modelos Principales

### Lote
- **Tabla**: `lotes`
- **Campos Clave**: `id`, `area_m2`, `valor`, `estado_enum`.
- **Estados**: `Disponible`, `Reservado`, `Vendido`.
- **Relaciones**: Pertenece a una `Etapa`.

### Compra
- **Tabla**: `compras`
- **Campos Clave**: `id`, `total`, `pendiente`, `estado`.
- **Estados**: `Activa`, `Pagada`, `Cancelada`.
- **Relaciones**: Vinculada a un `Usuario` y tiene múltiples `DetalleCompra`.

### Pago
- **Tabla**: `pagos`
- **Campos Clave**: `id`, `valor_pagado`, `fecha_pago`, `comprobante` (URL/Ruta).
- **Relaciones**: Vinculado a una `Compra`.

### PQRS
- **Tabla**: `pqrs`
- **Campos Clave**: `id`, `tipo` (Petición, Queja, etc), `estado` (Pendiente, Cerrado), `descripcion`.
- **Relaciones**: Pertenece a un `Usuario`.

---

## 3.3. Lógica de Modelos
- **Fechas**: Uso de `datetime.now(timezone.utc)` para auditoría automática.
- **Decimales**: Los campos financieros (`total`, `valor_pagado`) usan `Numeric(12, 2)` para precisión.
- **Cascadas**: Eliminación de una `Compra` elimina sus `DetalleCompra` asociados.
