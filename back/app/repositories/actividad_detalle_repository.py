from sqlalchemy import select

from app.models.actividad_detalle import ActividadDetalle
from app.repositories.base import BaseRepository


class ActividadDetalleRepository(BaseRepository[ActividadDetalle]):
    def __init__(self, db):
        super().__init__(ActividadDetalle, db)

    def get_by_actividad(self, actividad_id: int, active_only: bool = True) -> list[ActividadDetalle]:
        query = select(self.model).where(self.model.actividad_id == actividad_id)
        if active_only:
            query = query.where(self.model.estado == "activo")
        result = self.db.execute(query)
        return list(result.scalars().all())
