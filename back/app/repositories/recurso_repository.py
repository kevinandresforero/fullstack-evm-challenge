from app.models.recurso import Recurso
from app.repositories.base import BaseRepository


class RecursoRepository(BaseRepository[Recurso]):
    def __init__(self, db):
        super().__init__(Recurso, db)
