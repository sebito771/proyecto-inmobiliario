import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# configuración a partir de variables de entorno (o .env)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER", ""),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD", ""),
    MAIL_FROM=os.getenv("SENDER_EMAIL", "no-reply@tuapp.com"),
    MAIL_PORT=int(os.getenv("SMTP_PORT", "25")),
    MAIL_SERVER=os.getenv("SMTP_HOST", "localhost"),
    MAIL_STARTTLS=bool(os.getenv("MAIL_STARTTLS", "True").lower() in ("true", "1")),
    MAIL_SSL_TLS=bool(os.getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1")),
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=None,  # no templates usados aquí
)


async def send_verification_email(
    email: str, token: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """Envía un correo de verificación usando fastapi-mail.

    :param email: dirección de destino
    :param token: token que se inserta en el enlace
    :param background_tasks: si se proporciona, el envío se programa en segundo plano
    """

    message = MessageSchema(
        subject="Verifica tu cuenta",
        recipients=[email],
        body=(
            f"<strong>Haz click aquí para verificar:</strong> "
            f"<a href=\"{BASE_URL}/auth/verify?token={token}\">Link</a>"
        ),
        subtype="html",
    )

    fm = FastMail(MAIL_CONFIG)
    if background_tasks:
        background_tasks.add_task(fm.send_message, message)
    else:
        await fm.send_message(message)

