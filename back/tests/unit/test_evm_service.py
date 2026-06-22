import pytest

from app.constants import (
    CPI_BAJO_PRESUPUESTO,
    CPI_EN_PRESUPUESTO,
    CPI_SOBRE_PRESUPUESTO,
    ERROR_PRESUPUESTO_INVALIDO,
    ERROR_PROYECTO_SIN_ACTIVIDADES,
    SPI_ADELANTADO,
    SPI_ATRASADO,
    SPI_EN_CRONOGRAMA,
)
from app.models.actividad import Actividad
from app.services.evm_service import EvmService


@pytest.fixture
def evm_service():
    return EvmService()


@pytest.fixture
def actividad_base():
    return Actividad(
        id=1,
        proyecto_id=1,
        nombre="Actividad base",
        presupuesto=10000,
        porcentaje_avance_planificado=50,
        porcentaje_avance_real=30,
        costo_real=4000,
    )


class TestCalculosIndividuales:
    def test_calcular_pv(self, evm_service):
        assert evm_service._calcular_pv(10000.0, 50.0) == 5000.0

    def test_calcular_pv_cero_porcentaje(self, evm_service):
        assert evm_service._calcular_pv(10000.0, 0.0) == 0.0

    def test_calcular_pv_cien_porcentaje(self, evm_service):
        assert evm_service._calcular_pv(10000.0, 100.0) == 10000.0

    def test_calcular_ev(self, evm_service):
        assert evm_service._calcular_ev(10000.0, 30.0) == 3000.0

    def test_calcular_cv(self, evm_service):
        assert evm_service._calcular_cv(3000.0, 4000.0) == -1000.0

    def test_calcular_sv(self, evm_service):
        assert evm_service._calcular_sv(3000.0, 5000.0) == -2000.0

    def test_calcular_cpi(self, evm_service):
        assert evm_service._calcular_cpi(3000.0, 4000.0) == 0.75

    def test_calcular_cpi_ac_cero(self, evm_service):
        assert evm_service._calcular_cpi(3000.0, 0.0) is None

    def test_calcular_spi(self, evm_service):
        assert evm_service._calcular_spi(3000.0, 5000.0) == 0.6

    def test_calcular_spi_pv_cero(self, evm_service):
        assert evm_service._calcular_spi(3000.0, 0.0) is None

    def test_calcular_eac(self, evm_service):
        result = evm_service._calcular_eac(10000.0, 0.75)
        assert result == pytest.approx(13333.33, rel=1e-2)

    def test_calcular_eac_cpi_none(self, evm_service):
        assert evm_service._calcular_eac(10000.0, None) is None

    def test_calcular_eac_cpi_cero(self, evm_service):
        assert evm_service._calcular_eac(10000.0, 0.0) is None

    def test_calcular_vac(self, evm_service):
        assert evm_service._calcular_vac(10000.0, 13333.33) == pytest.approx(-3333.33, rel=1e-2)

    def test_calcular_vac_eac_none(self, evm_service):
        assert evm_service._calcular_vac(10000.0, None) is None


class TestInterpretacion:
    def test_cpi_mayor_1_bajo_presupuesto(self, evm_service):
        assert evm_service._interpretar_cpi(1.2) == CPI_BAJO_PRESUPUESTO

    def test_cpi_menor_1_sobre_presupuesto(self, evm_service):
        assert evm_service._interpretar_cpi(0.8) == CPI_SOBRE_PRESUPUESTO

    def test_cpi_igual_1_en_presupuesto(self, evm_service):
        assert evm_service._interpretar_cpi(1.0) == CPI_EN_PRESUPUESTO

    def test_cpi_none(self, evm_service):
        assert evm_service._interpretar_cpi(None) == "CPI indefinido (AC es cero en todas las actividades)"

    def test_spi_mayor_1_adelantado(self, evm_service):
        assert evm_service._interpretar_spi(1.2) == SPI_ADELANTADO

    def test_spi_menor_1_atrasado(self, evm_service):
        assert evm_service._interpretar_spi(0.8) == SPI_ATRASADO

    def test_spi_igual_1_en_cronograma(self, evm_service):
        assert evm_service._interpretar_spi(1.0) == SPI_EN_CRONOGRAMA

    def test_spi_none(self, evm_service):
        assert evm_service._interpretar_spi(None) == "SPI indefinido (PV es cero en todas las actividades)"


