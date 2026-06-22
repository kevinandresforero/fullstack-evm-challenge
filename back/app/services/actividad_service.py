from typing import Any

from app.constants import ERROR_PROYECTO_NO_ENCONTRADO
from app.models.actividad import Actividad
from app.repositories.actividad_repository import ActividadRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.actividad import ActividadCreate, ActividadUpdate
from app.services.evm_service import EvmService


class ActividadService:
    def __init__(self, repo: ActividadRepository, proyecto_repo: ProyectoRepository):
        self.repo = repo
        self.proyecto_repo = proyecto_repo

    def listar_por_proyecto(self, proyecto_id: int) -> list[Actividad]:
        return self.repo.get_by_proyecto(proyecto_id)

    def obtener(self, actividad_id: int) -> Actividad:
        actividad = self.repo.get_by_id(actividad_id)
        if not actividad:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        return actividad

    def crear(self, proyecto_id: int, data: ActividadCreate) -> Actividad:
        proyecto = self.proyecto_repo.get_by_id(proyecto_id)
        if not proyecto:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        entity = Actividad(
            proyecto_id=proyecto_id,
            nombre=data.nombre,
            descripcion=data.descripcion,
            presupuesto=data.presupuesto,
            porcentaje_avance_planificado=data.porcentaje_avance_planificado,
            porcentaje_avance_real=data.porcentaje_avance_real,
            costo_real=data.costo_real,
            recursos=data.recursos,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
        )
        return self.repo.create(entity)

    def actualizar(self, actividad_id: int, data: ActividadUpdate) -> Actividad:
        actividad = self.repo.get_by_id(actividad_id)
        if not actividad:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        update_data: dict[str, Any] = data.model_dump(exclude_unset=True)
        return self.repo.update(actividad, update_data)

    def eliminar(self, actividad_id: int) -> Actividad:
        actividad = self.repo.get_by_id(actividad_id)
        if not actividad:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        return self.repo.soft_delete(actividad)

    def obtener_con_evm(self, actividad_id: int, evm_service: EvmService) -> tuple[Actividad, Any]:
        actividad = self.obtener(actividad_id)
        indicadores = evm_service.calcular_indicadores_actividad(actividad)
        return actividad, indicadores
