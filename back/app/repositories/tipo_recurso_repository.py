from app.models.tipo_recurso import TipoRecurso
from app.repositories.base import BaseRepository


class TipoRecursoRepository(BaseRepository[TipoRecurso]):
    def __init__(self, db):
        super().__init__(TipoRecurso, db)
