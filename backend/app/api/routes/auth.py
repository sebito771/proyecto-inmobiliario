from fastapi import APIRouter, Depends, BackgroundTasks
from app.schemas.usuario import  UsuarioCreate, UsuarioLogin
from app.services.usuario import UsuarioServices
from app.services.email_services import send_verification_email
from app.core.security import get_current_user
from app.api.dependencies import get_usuario_service



router = APIRouter(prefix="/auth", tags=["auth"])

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
   data= get_current_user(token,"verification")
   usuario_id= data.get("sub")
   if not usuario_id:
      return {"message":"invalid token"}
   u=services.activate_user(usuario_id)
   return {"message":"account activated successfully", "user":u}
   
 
  


