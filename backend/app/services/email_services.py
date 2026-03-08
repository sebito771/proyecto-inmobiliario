import os
from io import BytesIO
from pathlib import Path
from datetime import datetime
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.datastructures import UploadFile
import dotenv

dotenv.load_dotenv()

# configuración a partir de variables de entorno (o .env)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "static" / "templates" / "email"

MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "no-reply@tuapp.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "25")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "localhost"),
    MAIL_STARTTLS=bool(os.getenv("MAIL_STARTTLS", "True").lower() in ("true", "1")),
    MAIL_SSL_TLS=bool(os.getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1")),
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=None,  # renderizado manual con Jinja2
)


def _render_template(template_name: str, context: dict) -> str:
    """Carga y renderiza una plantilla HTML desde TEMPLATE_DIR."""
    template_path = TEMPLATE_DIR / template_name
    html = template_path.read_text(encoding="utf-8")
    # Sustitución simple de variables {{ key }}
    for key, value in context.items():
        html = html.replace("{{ " + key + " }}", str(value))
    return html


async def send_verification_email(
    email: str, token: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """Envía un correo de verificación con plantilla HTML."""
    verification_url = f"{BASE_URL}/static/verify.html?token={token}"
    body = _render_template(
        "verification.html",
        {"verification_url": verification_url, "year": datetime.now().year},
    )
    message = MessageSchema(
        subject="Verifica tu cuenta",
        recipients=[email],
        body=body,
        subtype="html",
    )
    fm = FastMail(MAIL_CONFIG)
    if background_tasks:
        background_tasks.add_task(fm.send_message, message)
    else:
        await fm.send_message(message)


async def send_new_password_email(
    email: str, token: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """Envía un correo de restablecimiento de contraseña con plantilla HTML."""
    reset_url = f"{BASE_URL}/static/reset-password.html?token={token}"
    body = _render_template(
        "reset_password.html",
        {"reset_url": reset_url, "year": datetime.now().year},
    )
    message = MessageSchema(
        subject="Nueva contraseña",
        recipients=[email],
        body=body,
        subtype="html",
    )
    fm = FastMail(MAIL_CONFIG)
    if background_tasks:
        background_tasks.add_task(fm.send_message, message)
    else:
        await fm.send_message(message)


async def send_receipt_email(
    email: str,
    pdf_bytes: bytes,
    background_tasks: BackgroundTasks | None = None,
    *,
    nombre: str = "",
    referencia: str = "",
    fecha: str = "",
    monto: str = "",
    lote: str = "",
) -> None:
    """Envía un correo con el recibo PDF adjunto y cuerpo HTML desde plantilla."""
    body = _render_template(
        "receipt.html",
        {
            "nombre": nombre,
            "referencia": referencia,
            "fecha": fecha or datetime.now().strftime("%d/%m/%Y"),
            "monto": monto,
            "lote": lote,
            "year": datetime.now().year,
        },
    )
    pdf_io = BytesIO(pdf_bytes) if isinstance(pdf_bytes, bytes) else pdf_bytes
    upload = UploadFile(filename="recibo.pdf", file=pdf_io)
    message = MessageSchema(
        subject="Recibo de pago",
        recipients=[email],
        body=body,
        subtype="html",
        attachments=[upload],
    )
    fm = FastMail(MAIL_CONFIG)
    if background_tasks:
        background_tasks.add_task(fm.send_message, message)
    else:
        await fm.send_message(message)
