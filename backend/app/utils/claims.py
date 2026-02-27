from app.models.usuario import Usuario


def get_claims(db_usuario: Usuario)-> dict:
    """
    Genera los claims para un token de acceso.
    """
    return {
        "sub": str(db_usuario.id),
        "email": db_usuario.email,
        "rol_id": db_usuario.rol_id,
        "type": "access",
    }

