from sqlalchemy import select

from app.models.actividad import Actividad
from app.repositories.base import BaseRepository


class ActividadRepository(BaseRepository[Actividad]):
    def __init__(self, db):
        super().__init__(Actividad, db)

    def get_by_proyecto(self, proyecto_id: int, active_only: bool = True) -> list[Actividad]:
        query = select(self.model).where(self.model.proyecto_id == proyecto_id)
        if active_only:
            query = query.where(self.model.estado == "activo")
        result = self.db.execute(query)
        return list(result.scalars().all())
