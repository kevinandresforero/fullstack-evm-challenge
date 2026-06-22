# EVM Project Manager — Backend

Sistema de gestión de proyectos con cálculo automático de indicadores de Valor Ganado (Earned Value Management / EVM) basado en el estándar PMI.

## Stack

- **Framework:** FastAPI (Python 3.14)
- **Base de datos:** PostgreSQL 18
- **ORM:** SQLAlchemy 2.0
- **Migraciones:** Alembic
- **Pruebas:** pytest + httpx
- **Linter:** Ruff

## Requisitos previos

- Python 3.12+
- PostgreSQL 16+
- pip / venv

## Configuración

1. Clonar el repositorio:

```bash
git clone <repo-url>
cd back
```

2. Crear entorno virtual e instalar dependencias:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # si existe
```

3. Configurar variables de entorno:

```bash
cp .env.example .env
# Editar .env con las credenciales de PostgreSQL
```

4. Crear la base de datos:

```bash
psql -U postgres -c "CREATE DATABASE evm_db;"
```

5. Ejecutar migraciones:

```bash
alembic upgrade head
```

O usar el script SQL directo:

```bash
psql -U postgres -d evm_db -f scripts/init_db.sql
```

## Ejecución

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Documentación OpenAPI disponible en:
- Swagger UI: http://localhost:8000/api-docs
- ReDoc: http://localhost:8000/redoc

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET/POST | `/api/proyectos` | Listar / Crear proyectos |
| GET/PUT/DELETE | `/api/proyectos/{id}` | CRUD proyecto individual |
| GET/POST | `/api/proyectos/{id}/actividades` | Listar / Crear actividades |
| GET/PUT/DELETE | `/api/actividades/{id}` | CRUD actividad individual |
| GET | `/api/proyectos/{id}/evm` | Indicadores EVM consolidados del proyecto |
| GET | `/api/actividades/{id}/evm` | Indicadores EVM de una actividad |
| GET/POST | `/api/recursos` | Listar / Crear recursos |
| GET/POST | `/api/tipos-recurso` | Listar / Crear tipos de recurso |

## Pruebas

```bash
# Todas las pruebas
pytest -v

# Solo unitarias
pytest tests/unit -v

# Solo integración
pytest tests/integration -v

# Con cobertura
pytest --cov=app -v
```

## Nota sobre autenticación

Este módulo está diseñado como un microservicio dentro de una arquitectura más amplia.
En producción depende de un middleware de autenticación externo (WSO2 / API Gateway) que
debe ser provisto por la arquitectura base del proyecto. No se incluye autenticación en
este demo para mantener el foco en la funcionalidad EVM.

## Fórmulas EVM implementadas

| Indicador | Fórmula | Descripción |
|-----------|---------|-------------|
| PV | % planificado × BAC | Planned Value |
| EV | % completado × BAC | Earned Value |
| CV | EV − AC | Cost Variance |
| SV | EV − PV | Schedule Variance |
| CPI | EV / AC | Cost Performance Index |
| SPI | EV / PV | Schedule Performance Index |
| EAC | BAC / CPI | Estimate at Completion |
| VAC | BAC − EAC | Variance at Completion |

Interpretación: CPI > 1 = bajo presupuesto, CPI < 1 = sobre presupuesto.
SPI > 1 = adelantado, SPI < 1 = atrasado.

## Datos de ejemplo

```bash
python scripts/seed.py
```
