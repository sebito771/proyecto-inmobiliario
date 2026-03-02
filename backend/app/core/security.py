from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings


# Security settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
VERIFICATION_TOKEN_EXPIRE_HOURS = 24  # tokens de verificación válidos 24 horas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==================== Password Functions ====================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ==================== Token Functions ====================
def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """Crea un token de acceso para operaciones normales."""
    to_encode = data.copy()
    to_encode["type"] = "access"
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_password_reset_token(usuario_id: int) -> str:
    """Crea un token de restablecimiento de contraseña."""
    to_encode = {
        "sub": str(usuario_id),
        "type": "password_reset",
    }
    expire = datetime.now(timezone.utc) + timedelta(hours=1)  #
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def create_verification_token(usuario_id: int) -> str:
    """Crea un token de verificación de email."""
    to_encode = {
        "sub": str(usuario_id),
        "type": "verification",
    }
    expire = datetime.now(timezone.utc) + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


    

def verify_token(
    token: str, expected_type: Literal["access", "verification","password_reset"]
) -> Dict:
    """
    Verifica un token y valida que sea del tipo esperado.
    
    :param token: el JWT a verificar
    :param expected_type: tipo de token esperado ("access" o "verification")
    :return: payload del token
    :raises HTTPException: si el token es inválido o de tipo incorrecto
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    invalid_type_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type. Expected {expected_type}",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        
        # validar el tipo de token
        if token_type != expected_type:
            raise invalid_type_exception
        
        if payload.get("sub") is None:
            raise credentials_exception

        
        return payload
    except JWTError:
        raise credentials_exception


from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.repo import UsuarioRepository
from app.models.usuario import Usuario as UsuarioModel


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UsuarioModel:
    """Obtiene el usuario actual desde un token de acceso y carga la entidad.

    Además verifica que la cuenta esté activa.
    """
    payload = verify_token(token, expected_type="access")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = UsuarioRepository(db).get_by_id(int(user_id))
    if not user or not user.activo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo o no existe")

    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UsuarioModel = Depends(get_current_user)) -> UsuarioModel:
        if current_user.rol.nombre not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")
        return current_user
