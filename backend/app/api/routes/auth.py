from fastapi import APIRouter, Depends, BackgroundTasks , HTTPException
from app.schemas.usuario import  UsuarioCreate, UsuarioLogin , UsuarioResetPassword
from app.services.usuario import UsuarioServices
from app.services.email_services import send_verification_email, send_new_password_email
from app.core.security import  create_password_reset_token, verify_token
from app.api.dependencies import get_usuario_service



router = APIRouter( tags=["auth"])

@router.post("/login")
def Login(u: UsuarioLogin,services: UsuarioServices = Depends(get_usuario_service)):
  tk= services.login_user(u.email, u.password)
  return {"login successfuly":tk}

@router.post("/register")
async def Register(u:UsuarioCreate, background_tasks: BackgroundTasks, services: UsuarioServices = Depends(get_usuario_service)):
  usuario, token = await services.register_user(u)
  await send_verification_email(usuario.email, token, background_tasks=background_tasks)
  return {"message":"registered successfully", "tip":"check your email to verify your account"}

@router.post("/verify")
def activate(token: str, services: UsuarioServices = Depends(get_usuario_service)):
   data = verify_token(token, expected_type="verification")
   usuario_id = data.get("sub")
   if not usuario_id:
      raise HTTPException(status_code=400, detail="Invalid token")
   u=services.activate_user(usuario_id)
   return {"message":"account verified successfully", "user":u}

@router.post("/forgot-password")
async def forgot_password( email: str,   bt: BackgroundTasks,  services: UsuarioServices = Depends(get_usuario_service)):
      try:
        user = services.get_user_by_email(email) 
        token = create_password_reset_token(user.id) 

        await send_new_password_email(email, token, background_tasks=bt)
    
      except HTTPException as e:
         if e.status_code != 404:
            raise e
      return {"msg": "check your email to reset your password"}

@router.post("/reset-password")
def reset_password(u: UsuarioResetPassword, services: UsuarioServices= Depends(get_usuario_service)):
   return services.reset_password(u.token,u.new_password)

@router.post("/resend-verification")
async def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    services: UsuarioServices = Depends(get_usuario_service),
):
    """Reenvía el correo de verificación al usuario."""
    try:
        token = await services.retry_verification(email)
        await send_verification_email(email, token, background_tasks=background_tasks)
    except HTTPException as e:
        if e.status_code == 404:
            # No revelar si el usuario existe o no
            return {"message": "If the email exists, a verification link has been sent"}
        raise e
    return {"message": "Verification email sent if account exists and is not verified"}

                
   
   
 
  
