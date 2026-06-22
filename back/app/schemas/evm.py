from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class EvmIndicators(BaseModel):
    bac: float
    pv: float
    ev: float
    ac: float
    cv: float
    sv: float
    cpi: Optional[float] = None
    spi: Optional[float] = None
    eac: Optional[float] = None
    vac: Optional[float] = None
    cpi_interpretacion: str
    spi_interpretacion: str


class ActividadEvmResponse(BaseModel):
    actividad_id: int
    actividad_nombre: str
    indicadores: EvmIndicators


class ProyectoEvmResponse(BaseModel):
    proyecto_id: int
    proyecto_nombre: str
    total_actividades: int
    presupuesto_total: float
    indicadores: EvmIndicators
    actividades: list[ActividadEvmResponse]
