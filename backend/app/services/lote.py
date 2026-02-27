from app.repo import LoteRepository , UsuarioRepository , CompraRepository , DetalleRepository
from app.schemas.lote import LoteSell , LoteCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import compra as CompraModel , lote as LoteModel , detalle_compra as DetalleModel , etapa as Etapa
from app.models.etapas import Etapa
from datetime import datetime, timedelta






class LoteServices:
    def __init__(
                  self,repo:LoteRepository,
                  user_repo:UsuarioRepository,
                  compra_repo: CompraRepository,
                  detalle_repo: DetalleRepository,
                  db: Session
                 ):
        self.repo=repo
        self.user_repo=user_repo
        self.compra_repo=compra_repo
        self.detalle_repo=detalle_repo
        self.db=db

    def buy_lote(self, sell: LoteSell):
        """
        Realiza la compra de lotes y los deja en estado 'Reservado' 🟡
        """
        valid_lotes = []
        
        # 1. Verificación del Usuario 👤
        user = self.user_repo.find_by_id(sell.usuario_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.activo:
            raise HTTPException(status_code=400, detail="User not active")

        # 2. Verificación de Disponibilidad 🏗️
        for lote_id in sell.lote_id:
            lote = self.repo.get_by_id(lote_id)
            if not lote:
                raise HTTPException(status_code=404, detail=f"Lote {lote_id} not found")
            if lote.estado != "Disponible":
                raise HTTPException(status_code=400, detail=f"Lote {lote_id} not available")
            valid_lotes.append(lote)

        # 3. Cálculo del Total 💰
        total = sum(lote.valor for lote in valid_lotes)

        try:
            # ⚛️ Iniciamos la transacción: Todo o Nada
            with self.db.begin():
                # Crear la cabecera de la compra 🧾
                ahora = datetime.now(datetime.timezone.utc)
                expiracion = ahora + timedelta(hours=24)
                nueva_compra = CompraModel(
                    usuario_id=sell.usuario_id,
                    total=total,
                    fecha_compra=ahora,
                    fecha_expiracion=expiracion,
                    estado="Activa"
                )
                compradb = self.compra_repo.create(nueva_compra)

             
                for lote in valid_lotes:
                    detalle = DetalleModel(
                        compra_id=compradb.id,
                        lote_id=lote.id,
                        precio=lote.valor
                    )
                    self.detalle_repo.create(detalle)

                    #  Actualización estratégica: Reservado
                    self.repo.update(lote, {"estado": "Reservado"})

            return compradb

        except Exception as e:
            # Si algo falla, SQLAlchemy hace rollback automáticamente
            raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")
        
    def create_lote(self, lote_data: LoteCreate):
    # 1. Verificar si la etapa existe 🔍
     etapa = self.db.query(Etapa).filter(Etapa.id == lote_data.etapa_id).first()
     if not etapa:
        raise HTTPException(status_code=404, detail="La etapa especificada no existe")

    # 2. Crear la instancia del modelo
     nuevo_lote = LoteModel(
        area_m2=lote_data.area_m2,
        ubicacion=lote_data.ubicacion,
        valor=lote_data.valor,
        etapa_id=lote_data.etapa_id,
        estado='Disponible' # Estado inicial por defecto 🟢
    )
     self.repo.create(nuevo_lote)
     return nuevo_lote
    

    def list_lotes(self, estado: str = None, etapa_id: int = None):
     """
    Lista los lotes con filtros opcionales por estado y etapa. 🔍
     """
    # Empezamos con la consulta base
     query = self.db.query(LoteModel)

    # Si nos pasan un estado (ej: 'Disponible'), filtramos por él 🟢
     if estado:
        query = query.filter(LoteModel.estado == estado)

    # Si nos pasan una etapa, filtramos por ella 🚩
     if etapa_id:
        query = query.filter(LoteModel.etapa_id == etapa_id)

     return query.all()


