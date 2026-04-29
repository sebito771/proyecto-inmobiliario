# 02. Configuración y Seguridad

Detalles sobre la configuración del entorno y los mecanismos de protección de la API.

## 2.1. Configuración de la Aplicación (app.core.config)
Se utiliza `pydantic_settings` para cargar variables desde un archivo `.env`.

### Variables Clave
- `DATABASE_URL`: Conexión a la base de datos.
- `SECRET_KEY`: Clave para firma de tokens JWT.
- `ALGORITHM`: Por defecto `HS256`.
- `MAILJET_API`: Credenciales para el servicio de correo.

## 2.2. Autenticación y Tokens (app.core.auth)
La seguridad se basa en **OAuth2 con JWT**.

### Funcionalidades de Seguridad
- **Hash de Contraseñas**: Implementado con `CryptContext` (bcrypt).
- **Generación de Tokens**:
  - Access Tokens (Expiración configurable).
  - Password Reset Tokens.
  - Verification Tokens (Email).
- **Verificación de Roles**: Clase `RoleChecker` para proteger rutas (ej. `admin_only`).

### Manejo de Excepciones de Seguridad
| Estado | Error | Causa |
| :--- | :--- | :--- |
| 401 | `credentials_exception` | Token inválido o expirado. |
| 403 | `HTTPException` | El usuario no tiene el rol necesario. |

---

## 2.3. Reglas de Autenticación
1. Los tokens deben ser verificados en cada petición protegida.
2. Los roles se validan antes de ejecutar la lógica del endpoint.
3. Las cuentas deben estar activas y verificadas para realizar operaciones sensibles.
