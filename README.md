# 🏠 Inmobiliaria API

Bienvenido al backend del sistema de gestión inmobiliaria. Este proyecto está diseñado para ofrecer una experiencia robusta, rápida y eficiente en la administración de inmuebles, abonos y atención al cliente.

## 🚀 Tecnologías Principales
- **Backend**: FastAPI (Python)
- **Base de Datos**: MySQL / SQLAlchemy
- **Seguridad**: OAuth2 con JWT
- **Notificaciones**: Mailjet API

## 📂 Estructura del Proyecto
```text
inmobiliaria-back/
├── backend/               # Código fuente del servidor
│   ├── app/               # Lógica central (API, Servicios, Modelos, Repositorios)
│   ├── database/          # Conexión y configuraciones de la base de datos
│   └── tests/             # Pruebas unitarias y de integración
├── docs/                  # Documentación técnica detallada
│   ├── 01_arquitectura_general.md
│   ├── 02_configuracion_y_seguridad.md
│   ├── 03_modelos_base_de_datos.md
│   ├── 04_repositorios.md
│   └── 05_servicios_y_logica.md
└── README.md              # Guía principal del proyecto
```

## 📖 Documentación Técnica
Hemos dividido la documentación en módulos lógicos para facilitar su lectura:

- 🏗️ [**Arquitectura General**](docs/01_arquitectura_general.md): Rutas, dependencias y estructura de carpetas.
- 🔐 [**Configuración y Seguridad**](docs/02_configuracion_y_seguridad.md): Manejo de variables de entorno y lógica de autenticación.
- 📊 [**Modelos de Base de Datos**](docs/03_modelos_base_de_datos.md): Entidades (Lotes, Pagos, Compras) y sus relaciones.
- 📦 [**Repositorios**](docs/04_repositorios.md): Abstracción de la capa de datos (Patrón Repositorio).
- ⚙️ [**Servicios y Lógica**](docs/05_servicios_y_logica.md): Procesamiento de abonos, gestión de lotes y correos automáticos.

---
*Este proyecto busca garantizar una experiencia de usuario fluida y procesos administrativos altamente eficientes.*
