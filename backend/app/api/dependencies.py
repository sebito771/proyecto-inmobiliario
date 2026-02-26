from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import hash_password

def get_current_user(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user_dependency(user: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = Usuario(nombre=user.nombre, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user