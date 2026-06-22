from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.database import Base


class Recurso(Base):
    __tablename__ = "recurso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    tipo_recurso_id = Column(Integer, ForeignKey("tipo_recurso.id"), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_modificacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(String(20), default="activo")
