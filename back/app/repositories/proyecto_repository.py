from app.models.proyecto import Proyecto
from app.repositories.base import BaseRepository


class ProyectoRepository(BaseRepository[Proyecto]):
    def __init__(self, db):
        super().__init__(Proyecto, db)
