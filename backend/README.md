# Proyecto 2 SENA Backend

## Descripción
Este proyecto es un backend para un sistema inmobiliario desarrollado con FastAPI. Permite gestionar usuarios, lotes, compras, pagos y PQRS (Peticiones, Quejas, Reclamos y Sugerencias).

## Estructura del Proyecto
```
proyecto-inmobiliario
backend
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── usuarios.py
│   │   │   ├── lotes.py
│   │   │   ├── compras.py
│   │   │   ├── pagos.py
│   │   │   └── pqrs.py
│   │   └── dependencies.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── lote.py
│   │   ├── compra.py
│   │   ├── pago.py
│   │   └── pqrs.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── lote.py
│   │   ├── compra.py
│   │   ├── pago.py
│   │   └── pqrs.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── lote.py
│   │   ├── compra.py
│   │   ├── pago.py
│   │   └── pqrs.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   └── database
│       ├── __init__.py
│       └── connection.py
├── database
│   └── db.sql
├── requirements.txt
├── .env
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