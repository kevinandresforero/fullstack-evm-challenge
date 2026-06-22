from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.actividad_detalle_repository import ActividadDetalleRepository
from app.repositories.actividad_repository import ActividadRepository
from app.schemas.actividad_detalle import ActividadDetalleCreate, ActividadDetalleResponse, ActividadDetalleUpdate
from app.services.actividad_detalle_service import ActividadDetalleService

router = APIRouter(prefix="/api/actividades/{actividad_id}/detalles", tags=["Detalles de Actividad"])


def _build_service(db: Session) -> ActividadDetalleService:
    return ActividadDetalleService(
        repo=ActividadDetalleRepository(db),
        actividad_repo=ActividadRepository(db),
    )


@router.get("", response_model=list[ActividadDetalleResponse])
def listar_detalles(actividad_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.listar_por_actividad(actividad_id)


@router.post("", response_model=ActividadDetalleResponse, status_code=status.HTTP_201_CREATED)
def crear_detalle(actividad_id: int, data: ActividadDetalleCreate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.crear(actividad_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{detalle_id}", response_model=ActividadDetalleResponse)
def obtener_detalle(actividad_id: int, detalle_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.obtener(detalle_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{detalle_id}", response_model=ActividadDetalleResponse)
def actualizar_detalle(actividad_id: int, detalle_id: int, data: ActividadDetalleUpdate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.actualizar(detalle_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{detalle_id}", response_model=ActividadDetalleResponse)
def eliminar_detalle(actividad_id: int, detalle_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.eliminar(detalle_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
