from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_fin: date


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ProyectoResponse(ProyectoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_modificacion: datetime
    estado: str


class ProyectoListResponse(BaseModel):
    id: int
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    estado: str
    presupuesto_total: float
    actividad_count: int
