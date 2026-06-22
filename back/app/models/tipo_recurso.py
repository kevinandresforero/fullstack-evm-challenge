from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class TipoRecurso(Base):
    __tablename__ = "tipo_recurso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_modificacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(String(20), default="activo")
