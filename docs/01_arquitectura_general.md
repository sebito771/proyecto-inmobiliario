# 01. Arquitectura General del Proyecto

Esta sección describe la estructura básica de la aplicación, las rutas de la API y las dependencias principales.

## 1.1. Punto de Entrada (main.py)
La aplicación utiliza **FastAPI** como framework principal.

### Configuración de la Aplicación
- **CORS**: Configurado para permitir todos los orígenes (`*`).
- **Archivos Estáticos**: Montados en `/static` (directorio `app/static`).

### Rutas Principales (Routers)
| Prefijo | Tag | Descripción |
| :--- | :--- | :--- |
| `/auth` | auth | Gestión de sesiones y tokens |
| `/email` | email | Endpoints de prueba/envío de correos |
| `/lotes` | lotes | Gestión de inventario de lotes |
| `/pqrs` | pqrs | Peticiones, Quejas, Reclamos y Sugerencias |
| `/roles` | roles | Gestión de roles de usuario |
| `/detalle-compra` | detalle_compra | Detalles de transacciones |
| `/pagos` | pagos | Registro y consulta de abonos |
| `/usuarios` | usuarios | Administración de usuarios |

## 1.2. Inyección de Dependencias (dependencies.py)
Se utiliza un sistema de dependencias para proveer los servicios a los endpoints, asegurando que cada uno reciba su repositorio y la sesión de base de datos correspondiente.

### Servicios Disponibles
- `get_usuario_service`
- `get_lote_service`
- `get_pqrs_service`
- `get_rol_service`
- `get_detalle_compra_service`
- `get_pago_service`

---

## 1.3. Componentes y Servicios (Resumen)
| Nombre | Responsabilidad |
| --- | --- |
| `auth` | Autenticación y seguridad. |
| `lote` | Gestión del inventario y estados. |
| `pqrs` | Flujo de atención al cliente. |
| `pago` | Procesamiento de abonos y generación de recibos. |
