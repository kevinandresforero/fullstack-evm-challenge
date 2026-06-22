from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ActividadDetalleBase(BaseModel):
    concepto: str = Field(..., min_length=1, max_length=255)
    cantidad: Decimal = Field(default=1, ge=0, max_digits=12, decimal_places=2)
    costo_unitario: Decimal = Field(default=0, ge=0, max_digits=12, decimal_places=2)


class ActividadDetalleCreate(ActividadDetalleBase):
    pass


class ActividadDetalleUpdate(BaseModel):
    concepto: Optional[str] = Field(None, min_length=1, max_length=255)
    cantidad: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)
    costo_unitario: Optional[Decimal] = Field(None, ge=0, max_digits=12, decimal_places=2)


class ActividadDetalleResponse(ActividadDetalleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actividad_id: int
    fecha_modificacion: datetime
    estado: str
