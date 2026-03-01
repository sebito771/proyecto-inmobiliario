from app.repo import LoteRepository , UsuarioRepository , CompraRepository , DetalleRepository, EtapaRepository
from app.schemas.lote import LoteSell , LoteCreate , LoteUpdate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import compra as CompraModel , lote as LoteModel , detalle_compra as DetalleModel 
from datetime import datetime, timedelta


class LoteServices:
    def __init__(
                  self,repo:LoteRepository,
                  user_repo:UsuarioRepository,
                  compra_repo: CompraRepository,
                  detalle_repo: DetalleRepository,
                  etapa_repo: EtapaRepository,
                  db: Session
                 ):
        self.repo=repo
        self.user_repo=user_repo
        self.compra_repo=compra_repo
        self.detalle_repo=detalle_repo
        self.etapa_repo=etapa_repo
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
        self._clean_expired_purchases()
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
                compradb = self.compra_repo.create_without_commit(nueva_compra)

             
                for lote in valid_lotes:
                    detalle = DetalleModel(
                        compra_id=compradb.id,
                        lote_id=lote.id,
                        precio=lote.valor
                    )
                    self.detalle_repo.create_without_commit(detalle)

                    #  Actualización estratégica: Reservado
                    self.repo.update(lote, {"estado": "Reservado"})

            return compradb

        except Exception as e:
            # Si algo falla, SQLAlchemy hace rollback automáticamente
            raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")
        
    def create_lote(self, lote_data: LoteCreate):
    # 1. Verificar si la etapa existe 🔍
     etapa =  self.etapa_repo.get_by_id(lote_data.etapa_id)
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
    
    def update_lote(self, lote_id: int, updates: LoteUpdate):
       lote= self.repo.get_by_id(lote_id)
       if not lote:
            raise HTTPException(status_code=404, detail="Lote no encontrado")
       
       update_data = updates.model_dump(exclude_unset=True)
       self.repo.update(lote, update_data)
       return lote
       
     

    def list_lotes(self, estado: str = None, etapa_id: int = None):
     """
    Lista los lotes con filtros opcionales por estado y etapa. 🔍
     """
     self._clean_expired_purchases()
    # verificamos que exista la etapa
     if etapa_id:
        etapa = self.etapa_repo.get_by_id(etapa_id)
        if not etapa:
            raise HTTPException(status_code=404, detail="Etapa no encontrada")
     
     return self.repo.list_filtered(estado, etapa_id)
    
   
    def _clean_expired_purchases(self):
     """
    Busca todas las compras expiradas usando el repo y las cancela.
     """
     ahora = datetime.now(datetime.timezone.utc)
    
    # 1. Usamos el repo para traer solo las que debemos limpiar
     expired_purchases = self.compra_repo.get_expired_active(ahora)

     if not expired_purchases:
        return 


     try:
        with self.db.begin():
            for compra in expired_purchases:
                #  Obtenemos detalles mediante el repo de detalles
                detalles = self.detalle_repo.get_by_compra_id(compra.id)
                
                for item in detalles:
                    lote = self.repo.get_by_id(item.lote_id)
                    if lote and lote.estado == "Reservado":
                  
                        self.repo.update_without_commit(lote, {"estado": "Disponible"})
                
                # 4. Cancelamos la compra
                self.compra_repo.update_without_commit(compra, {"estado": "Cancelada"})
                
     except Exception as e:
        # Aquí puedes loguear el error, pero no bloqueamos al usuario
        print(f"Error en auto-limpieza: {e}")
