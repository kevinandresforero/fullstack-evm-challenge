"""Pruebas de integración para endpoints EVM."""

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app


class TestEvmAPI:
    async def test_evm_proyecto_sin_actividades_retorna_404(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/api/proyectos",
                json={
                    "nombre": "Proyecto sin actividades",
                    "fecha_inicio": "2026-01-01",
                    "fecha_fin": "2026-12-31",
                },
            )
            proyecto_id = resp.json()["id"]
            response = await client.get(f"/api/proyectos/{proyecto_id}/evm")
            assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_evm_proyecto_con_actividades_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/api/proyectos",
                json={
                    "nombre": "Proyecto con actividades",
                    "fecha_inicio": "2026-01-01",
                    "fecha_fin": "2026-12-31",
                },
            )
            proyecto_id = resp.json()["id"]
            await client.post(
                f"/api/proyectos/{proyecto_id}/actividades",
                json={
                    "nombre": "Actividad 1",
                    "presupuesto": 10000,
                    "porcentaje_avance_planificado": 100,
                    "porcentaje_avance_real": 100,
                    "costo_real": 9000,
                },
            )
            response = await client.get(f"/api/proyectos/{proyecto_id}/evm")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "indicadores" in data
            assert data["total_actividades"] == 1
            assert data["presupuesto_total"] == 10000.0
            assert data["indicadores"]["cpi"] == 10000.0 / 9000.0

    async def test_evm_actividad_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/api/proyectos",
                json={
                    "nombre": "Proyecto EVM",
                    "fecha_inicio": "2026-01-01",
                    "fecha_fin": "2026-12-31",
                },
            )
            proyecto_id = resp.json()["id"]
            act_resp = await client.post(
                f"/api/proyectos/{proyecto_id}/actividades",
                json={
                    "nombre": "Actividad EVM",
                    "presupuesto": 5000,
                    "porcentaje_avance_planificado": 60,
                    "porcentaje_avance_real": 40,
                    "costo_real": 3000,
                },
            )
            actividad_id = act_resp.json()["id"]
            response = await client.get(
                f"/api/proyectos/{proyecto_id}/actividades/{actividad_id}/evm",
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["bac"] == 5000.0
            assert data["cpi_interpretacion"] is not None
            assert data["spi_interpretacion"] is not None

    async def test_health_check_retorna_200(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/health")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "ok"
