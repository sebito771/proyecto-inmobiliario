from fastapi import APIRouter, BackgroundTasks
from app.services.email_services import send_email

router = APIRouter()

@router.post("/send-email")
async def send_test_email(background_tasks: BackgroundTasks):

    await send_email(
        to_email="sebascova18@gmail.com",
        subject="Correo de prueba",
        body="<h1>Hola desde FastAPI</h1>",
        background_tasks=background_tasks
    )

    return {"message": "Email sending task has been scheduled"}
