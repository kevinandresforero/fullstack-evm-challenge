from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ActividadBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    presupuesto: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    porcentaje_avance_planificado: Decimal = Field(..., ge=0, le=100, max_digits=5, decimal_places=2)
    porcentaje_avance_real: Decimal = Field(..., ge=0, le=100, max_digits=5, decimal_places=2)
    costo_real: Decimal = Field(..., ge=0, max_digits=12, decimal_places=2)
    recursos: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    presupuesto: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=2)
    porcentaje_avance_planificado: Optional[Decimal] = Field(None, ge=0, le=100, max_digits=5, decimal_places=2)
    porcentaje_avance_real: Optional[Decimal] = Field(None, ge=0, le=100, max_digits=5, decimal_places=2)
    costo_real: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    recursos: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ActividadResponse(ActividadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    proyecto_id: int
    fecha_modificacion: datetime
    estado: str
