from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.actividad_repository import ActividadRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.actividad import ActividadCreate, ActividadResponse, ActividadUpdate
from app.services.actividad_service import ActividadService
from app.services.evm_service import EvmService

router = APIRouter(prefix="/api/proyectos/{proyecto_id}/actividades", tags=["Actividades"])


def _build_service(db: Session) -> ActividadService:
    return ActividadService(
        repo=ActividadRepository(db),
        proyecto_repo=ProyectoRepository(db),
    )


@router.get("", response_model=list[ActividadResponse])
def listar_actividades(proyecto_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.listar_por_proyecto(proyecto_id)


@router.post("", response_model=ActividadResponse, status_code=status.HTTP_201_CREATED)
def crear_actividad(proyecto_id: int, data: ActividadCreate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.crear(proyecto_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{actividad_id}", response_model=ActividadResponse)
def obtener_actividad(proyecto_id: int, actividad_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.obtener(actividad_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{actividad_id}", response_model=ActividadResponse)
def actualizar_actividad(proyecto_id: int, actividad_id: int, data: ActividadUpdate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.actualizar(actividad_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{actividad_id}", response_model=ActividadResponse)
def eliminar_actividad(proyecto_id: int, actividad_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.eliminar(actividad_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{actividad_id}/evm")
def obtener_evm_actividad(proyecto_id: int, actividad_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    evm_service = EvmService()
    try:
        _, indicadores = service.obtener_con_evm(actividad_id, evm_service)
        return indicadores
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
