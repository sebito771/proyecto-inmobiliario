from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import auth , lote, pqrs, rol, detalle_compra, pago, usuarios, email
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# ,usuarios, , compras, pagos, 
load_dotenv()
app = FastAPI()

# Servir archivos estáticos (páginas de verificación / reset password)
app.mount("/static", StaticFiles(directory="app/static"), name="static")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lista de URLs permitidas
    allow_credentials=False,  # si quieres enviar cookies
    allow_methods=["*"],     # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # Headers permitidos
)

#active
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#inactive
#app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(email.router, prefix="/email",tags=["email"])
app.include_router(lote.router, prefix="/lotes", tags=["lotes"])
app.include_router(pqrs.router, prefix="/pqrs", tags=["pqrs"])
app.include_router(rol.router, prefix="/roles", tags=["roles"])
app.include_router(detalle_compra.router, prefix="/detalle-compra", tags=["detalle_compra"])
app.include_router(pago.router, prefix="/pagos", tags=["pagos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
# app.include_router(compras.router, prefix="/compras", tags=["compras"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inmobiliaria API"}