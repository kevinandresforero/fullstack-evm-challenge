"""Pruebas unitarias para ActividadService.

Se mockean ActividadRepository y ProyectoRepository para aislar la lógica del servicio.
"""

from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from app.constants import ERROR_ACTIVIDAD_NO_ENCONTRADA, ERROR_PROYECTO_NO_ENCONTRADO
from app.schemas.actividad import ActividadCreate, ActividadUpdate
from app.services.actividad_service import ActividadService


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_proyecto_repo():
    return Mock()


@pytest.fixture
def service(mock_repo, mock_proyecto_repo):
    return ActividadService(repo=mock_repo, proyecto_repo=mock_proyecto_repo)


class TestActividadService:
    """1 caso de éxito, 3 casos de fallo."""

    def test_crear_exito(self, service, mock_repo, mock_proyecto_repo):
        """1 caso de éxito: crear actividad cuando proyecto existe."""
        mock_proyecto_repo.get_by_id.return_value = Mock(id=1, nombre="Proyecto")
        data = ActividadCreate(
            nombre="Actividad nueva",
            presupuesto=Decimal("10000"),
            porcentaje_avance_planificado=Decimal("50"),
            porcentaje_avance_real=Decimal("30"),
            costo_real=Decimal("4000"),
        )
        mock_repo.create.return_value = Mock(id=1, nombre="Actividad nueva")
        resultado = service.crear(1, data)
        assert resultado.id == 1
        mock_repo.create.assert_called_once()

    def test_crear_proyecto_no_existe_error(self, service, mock_repo, mock_proyecto_repo):
        """Caso de fallo 1: crear actividad con proyecto inexistente."""
        mock_proyecto_repo.get_by_id.return_value = None
        data = ActividadCreate(
            nombre="Actividad fallida",
            presupuesto=Decimal("5000"),
            porcentaje_avance_planificado=Decimal("50"),
            porcentaje_avance_real=Decimal("30"),
            costo_real=Decimal("2000"),
        )
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.crear(999, data)

    def test_obtener_no_existe_error(self, service, mock_repo):
        """Caso de fallo 2: obtener actividad que no existe."""
        mock_repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.obtener(999)

    def test_actualizar_no_existe_error(self, service, mock_repo):
        """Caso de fallo 3: actualizar actividad que no existe."""
        mock_repo.get_by_id.return_value = None
        data = ActividadUpdate(nombre="Actualizada")
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.actualizar(999, data)

    def test_eliminar_exito(self, service, mock_repo):
        """Eliminar actividad existente."""
        mock_act = Mock(id=1, estado="activo")
        mock_repo.get_by_id.return_value = mock_act
        mock_repo.soft_delete.return_value = Mock(id=1, estado="inactivo")
        resultado = service.eliminar(1)
        assert resultado.estado == "inactivo"
        mock_repo.soft_delete.assert_called_once_with(mock_act)
