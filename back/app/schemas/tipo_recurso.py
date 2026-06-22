from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TipoRecursoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class TipoRecursoCreate(TipoRecursoBase):
    pass


class TipoRecursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None


class TipoRecursoResponse(TipoRecursoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_modificacion: datetime
    estado: str
