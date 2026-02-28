from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Definimos tipos genéricos
ModelType = TypeVar("ModelType") # Para el modelo de SQLAlchemy (Usuario, Pago, etc.)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: Any) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: ModelType) -> ModelType:
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in
    
    def create_without_commit(self, obj_in: ModelType) -> ModelType:
        self.db.add(obj_in)
        return obj_in


    def update(self, db_obj: ModelType, updates: dict) -> ModelType:
        for field in updates:
            setattr(db_obj, field, updates[field])
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update_without_commit(self, db_obj: ModelType, updates: dict) -> ModelType:
        for field in updates:
            setattr(db_obj, field, updates[field])
        return db_obj


    def delete(self, db_obj: ModelType) -> None:
        self.db.delete(db_obj)
        self.db.commit()
    
    def delete_without_commit(self, db_obj: ModelType) -> None:
        self.db.delete(db_obj)
        return db_obj