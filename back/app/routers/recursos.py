from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.recurso_repository import RecursoRepository
from app.repositories.tipo_recurso_repository import TipoRecursoRepository
from app.schemas.recurso import RecursoCreate, RecursoResponse, RecursoUpdate
from app.services.recurso_service import RecursoService

router = APIRouter(prefix="/api/recursos", tags=["Recursos"])


def _build_service(db: Session) -> RecursoService:
    return RecursoService(
        repo=RecursoRepository(db),
        tipo_recurso_repo=TipoRecursoRepository(db),
    )


@router.get("", response_model=list[RecursoResponse])
def listar_recursos(db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.listar()


@router.post("", response_model=RecursoResponse, status_code=status.HTTP_201_CREATED)
def crear_recurso(data: RecursoCreate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.crear(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{recurso_id}", response_model=RecursoResponse)
def obtener_recurso(recurso_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.obtener(recurso_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{recurso_id}", response_model=RecursoResponse)
def actualizar_recurso(recurso_id: int, data: RecursoUpdate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.actualizar(recurso_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{recurso_id}", response_model=RecursoResponse)
def eliminar_recurso(recurso_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.eliminar(recurso_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
