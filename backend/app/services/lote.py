from app.repo import LoteRepository , UsuarioRepository , CompraRepository , DetalleRepository, EtapaRepository
from app.schemas.lote import LoteSell , LoteCreate , LoteUpdate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Compra as CompraModel , Lote as LoteModel , DetalleCompra as DetalleModel 
from datetime import datetime, timedelta , timezone



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
    
    # 1. Verificaciones previas (Usuario y Disponibilidad) 👤
     user = self.user_repo.get_by_id(sell.usuario_id)
     if not user or not user.activo:
            raise HTTPException(status_code=400, detail="inactive user")

    # Ejecutamos la limpieza antes de la lógica principal
     self._clean_expired_purchases()

     # Evitar duplicados si el usuario envía el mismo ID varias veces
     unique_lote_ids = list(set(sell.lote_id))

     for lote_id in unique_lote_ids:
        lote = self.repo.get_by_id(lote_id)
        if not lote or lote.estado != "Disponible":
            raise HTTPException(status_code=400, detail=f"Lote {lote_id} no disponible")
        valid_lotes.append(lote)

     total = sum(lote.valor for lote in valid_lotes)

     try:
        # --- INICIO DEL BLOQUE ATÓMICO ---
        ahora = datetime.now(timezone.utc)
        expiracion = ahora + timedelta(hours=24)
        nueva_compra = CompraModel(
            usuario_id=sell.usuario_id,
            total=total,
            pendiente=total,
            fecha_compra=ahora,
            fecha_expiracion=expiracion,
            estado="Activa"
        )
   
        compradb = self.compra_repo.create_without_commit(nueva_compra)
        
        # B. Forzar el envío a la DB para obtener el ID de la compra 🆔
        # Esto permite que los detalles tengan el ID de compra sin cerrar la transacción.
        self.db.flush()

        # C. Crear los detalles y actualizar lotes 🔄
        for lote in valid_lotes:
            detalle = DetalleModel(
                compra_id=compradb.id,
                lote_id=lote.id,
                precio=lote.valor
            )
            self.detalle_repo.create_without_commit(detalle)
            self.repo.update_without_commit(lote, {"estado": "Reservado"})

        # D. CIERRE ATÓMICO: Si llegamos aquí, todo está bien.
        self.db.commit() 
        self.db.refresh(compradb)
        return compradb

     except Exception as e:
        # Si CUALQUIER cosa falla arriba, deshacemos TODO lo que se hizo en esta sesión.
        self.db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error in transaction: {str(e)}")
        
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
            raise HTTPException(status_code=404, detail="Lote not found")
       
       update_data = updates.model_dump(exclude_unset=True)
       self.repo.update(lote, update_data)
       return lote
    
    def delete_lote(self, lote_id: int):
       lote= self.repo.get_by_id(lote_id)
       if not lote:
          raise HTTPException(status_code=404, detail="Lote not found")
       if lote.estado != "Disponible":
          raise HTTPException(status_code=400, detail="Cannot delete a reserved or sold lote")
       
       # Verificar que no haya detalles_compra asociados
       detalles = self.detalle_repo.get_by_lote_id(lote_id)
       if detalles:
          raise HTTPException(status_code=400, detail="Cannot delete lote with associated sales")
       
       self.repo.delete(lote)
       return {"message": "Lote deleted successfully"}
       
     

    def list_lotes(self, estado: str = None, etapa_id: int = None):
     """
    Lista los lotes con filtros opcionales por estado y etapa. 🔍
     """
     self._clean_expired_purchases()
    # verificamos que exista la etapa
     if etapa_id:
        etapa = self.etapa_repo.get_by_id(etapa_id)
        if not etapa:
            raise HTTPException(status_code=404, detail="Etapa not found")
     
     return self.repo.list_filtered(estado, etapa_id)
    
   
    def _clean_expired_purchases(self):
     """
    Busca todas las compras expiradas usando el repo y las cancela.
     """
     ahora = datetime.now(timezone.utc)
    
    # 1. Usamos el repo para traer solo las que debemos limpiar
     expired_purchases = self.compra_repo.get_expired_active(ahora)

     if not expired_purchases:
        return 


     try:
        for compra in expired_purchases:
            #  Obtenemos detalles mediante el repo de detalles
            detalles = self.detalle_repo.get_by_compra_id(compra.id)
            
            for item in detalles:
                lote = self.repo.get_by_id(item.lote_id)
                if lote and lote.estado == "Reservado":
                
                    self.repo.update_without_commit(lote, {"estado": "Disponible"})
            
            # 4. Cancelamos la compra
            self.compra_repo.update_without_commit(compra, {"estado": "Cancelada"})
        
        self.db.commit()
     except Exception as e:
        # Aquí puedes loguear el error, pero no bloqueamos al usuario
        self.db.rollback()
        print(f"Error en auto-limpieza: {e}")
