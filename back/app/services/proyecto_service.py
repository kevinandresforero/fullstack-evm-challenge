from typing import Any

from app.constants import ERROR_PROYECTO_NO_ENCONTRADO
from app.models.proyecto import Proyecto
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate


class ProyectoService:
    def __init__(self, repo: ProyectoRepository):
        self.repo = repo

    def listar(self) -> list[Proyecto]:
        return self.repo.get_all()

    def obtener(self, proyecto_id: int) -> Proyecto:
        proyecto = self.repo.get_by_id(proyecto_id)
        if not proyecto:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        return proyecto

    def crear(self, data: ProyectoCreate) -> Proyecto:
        entity = Proyecto(
            nombre=data.nombre,
            descripcion=data.descripcion,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
        )
        return self.repo.create(entity)

    def actualizar(self, proyecto_id: int, data: ProyectoUpdate) -> Proyecto:
        proyecto = self.repo.get_by_id(proyecto_id)
        if not proyecto:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        update_data: dict[str, Any] = data.model_dump(exclude_unset=True)
        return self.repo.update(proyecto, update_data)

    def eliminar(self, proyecto_id: int) -> Proyecto:
        proyecto = self.repo.get_by_id(proyecto_id)
        if not proyecto:
            raise ValueError(ERROR_PROYECTO_NO_ENCONTRADO)
        return self.repo.soft_delete(proyecto)
