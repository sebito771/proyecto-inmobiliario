from fastapi import FastAPI
from app.api.routes import auth , lote, pqrs, rol, detalle_compra
from dotenv import load_dotenv

# ,usuarios, , compras, pagos, 
load_dotenv()
app = FastAPI()
#active
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#inactive
#app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(lote.router, prefix="/lotes", tags=["lotes"])
app.include_router(pqrs.router, prefix="/pqrs", tags=["pqrs"])
app.include_router(rol.router, prefix="/roles", tags=["roles"])
app.include_router(detalle_compra.router, prefix="/detalle-compra", tags=["detalle_compra"])
# app.include_router(compras.router, prefix="/compras", tags=["compras"])
# app.include_router(pagos.router, prefix="/pagos", tags=["pagos"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inmobiliaria API"}