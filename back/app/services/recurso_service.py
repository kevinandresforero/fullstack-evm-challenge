from typing import Any

from app.constants import ERROR_RECURSO_NO_ENCONTRADO
from app.models.recurso import Recurso
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.tipo_recurso_repository import TipoRecursoRepository
from app.schemas.recurso import RecursoCreate, RecursoUpdate


class RecursoService:
    def __init__(self, repo: RecursoRepository, tipo_recurso_repo: TipoRecursoRepository):
        self.repo = repo
        self.tipo_recurso_repo = tipo_recurso_repo

    def listar(self) -> list[Recurso]:
        return self.repo.get_all()

    def obtener(self, recurso_id: int) -> Recurso:
        recurso = self.repo.get_by_id(recurso_id)
        if not recurso:
            raise ValueError(ERROR_RECURSO_NO_ENCONTRADO)
        return recurso

    def crear(self, data: RecursoCreate) -> Recurso:
        tipo = self.tipo_recurso_repo.get_by_id(data.tipo_recurso_id)
        if not tipo:
            raise ValueError("Tipo de recurso no encontrado")
        entity = Recurso(
            nombre=data.nombre,
            tipo_recurso_id=data.tipo_recurso_id,
            descripcion=data.descripcion,
        )
        return self.repo.create(entity)

    def actualizar(self, recurso_id: int, data: RecursoUpdate) -> Recurso:
        recurso = self.repo.get_by_id(recurso_id)
        if not recurso:
            raise ValueError(ERROR_RECURSO_NO_ENCONTRADO)
        update_data: dict[str, Any] = data.model_dump(exclude_unset=True)
        return self.repo.update(recurso, update_data)

    def eliminar(self, recurso_id: int) -> Recurso:
        recurso = self.repo.get_by_id(recurso_id)
        if not recurso:
            raise ValueError(ERROR_RECURSO_NO_ENCONTRADO)
        return self.repo.soft_delete(recurso)
