# Proyecto 2 SENA Backend

## Descripción
Este proyecto es un backend para un sistema inmobiliario desarrollado con FastAPI. Permite gestionar usuarios, lotes, compras, pagos y PQRS (Peticiones, Quejas, Reclamos y Sugerencias).

## Estructura del Proyecto
```
backend
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── detalle_compra.py
│   │       ├── lote.py
│   │       ├── pago.py
│   │       ├── pqrs.py
│   │       ├── rol.py
│   │       └── usuarios.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── database
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── compra.py
│   │   ├── detalle_compra.py
│   │   ├── etapas.py
│   │   ├── lote.py
│   │   ├── pago.py
│   │   ├── pqrs.py
│   │   ├── rol.py
│   │   └── usuario.py
│   ├── repo
│   │   ├── __init__.py
│   │   ├── base_repo.py
│   │   ├── compra.py
│   │   ├── detalle_compra.py
│   │   ├── etapa.py
│   │   ├── lote.py
│   │   ├── pago.py
│   │   ├── pqrs.py
│   │   ├── rol.py
│   │   └── usuario.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── compra.py
│   │   ├── lote.py
│   │   ├── pago.py
│   │   ├── pqrs.py
│   │   └── usuario.py
│   └── services
│       ├── __init__.py
│       ├── detalle_compra.py
│       ├── email_services.py
│       ├── lote.py
│       ├── pago.py
│       ├── pqrs.py
│       ├── rol.py
│       └── usuario.py
├── database
│   ├── db.sql
│   └── seed.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Instalación
1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd proyecto-inmobiliario
   cd backend
   ```

2. Crea un entorno virtual y actívalo:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno en el archivo `.env`.


5. carga el sql en tu gestor de base de datos
### Creacion de la base de datos
```bash
backend/database/db.sql 
```
### Carga de seed para la base de datos
```bash
backend/database/seed.py
py seed.py 
```

## Uso
Para iniciar el servidor, ejecuta:
```
uvicorn app.main:app --reload
```

Accede a la documentación de la API en `http://localhost:8000/docs`.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cambios.

## Licencia
Este proyecto está bajo la Licencia MIT.