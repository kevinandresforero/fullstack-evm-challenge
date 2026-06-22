from typing import Optional

from app.constants import (
    CPI_BAJO_PRESUPUESTO,
    CPI_EN_PRESUPUESTO,
    CPI_SOBRE_PRESUPUESTO,
    ERROR_CPI_INDEFINIDO,
    ERROR_PRESUPUESTO_INVALIDO,
    ERROR_PROYECTO_SIN_ACTIVIDADES,
    ERROR_SPI_INDEFINIDO,
    SPI_ADELANTADO,
    SPI_ATRASADO,
    SPI_EN_CRONOGRAMA,
)
from app.models.actividad import Actividad
from app.schemas.evm import ActividadEvmResponse, EvmIndicators, ProyectoEvmResponse


class EvmService:
    def _calcular_pv(self, bac: float, porcentaje_planificado: float) -> float:
        return (porcentaje_planificado / 100.0) * bac

    def _calcular_ev(self, bac: float, porcentaje_real: float) -> float:
        return (porcentaje_real / 100.0) * bac

    def _calcular_cv(self, ev: float, ac: float) -> float:
        return ev - ac

    def _calcular_sv(self, ev: float, pv: float) -> float:
        return ev - pv

    def _calcular_cpi(self, ev: float, ac: float) -> Optional[float]:
        if ac == 0.0:
            return None
        return ev / ac

    def _calcular_spi(self, ev: float, pv: float) -> Optional[float]:
        if pv == 0.0:
            return None
        return ev / pv

    def _calcular_eac(self, bac: float, cpi: Optional[float]) -> Optional[float]:
        if cpi is None or cpi == 0.0:
            return None
        return bac / cpi

    def _calcular_vac(self, bac: float, eac: Optional[float]) -> Optional[float]:
        if eac is None:
            return None
        return bac - eac

    def _interpretar_cpi(self, cpi: Optional[float]) -> str:
        if cpi is None:
            return ERROR_CPI_INDEFINIDO
        if cpi > 1.0:
            return CPI_BAJO_PRESUPUESTO
        if cpi < 1.0:
            return CPI_SOBRE_PRESUPUESTO
        return CPI_EN_PRESUPUESTO

    def _interpretar_spi(self, spi: Optional[float]) -> str:
        if spi is None:
            return ERROR_SPI_INDEFINIDO
        if spi > 1.0:
            return SPI_ADELANTADO
        if spi < 1.0:
            return SPI_ATRASADO
        return SPI_EN_CRONOGRAMA

    def calcular_indicadores_actividad(self, actividad: Actividad) -> EvmIndicators:
        bac = float(actividad.presupuesto)
        pv = self._calcular_pv(bac, float(actividad.porcentaje_avance_planificado))
        ev = self._calcular_ev(bac, float(actividad.porcentaje_avance_real))
        ac = float(actividad.costo_real)
        cv = self._calcular_cv(ev, ac)
        sv = self._calcular_sv(ev, pv)
        cpi = self._calcular_cpi(ev, ac)
        spi = self._calcular_spi(ev, pv)
        eac = self._calcular_eac(bac, cpi)
        vac = self._calcular_vac(bac, eac)

        return EvmIndicators(
            bac=bac,
            pv=pv,
            ev=ev,
            ac=ac,
            cv=cv,
            sv=sv,
            cpi=cpi,
            spi=spi,
            eac=eac,
            vac=vac,
            cpi_interpretacion=self._interpretar_cpi(cpi),
            spi_interpretacion=self._interpretar_spi(spi),
        )

    def calcular_indicadores_proyecto(self, proyecto_id: int, proyecto_nombre: str, actividades: list[Actividad]) -> ProyectoEvmResponse:
        if not actividades:
            raise ValueError(ERROR_PROYECTO_SIN_ACTIVIDADES)

        total_bac = sum(float(a.presupuesto) for a in actividades)
        if total_bac <= 0:
            raise ValueError(ERROR_PRESUPUESTO_INVALIDO)

        indicadores_actividades: list[ActividadEvmResponse] = []
        suma_pv = 0.0
        suma_ev = 0.0
        suma_ac = 0.0

        for actividad in actividades:
            ind_act = self.calcular_indicadores_actividad(actividad)
            suma_pv += ind_act.pv
            suma_ev += ind_act.ev
            suma_ac += ind_act.ac
            indicadores_actividades.append(
                ActividadEvmResponse(
                    actividad_id=actividad.id,
                    actividad_nombre=actividad.nombre,
                    indicadores=ind_act,
                )
            )

        cv_total = self._calcular_cv(suma_ev, suma_ac)
        sv_total = self._calcular_sv(suma_ev, suma_pv)
        cpi_total = self._calcular_cpi(suma_ev, suma_ac)
        spi_total = self._calcular_spi(suma_ev, suma_pv)
        eac_total = self._calcular_eac(total_bac, cpi_total)
        vac_total = self._calcular_vac(total_bac, eac_total)

        return ProyectoEvmResponse(
            proyecto_id=proyecto_id,
            proyecto_nombre=proyecto_nombre,
            total_actividades=len(actividades),
            presupuesto_total=total_bac,
            indicadores=EvmIndicators(
                bac=total_bac,
                pv=suma_pv,
                ev=suma_ev,
                ac=suma_ac,
                cv=cv_total,
                sv=sv_total,
                cpi=cpi_total,
                spi=spi_total,
                eac=eac_total,
                vac=vac_total,
                cpi_interpretacion=self._interpretar_cpi(cpi_total),
                spi_interpretacion=self._interpretar_spi(spi_total),
            ),
            actividades=indicadores_actividades,
        )
