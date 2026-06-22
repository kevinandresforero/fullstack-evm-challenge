from typing import Any

from app.constants import ERROR_TIPO_RECURSO_NO_ENCONTRADO
from app.models.tipo_recurso import TipoRecurso
from app.repositories.tipo_recurso_repository import TipoRecursoRepository
from app.schemas.tipo_recurso import TipoRecursoCreate, TipoRecursoUpdate


class TipoRecursoService:
    def __init__(self, repo: TipoRecursoRepository):
        self.repo = repo

    def listar(self) -> list[TipoRecurso]:
        return self.repo.get_all()

    def obtener(self, tipo_recurso_id: int) -> TipoRecurso:
        tipo = self.repo.get_by_id(tipo_recurso_id)
        if not tipo:
            raise ValueError(ERROR_TIPO_RECURSO_NO_ENCONTRADO)
        return tipo

    def crear(self, data: TipoRecursoCreate) -> TipoRecurso:
        entity = TipoRecurso(
            nombre=data.nombre,
            descripcion=data.descripcion,
        )
        return self.repo.create(entity)

    def actualizar(self, tipo_recurso_id: int, data: TipoRecursoUpdate) -> TipoRecurso:
        tipo = self.repo.get_by_id(tipo_recurso_id)
        if not tipo:
            raise ValueError(ERROR_TIPO_RECURSO_NO_ENCONTRADO)
        update_data: dict[str, Any] = data.model_dump(exclude_unset=True)
        return self.repo.update(tipo, update_data)

    def eliminar(self, tipo_recurso_id: int) -> TipoRecurso:
        tipo = self.repo.get_by_id(tipo_recurso_id)
        if not tipo:
            raise ValueError(ERROR_TIPO_RECURSO_NO_ENCONTRADO)
        return self.repo.soft_delete(tipo)
