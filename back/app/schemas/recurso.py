from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RecursoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    tipo_recurso_id: int
    descripcion: Optional[str] = None


class RecursoCreate(RecursoBase):
    pass


class RecursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    tipo_recurso_id: Optional[int] = None
    descripcion: Optional[str] = None


class RecursoResponse(RecursoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_modificacion: datetime
    estado: str
