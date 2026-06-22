from decimal import Decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    actividad_detalle,
    actividades,
    proyectos,
    recursos,
    tipo_recursos,
)

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    docs_url="/api-docs",
    redoc_url="/redoc",
    json_encoders={Decimal: float},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proyectos.router)
app.include_router(actividades.router)
app.include_router(actividad_detalle.router)
app.include_router(recursos.router)
app.include_router(tipo_recursos.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "evm-project-manager"}
