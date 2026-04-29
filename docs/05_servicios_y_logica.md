# 05. Servicios y Lógica de Negocio

Aquí se concentra la complejidad de la aplicación, coordinando repositorios, validaciones y servicios externos.

## 5.1. LoteServices (Gestión de Ventas)
Es el servicio más crítico. Maneja el flujo de reserva y compra.

### Operaciones Clave
- **`buy_lote`**: 
  1. Valida usuario activo.
  2. Limpia compras expiradas (`_clean_expired_purchases`).
  3. Verifica disponibilidad de lotes seleccionados.
  4. Crea la compra y cambia estado de lotes a `Reservado`.
- **`delete_lote`**: Valida que el lote no tenga ventas asociadas antes de permitir el borrado.

## 5.2. PagoServices (Procesamiento de Abonos)
Coordina el registro financiero y la generación de documentos.

### Flujo de Registro (`registrar_abono`)
1. Valida si el abono supera la deuda pendiente.
2. Crea el registro en `pagos`.
3. Actualiza el `pendiente` en la `compra`.
4. Si se salda la deuda, marca los lotes como `Vendido` y la compra como `Pagada`.
5. **Genera PDF**: Crea un recibo usando la librería `FPDF`.
6. **Notifica**: Envía el recibo por email (Mailjet) usando una `BackgroundTask`.

## 5.3. EmailServices (Notificaciones)
Integración con la API de **Mailjet**.

### Funciones Disponibles
- `send_verification_email`: Para activación de cuenta.
- `send_new_password_email`: Para recuperación de acceso.
- `send_receipt_email`: Adjunta el PDF del abono en Base64.

## 5.4. UsuarioServices (Auth)
- `login_user`: Valida contraseña y devuelve token.
- `register_user`: Crea el usuario inactivo y dispara el email de verificación.

---

## 5.5. Matriz de Errores Comunes
| Código | Mensaje / Razón |
| :--- | :--- |
| 400 | `Lote {id} no disponible` |
| 400 | `Abono mayor al pendiente` |
| 404 | `Compra not found` |
| 401 | `invalid_credentials` |
