from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, func
from app.database import Base


class ActividadDetalle(Base):
    __tablename__ = "actividad_detalle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)
    concepto = Column(String(255), nullable=False)
    cantidad = Column(Numeric(12, 2), default=1)
    costo_unitario = Column(Numeric(12, 2), default=0)
    fecha_modificacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estado = Column(String(20), default="activo")
