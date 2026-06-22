"""Pruebas de integración para endpoints de actividades."""

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


class TestActividadesAPI:
    async def _crear_proyecto(self, client):
        resp = await client.post(
            "/api/proyectos",
            json={
                "nombre": "Proyecto test actividades",
                "fecha_inicio": "2026-01-01",
                "fecha_fin": "2026-12-31",
            },
        )
        return resp.json()["id"]

    async def _crear_actividad(self, client, proyecto_id):
        resp = await client.post(
            f"/api/proyectos/{proyecto_id}/actividades",
            json={
                "nombre": "Actividad integración",
                "presupuesto": 10000,
                "porcentaje_avance_planificado": 50,
                "porcentaje_avance_real": 30,
                "costo_real": 4000,
            },
        )
        return resp

    async def test_crear_actividad_retorna_201(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            response = await self._crear_actividad(client, proyecto_id)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["nombre"] == "Actividad integración"
            assert data["proyecto_id"] == proyecto_id

    async def test_listar_actividades_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            await self._crear_actividad(client, proyecto_id)
            response = await client.get(f"/api/proyectos/{proyecto_id}/actividades")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    async def test_obtener_actividad_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            created = await self._crear_actividad(client, proyecto_id)
            actividad_id = created.json()["id"]
            response = await client.get(f"/api/proyectos/{proyecto_id}/actividades/{actividad_id}")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["id"] == actividad_id

    async def test_actualizar_actividad_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            created = await self._crear_actividad(client, proyecto_id)
            actividad_id = created.json()["id"]
            response = await client.put(
                f"/api/proyectos/{proyecto_id}/actividades/{actividad_id}",
                json={"nombre": "Actividad actualizada"},
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["nombre"] == "Actividad actualizada"

    async def test_eliminar_actividad_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            created = await self._crear_actividad(client, proyecto_id)
            actividad_id = created.json()["id"]
            response = await client.delete(
                f"/api/proyectos/{proyecto_id}/actividades/{actividad_id}",
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["estado"] == "inactivo"

    async def test_actividad_inexistente_retorna_404(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            proyecto_id = await self._crear_proyecto(client)
            response = await client.get(f"/api/proyectos/{proyecto_id}/actividades/99999")
            assert response.status_code == status.HTTP_404_NOT_FOUND
