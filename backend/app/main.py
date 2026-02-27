from fastapi import FastAPI
from app.api.routes import auth,usuarios, lotes, compras, pagos, pqrs

app = FastAPI()
#active
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#inactive
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(lotes.router, prefix="/lotes", tags=["lotes"])
app.include_router(compras.router, prefix="/compras", tags=["compras"])
app.include_router(pagos.router, prefix="/pagos", tags=["pagos"])
app.include_router(pqrs.router, prefix="/pqrs", tags=["pqrs"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inmobiliaria API"}