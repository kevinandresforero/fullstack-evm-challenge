"""Pruebas de integración para endpoints de proyectos.

Valida el contrato de respuesta (códigos HTTP, estructura JSON, tipos).
"""

from datetime import date

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


class TestProyectosAPI:
    async def _crear_proyecto(self, client):
        response = await client.post(
            "/api/proyectos",
            json={
                "nombre": "Proyecto integración",
                "descripcion": "Test de integración",
                "fecha_inicio": "2026-01-01",
                "fecha_fin": "2026-12-31",
            },
        )
        return response

    async def test_crear_proyecto_retorna_201(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await self._crear_proyecto(client)
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["nombre"] == "Proyecto integración"
            assert "id" in data
            assert "estado" in data

    async def test_listar_proyectos_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await self._crear_proyecto(client)
            response = await client.get("/api/proyectos")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    async def test_obtener_proyecto_por_id_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await self._crear_proyecto(client)
            proyecto_id = created.json()["id"]
            response = await client.get(f"/api/proyectos/{proyecto_id}")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["id"] == proyecto_id

    async def test_obtener_proyecto_inexistente_retorna_404(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/proyectos/99999")
            assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_actualizar_proyecto_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await self._crear_proyecto(client)
            proyecto_id = created.json()["id"]
            response = await client.put(
                f"/api/proyectos/{proyecto_id}",
                json={"nombre": "Proyecto actualizado"},
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["nombre"] == "Proyecto actualizado"

    async def test_eliminar_proyecto_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await self._crear_proyecto(client)
            proyecto_id = created.json()["id"]
            response = await client.delete(f"/api/proyectos/{proyecto_id}")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["estado"] == "inactivo"
