from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioInDB
from app.models.usuario import Usuario as UsuarioModel
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_verification_token,
    verify_token
)
from app.repo.usuario import UsuarioRepository
from fastapi import HTTPException
from app.utils.claims import get_claims 


invalid_credentials = HTTPException(status_code=401, detail="Invalid credentials")
account_inactive = HTTPException(status_code=403, detail="Account is not active")
account_not_verified = HTTPException(status_code=403, detail="Account is not verified,check your email")




class UsuarioServices:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def login_user(self, email: str, password: str) -> str:
        db_usuario = self.repo.find_by_email(email)
        if not db_usuario:
            raise invalid_credentials
        if not verify_password(password, db_usuario.password):
            raise invalid_credentials
        if not db_usuario.activo:
            raise account_inactive
        if not db_usuario.is_verified:
            raise account_not_verified

        data = get_claims(db_usuario)
        token = create_access_token(data)
        return token

    async def register_user(self, usuario: UsuarioCreate) -> tuple[UsuarioInDB, str]:
        if self.repo.find_by_email(usuario.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        password_hash = hash_password(usuario.password)

        db_usuario = UsuarioModel(
            nombre=usuario.nombre,
            email=usuario.email,
            password=password_hash,
            activo=True,
            is_verified=False
        )

        created = self.repo.create(db_usuario)

        verification_token = create_verification_token(created.id)

        usuario_schema = UsuarioInDB.model_validate(created)
        return usuario_schema, verification_token

    def update_user(self, usuario_id: int, updates: UsuarioUpdate) -> UsuarioInDB:
        db_usuario = self.repo.get_by_id(usuario_id)
        if not db_usuario:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = updates.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        updated = self.repo.update(db_usuario, update_data)

        return UsuarioInDB.model_validate(updated)

    def activate_user(self, usuario_id: int) -> UsuarioInDB:
        db_usuario = self.repo.activate_user(usuario_id)
        if not db_usuario:
            raise HTTPException(status_code=404, detail="User not found")

        return UsuarioInDB.model_validate(db_usuario)
    
    def get_user_by_email(self, email: str) -> UsuarioInDB:
        db_usuario = self.repo.find_by_email(email)
        if not db_usuario:
            raise HTTPException(status_code=404, detail="User not found")
        return UsuarioInDB.model_validate(db_usuario)
        

    def reset_password(self, token: str, new_password: str):
    # 1. Validamos que el token sea de tipo password_reset
     payload = verify_token(token, expected_type="password_reset")
     user_id = payload.get("sub")
    
    # 2. Buscamos al usuario
     user = self.repo.get_by_id(user_id)
     if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Hasheamos la nueva clave y actualizamos
     new_hash = hash_password(new_password)
     self.repo.update(user, {"password": new_hash})
    
     return {"message": "password updated successfully"}

    # ------ métodos administrativos ------
    def list_users(self):
        """Retorna todos los usuarios junto con su rol."""
        return self.repo.list()

    def desactivar_usuario(self, usuario_id: int):
        user = self.repo.get_by_id(usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.activo = False
        self.repo.update(user, {"activo": False})
        return user