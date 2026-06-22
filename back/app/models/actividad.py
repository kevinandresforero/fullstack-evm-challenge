from sqlalchemy import Column, Integer, String, Text, Numeric, Date, DateTime, ForeignKey, func
from app.database import Base


class Actividad(Base):
    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proyecto_id = Column(Integer, ForeignKey("proyecto.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    presupuesto = Column(Numeric(12, 2), nullable=False)
    porcentaje_avance_planificado = Column(Numeric(5, 2), nullable=False, default=0)
    porcentaje_avance_real = Column(Numeric(5, 2), nullable=False, default=0)
    costo_real = Column(Numeric(12, 2), nullable=False, default=0)
    recursos = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    fecha_modificacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(String(20), default="activo")
