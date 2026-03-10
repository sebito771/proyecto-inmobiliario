import logging
import base64

from pathlib import Path
from datetime import datetime
from fastapi import BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from mailjet_rest import Client

from app.core.config import settings

logger = logging.getLogger(__name__)

# 1. Inicializar cliente de Mailjet
# Usa las credenciales de la configuración centralizada (config.py)
mailjet = Client(auth=(settings.MAILJET_USERNAME, settings.MAILJET_PASSWORD), version='v3.1')

BASE_URL = settings.BASE_URL
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "static" / "templates" / "email"


def _render_template(template_name: str, context: dict) -> str:
    """Carga y renderiza una plantilla HTML desde TEMPLATE_DIR."""
    template_path = TEMPLATE_DIR / template_name
    if not template_path.exists():
        logger.error(f"Email template not found: {template_path}")
        return f"<p>Error: Template {template_name} not found.</p>"
    html = template_path.read_text(encoding="utf-8")
    # Sustitución simple de variables {{ key }}
    for key, value in context.items():
        html = html.replace("{{ " + key + " }}", str(value))
    return html


def _send_mailjet_email(data: dict):
    """
    Función síncrona interna para enviar un email usando la API de Mailjet.
    Se ejecuta en un background task o en un thread pool para no bloquear.
    """
    try:
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            logger.info(f"Email sent successfully via Mailjet: {result.json().get('Messages', [])}")
        else:
            logger.error(f"Mailjet API Error: {result.status_code} - {result.json()}")
    except Exception as e:
        logger.error(f"Exception while sending email via Mailjet: {e}", exc_info=True)


async def send_email(
    to_email: str, subject: str, body: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """
    Envía un correo genérico usando la API de Mailjet de forma no bloqueante.
    """
    message_data = {
        'Messages': [{
            "From": {
                "Email": settings.MAIL_FROM,
                "Name": "Soporte Inmobiliaria",
            },
            "To": [{"Email": to_email}],
            "Subject": subject,
            "HTMLPart": body,
        }]
    }
    logger.info(f"Scheduling generic email to {to_email}")
    if background_tasks:
        background_tasks.add_task(_send_mailjet_email, message_data)
    else:
        # Si no hay background tasks, se ejecuta en un threadpool para no bloquear
        await run_in_threadpool(_send_mailjet_email, message_data)


async def send_verification_email(
    email: str, token: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """Envía un correo de verificación con plantilla HTML usando Mailjet."""
    verification_url = f"{BASE_URL}/static/verify.html?token={token}"
    body = _render_template(
        "verification.html",
        {"verification_url": verification_url, "year": datetime.now().year},
    )
    
    message_data = {
        'Messages': [{
            "From": {
                "Email": settings.MAIL_FROM,
                "Name": "Soporte Inmobiliaria"
            },
            "To": [{"Email": email}],
            "Subject": "Verifica tu cuenta",
            "HTMLPart": body
        }]
    }

    logger.info(f"Scheduling verification email to {email}")
    if background_tasks:
        background_tasks.add_task(_send_mailjet_email, message_data)
    else:
        await run_in_threadpool(_send_mailjet_email, message_data)


async def send_new_password_email(
    email: str, token: str, background_tasks: BackgroundTasks | None = None
) -> None:
    """Envía un correo de restablecimiento de contraseña con plantilla HTML usando Mailjet."""
    reset_url = f"{BASE_URL}/static/reset-password.html?token={token}"
    body = _render_template(
        "reset_password.html",
        {"reset_url": reset_url, "year": datetime.now().year},
    )
    
    message_data = {
        'Messages': [{
            "From": {
                "Email": settings.MAIL_FROM,
                "Name": "Soporte Inmobiliaria"
            },
            "To": [{"Email": email}],
            "Subject": "Restablecimiento de contraseña",
            "HTMLPart": body
        }]
    }

    logger.info(f"Scheduling password reset email to {email}")
    if background_tasks:
        background_tasks.add_task(_send_mailjet_email, message_data)
    else:
        await run_in_threadpool(_send_mailjet_email, message_data)


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
    """Envía un correo con el recibo PDF adjunto y cuerpo HTML desde plantilla usando Mailjet."""
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

    # Codificar el PDF en Base64 para la API de Mailjet
    base64_content = base64.b64encode(pdf_bytes).decode('utf-8')

    message_data = {
        'Messages': [{
            "From": {
                "Email": settings.MAIL_FROM,
                "Name": "Facturación Inmobiliaria"
            },
            "To": [{"Email": email}],
            "Subject": "Recibo de pago",
            "HTMLPart": body,
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": "recibo.pdf",
                "Base64Content": base64_content
            }]
        }]
    }

    logger.info(f"Scheduling receipt email to {email}")
    if background_tasks:
        background_tasks.add_task(_send_mailjet_email, message_data)
    else:
        await run_in_threadpool(_send_mailjet_email, message_data)
