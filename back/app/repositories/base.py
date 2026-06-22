from typing import Any, Generic, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_all(self, active_only: bool = True) -> list[ModelType]:
        query = select(self.model)
        if active_only and hasattr(self.model, "estado"):
            query = query.where(self.model.estado == "activo")
        result = self.db.execute(query)
        return list(result.scalars().all())

    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == entity_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def create(self, entity: ModelType) -> ModelType:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: ModelType, data: dict[str, Any]) -> ModelType:
        for key, value in data.items():
            if value is not None:
                setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def soft_delete(self, entity: ModelType) -> ModelType:
        entity.estado = "inactivo"
        self.db.commit()
        self.db.refresh(entity)
        return entity
