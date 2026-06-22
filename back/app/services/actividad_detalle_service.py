from typing import Any

from app.constants import ERROR_ACTIVIDAD_DETALLE_NO_ENCONTRADO, ERROR_ACTIVIDAD_NO_ENCONTRADA
from app.models.actividad_detalle import ActividadDetalle
from app.repositories.actividad_detalle_repository import ActividadDetalleRepository
from app.repositories.actividad_repository import ActividadRepository
from app.schemas.actividad_detalle import ActividadDetalleCreate, ActividadDetalleUpdate


class ActividadDetalleService:
    def __init__(self, repo: ActividadDetalleRepository, actividad_repo: ActividadRepository):
        self.repo = repo
        self.actividad_repo = actividad_repo

    def listar_por_actividad(self, actividad_id: int) -> list[ActividadDetalle]:
        return self.repo.get_by_actividad(actividad_id)

    def obtener(self, detalle_id: int) -> ActividadDetalle:
        detalle = self.repo.get_by_id(detalle_id)
        if not detalle:
            raise ValueError(ERROR_ACTIVIDAD_DETALLE_NO_ENCONTRADO)
        return detalle

    def crear(self, actividad_id: int, data: ActividadDetalleCreate) -> ActividadDetalle:
        actividad = self.actividad_repo.get_by_id(actividad_id)
        if not actividad:
            raise ValueError(ERROR_ACTIVIDAD_NO_ENCONTRADA)
        entity = ActividadDetalle(
            actividad_id=actividad_id,
            concepto=data.concepto,
            cantidad=data.cantidad,
            costo_unitario=data.costo_unitario,
        )
        return self.repo.create(entity)

    def actualizar(self, detalle_id: int, data: ActividadDetalleUpdate) -> ActividadDetalle:
        detalle = self.repo.get_by_id(detalle_id)
        if not detalle:
            raise ValueError(ERROR_ACTIVIDAD_DETALLE_NO_ENCONTRADO)
        update_data: dict[str, Any] = data.model_dump(exclude_unset=True)
        return self.repo.update(detalle, update_data)

    def eliminar(self, detalle_id: int) -> ActividadDetalle:
        detalle = self.repo.get_by_id(detalle_id)
        if not detalle:
            raise ValueError(ERROR_ACTIVIDAD_DETALLE_NO_ENCONTRADO)
        return self.repo.soft_delete(detalle)
