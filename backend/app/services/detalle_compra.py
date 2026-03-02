from fastapi import HTTPException
from app.repo import DetalleRepository, CompraRepository, LoteRepository
from app.models.detalle_compra import DetalleCompra as DetalleCompraModel
from app.schemas.compra import DetalleCompraCreate


class DetalleCompraServices:
    def __init__(self, repo: DetalleRepository, compra_repo: CompraRepository, lote_repo: LoteRepository):
        self.repo = repo
        self.compra_repo = compra_repo
        self.lote_repo = lote_repo

    def get(self, detalle_id: int):
        """Obtiene un detalle de compra por ID."""
        detalle = self.repo.get_by_id(detalle_id)
        if not detalle:
            raise HTTPException(status_code=404, detail="DetalleCompra not found")
        return detalle

    def list_by_compra(self, compra_id: int):
        """Retorna todos los detalles de una compra."""
        compra = self.compra_repo.get_by_id(compra_id)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra not found")
        return self.repo.get_by_compra_id(compra_id)

    def create(self, datos: DetalleCompraCreate):
        """Crea un nuevo detalle de compra."""
        compra = self.compra_repo.get_by_id(datos.compra_id)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra not found")
        
        lote = self.lote_repo.get_by_id(datos.lote_id)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote not found")

        nuevo = DetalleCompraModel(
            compra_id=datos.compra_id,
            lote_id=datos.lote_id,
            precio=datos.precio
        )
        return self.repo.create(nuevo)
