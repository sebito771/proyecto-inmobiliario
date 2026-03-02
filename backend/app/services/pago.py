from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from io import BytesIO
from fpdf import FPDF

from app.repo import PagoRepository, CompraRepository, DetalleRepository, LoteRepository, UsuarioRepository
from app.models.pago import Pago as PagoModel
from app.schemas.pago import PagoCreate
from app.services.email_services import send_receipt_email


class PagoServices:
    def __init__(
        self,
        repo: PagoRepository,
        compra_repo: CompraRepository,
        detalle_repo: DetalleRepository,
        lote_repo: LoteRepository,
        user_repo: UsuarioRepository,
        db: Session,
    ):
        self.repo = repo
        self.compra_repo = compra_repo
        self.detalle_repo = detalle_repo
        self.lote_repo = lote_repo
        self.user_repo = user_repo
        self.db = db

    def _generate_pdf(self, pago: PagoModel) -> BytesIO:
        """Arma un PDF simple con los datos del pago y lo devuelve en memoria."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"Recibo de pago #{pago.id}", ln=True)
        pdf.cell(0, 10, txt=f"Compra: {pago.compra_id}", ln=True)
        pdf.cell(0, 10, txt=f"Valor pagado: {pago.valor_pagado}", ln=True)
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    def registrar_abono(
        self,
        data: PagoCreate,
        background_tasks: BackgroundTasks | None = None,
    ):
        """Registra un pago sobre una compra y actualiza pendiente/estado.

        Realiza todas las operaciones dentro de una transacción.
        Genera un PDF y programa el envío por correo.
        """
        compra = self.compra_repo.get_by_id(data.compra_id)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra not found")

        # validaciones
        if data.valor_pagado > compra.pendiente:
            raise HTTPException(status_code=400, detail="Abono mayor al pendiente")

        pendiente_inicial = float(compra.pendiente)

        try:
            with self.db.begin():
                pago = PagoModel(
                    compra_id=data.compra_id,
                    valor_pagado=data.valor_pagado,
                    comprobante=data.comprobante,
                )
                # se utiliza create_without_commit para manejar transacción externa
                self.repo.create_without_commit(pago)

                compra.pendiente = compra.pendiente - data.valor_pagado
                if compra.pendiente <= 0:
                    compra.estado = "Pagada"

                # primer pago -> actualizar lotes a 'Vendido'
                if pendiente_inicial == float(compra.total):
                    detalles = self.detalle_repo.get_by_compra_id(compra.id)
                    for detalle in detalles:
                        lote = self.lote_repo.get_by_id(detalle.lote_id)
                        if lote and lote.estado != "Vendido":
                            lote.estado = "Vendido"

                # al usar db.begin(), los objetos se comitean al salir
                self.db.flush()

            # refrescar pago y compra
            self.db.refresh(pago)
            self.db.refresh(compra)
        except Exception as e:
            # cualquier fallo revierte automáticamente, pero devolvemos HTTP
            raise HTTPException(status_code=500, detail=f"Error registrando abono: {e}")

        # generar pdf y enviar por correo en background
        receipt = self._generate_pdf(pago)
        usuario = self.user_repo.get_by_id(compra.usuario_id)
        if usuario:
            # convertimos a bytes por si devuelve BytesIO
            pdf_bytes = receipt.getvalue() if hasattr(receipt, "getvalue") else receipt
            if background_tasks:
                background_tasks.add_task(send_receipt_email, usuario.email, pdf_bytes)
            else:
                # no hay tasks, enviamos sincrónicamente
                import asyncio

                asyncio.create_task(send_receipt_email(usuario.email, pdf_bytes))

        return pago

    def get_resumen_compra(self, compra_id: int):
        """Retorna {total_compra, total_pagado, saldo_pendiente}."""
        compra = self.compra_repo.get_by_id(compra_id)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra not found")
        return {
            "total_compra": float(compra.total),
            "total_pagado": float(compra.total) - float(compra.pendiente),
            "saldo_pendiente": float(compra.pendiente),
        }
