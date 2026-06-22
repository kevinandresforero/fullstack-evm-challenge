"""Pruebas unitarias para ProyectoService.

Se mockea ProyectoRepository para aislar la lógica del servicio.
"""

from datetime import date
from unittest.mock import Mock, patch

import pytest

from app.constants import ERROR_PROYECTO_NO_ENCONTRADO
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from app.services.proyecto_service import ProyectoService


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def service(mock_repo):
    return ProyectoService(repo=mock_repo)


class TestProyectoService:
    """Caso de éxito (1) y casos de fallo (3)."""

    def test_crear_exito(self, service, mock_repo):
        """1 caso de éxito: crear proyecto retorna entidad."""
        data = ProyectoCreate(
            nombre="Nuevo proyecto",
            fecha_inicio=date(2026, 1, 1),
            fecha_fin=date(2026, 12, 31),
        )
        mock_repo.create.return_value = Mock(id=1, nombre="Nuevo proyecto")
        resultado = service.crear(data)
        assert resultado.id == 1
        mock_repo.create.assert_called_once()

    def test_obtener_no_existe_error(self, service, mock_repo):
        """Caso de fallo 1: obtener proyecto que no existe."""
        mock_repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.obtener(999)

    def test_actualizar_no_existe_error(self, service, mock_repo):
        """Caso de fallo 2: actualizar proyecto que no existe."""
        mock_repo.get_by_id.return_value = None
        data = ProyectoUpdate(nombre="Actualizado")
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.actualizar(999, data)

    def test_eliminar_no_existe_error(self, service, mock_repo):
        """Caso de fallo 3: eliminar proyecto que no existe."""
        mock_repo.get_by_id.return_value = None
        with pytest.raises(ValueError, match=ERROR_PROYECTO_NO_ENCONTRADO):
            service.eliminar(999)

    def test_listar_delega_al_repo(self, service, mock_repo):
        """Verifica que listar delegue al repositorio."""
        mock_repo.get_all.return_value = [Mock(id=1), Mock(id=2)]
        resultado = service.listar()
        assert len(resultado) == 2
        mock_repo.get_all.assert_called_once()
