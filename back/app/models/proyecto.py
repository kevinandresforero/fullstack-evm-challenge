from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from app.database import Base


class Proyecto(Base):
    __tablename__ = "proyecto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_modificacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(String(20), default="activo")
