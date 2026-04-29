# 04. Repositorios (Capa de Acceso a Datos)

El proyecto implementa el **Patrón Repositorio** para abstraer las consultas de SQLAlchemy de la lógica de negocio.

## 4.1. BaseRepository
Clase genérica que provee operaciones CRUD estándar:
- `get_by_id(id)`
- `list()`
- `create(obj)` / `create_without_commit(obj)`
- `update(id, data)`
- `delete(id)`

## 4.2. Repositorios Específicos

| Repositorio | Métodos Personalizados |
| :--- | :--- |
| `UsuarioRepository` | `find_by_email`, `activate_user` |
| `CompraRepository` | `get_expired_active`, `get_by_usuario_id` |
| `LoteRepository` | `list_filtered` (por etapa/estado), `get_by_compra_id` |
| `RolRepository` | `find_by_name` |
| `PqrsRepository` | `list_by_usuario` |
| `PagoRepository` | `get_by_compra_id` |

---

## 4.3. Guía de Uso
Para interactuar con la base de datos, siempre se debe instanciar el repositorio dentro de un bloque de sesión:

```python
# Ejemplo de uso en un servicio
lote_repo = LoteRepository(db_session)
lotes_disponibles = lote_repo.list_filtered(estado="Disponible")
```
