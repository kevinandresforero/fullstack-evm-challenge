from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.actividad_repository import ActividadRepository
from app.repositories.proyecto_repository import ProyectoRepository
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from app.services.evm_service import EvmService
from app.services.proyecto_service import ProyectoService

router = APIRouter(prefix="/api/proyectos", tags=["Proyectos"])


def _build_service(db: Session) -> ProyectoService:
    return ProyectoService(repo=ProyectoRepository(db))


@router.get("", response_model=list[ProyectoResponse])
def listar_proyectos(db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.listar()


@router.post("", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
def crear_proyecto(data: ProyectoCreate, db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.crear(data)


@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def obtener_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.obtener(proyecto_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto(proyecto_id: int, data: ProyectoUpdate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.actualizar(proyecto_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{proyecto_id}", response_model=ProyectoResponse)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.eliminar(proyecto_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{proyecto_id}/evm")
def obtener_evm_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto_service = _build_service(db)
    actividad_repo = ActividadRepository(db)
    evm_service = EvmService()
    try:
        proyecto = proyecto_service.obtener(proyecto_id)
        actividades = actividad_repo.get_by_proyecto(proyecto_id)
        resultado = evm_service.calcular_indicadores_proyecto(
            proyecto_id=proyecto.id,
            proyecto_nombre=proyecto.nombre,
            actividades=actividades,
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