class TestCalculoActividad:
    def test_caso_exito(self, evm_service, actividad_base):
        indicadores = evm_service.calcular_indicadores_actividad(actividad_base)

        assert indicadores.bac == 10000.0
        assert indicadores.pv == 5000.0
        assert indicadores.ev == 3000.0
        assert indicadores.ac == 4000.0
        assert indicadores.cv == -1000.0
        assert indicadores.sv == -2000.0
        assert indicadores.cpi == 0.75
        assert indicadores.spi == 0.6
        assert indicadores.eac == pytest.approx(13333.33, rel=1e-2)
        assert indicadores.vac == pytest.approx(-3333.33, rel=1e-2)
        assert indicadores.cpi_interpretacion == CPI_SOBRE_PRESUPUESTO
        assert indicadores.spi_interpretacion == SPI_ATRASADO

    def test_ac_cero(self, evm_service):
        actividad = Actividad(
            id=2, proyecto_id=1, nombre="Sin costo",
            presupuesto=5000,
            porcentaje_avance_planificado=100,
            porcentaje_avance_real=100,
            costo_real=0,
        )
        indicadores = evm_service.calcular_indicadores_actividad(actividad)

        assert indicadores.ac == 0.0
        assert indicadores.ev == 5000.0
        assert indicadores.cpi is None
        assert indicadores.eac is None
        assert indicadores.vac is None
        assert "CPI indefinido" in indicadores.cpi_interpretacion

    def test_avance_real_cero(self, evm_service):
        actividad = Actividad(
            id=3, proyecto_id=1, nombre="Sin avance",
            presupuesto=10000,
            porcentaje_avance_planificado=50,
            porcentaje_avance_real=0,
            costo_real=2000,
        )
        indicadores = evm_service.calcular_indicadores_actividad(actividad)

        assert indicadores.ev == 0.0
        assert indicadores.cv == -2000.0
        assert indicadores.sv == -5000.0
        assert indicadores.cpi == 0.0
        assert indicadores.spi == 0.0
        assert indicadores.eac is None
        assert indicadores.vac is None

    def test_pv_cero(self, evm_service):
        actividad = Actividad(
            id=4, proyecto_id=1, nombre="Sin planificar",
            presupuesto=10000,
            porcentaje_avance_planificado=0,
            porcentaje_avance_real=10,
            costo_real=1000,
        )
        indicadores = evm_service.calcular_indicadores_actividad(actividad)

        assert indicadores.pv == 0.0
        assert indicadores.spi is None
        assert "SPI indefinido" in indicadores.spi_interpretacion

    def test_presupuesto_minimo(self, evm_service):
        actividad = Actividad(
            id=5, proyecto_id=1, nombre="Actividad pequeña",
            presupuesto=1,
            porcentaje_avance_planificado=100,
            porcentaje_avance_real=100,
            costo_real=1,
        )
        indicadores = evm_service.calcular_indicadores_actividad(actividad)

        assert indicadores.bac == 1.0
        assert indicadores.pv == 1.0
        assert indicadores.ev == 1.0
        assert indicadores.cpi == 1.0
        assert indicadores.spi == 1.0
        assert indicadores.cpi_interpretacion == CPI_EN_PRESUPUESTO
        assert indicadores.spi_interpretacion == SPI_EN_CRONOGRAMA


class TestCalculoProyecto:
    def test_caso_exito(self, evm_service, actividad_base):
        resultado = evm_service.calcular_indicadores_proyecto(
            proyecto_id=1,
            proyecto_nombre="Proyecto de prueba",
            actividades=[actividad_base],
        )

        assert resultado.proyecto_id == 1
        assert resultado.total_actividades == 1
        assert resultado.presupuesto_total == 10000.0
        assert resultado.indicadores.bac == 10000.0
        assert len(resultado.actividades) == 1
        assert resultado.actividades[0].actividad_nombre == "Actividad base"

    def test_multiples_actividades(self, evm_service):
        act1 = Actividad(
            id=1, proyecto_id=1, nombre="Act 1",
            presupuesto=10000,
            porcentaje_avance_planificado=100,
            porcentaje_avance_real=100,
            costo_real=8000,
        )
        act2 = Actividad(
            id=2, proyecto_id=1, nombre="Act 2",
            presupuesto=20000,
            porcentaje_avance_planificado=50,
            porcentaje_avance_real=25,
            costo_real=6000,
        )
        resultado = evm_service.calcular_indicadores_proyecto(
            proyecto_id=1, proyecto_nombre="Proyecto", actividades=[act1, act2],
        )

        assert resultado.total_actividades == 2
        assert resultado.presupuesto_total == 30000.0
        assert resultado.indicadores.pv == 20000.0
        assert resultado.indicadores.ev == 15000.0
        assert resultado.indicadores.ac == 14000.0
        assert resultado.indicadores.cpi == 15000.0 / 14000.0

    def test_sin_actividades_error(self, evm_service):
        with pytest.raises(ValueError, match=ERROR_PROYECTO_SIN_ACTIVIDADES):
            evm_service.calcular_indicadores_proyecto(
                proyecto_id=1, proyecto_nombre="Vacio", actividades=[],
            )

    def test_presupuesto_total_cero_error(self, evm_service):
        act = Actividad(
            id=1, proyecto_id=1, nombre="Act cero",
            presupuesto=0,
            porcentaje_avance_planificado=0,
            porcentaje_avance_real=0,
            costo_real=0,
        )
        with pytest.raises(ValueError, match=ERROR_PRESUPUESTO_INVALIDO):
            evm_service.calcular_indicadores_proyecto(
                proyecto_id=1, proyecto_nombre="Sin presupuesto", actividades=[act],
            )
