from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.tipo_recurso_repository import TipoRecursoRepository
from app.schemas.tipo_recurso import TipoRecursoCreate, TipoRecursoResponse, TipoRecursoUpdate
from app.services.tipo_recurso_service import TipoRecursoService

router = APIRouter(prefix="/api/tipos-recurso", tags=["Tipos de Recurso"])


def _build_service(db: Session) -> TipoRecursoService:
    return TipoRecursoService(repo=TipoRecursoRepository(db))


@router.get("", response_model=list[TipoRecursoResponse])
def listar_tipos(db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.listar()


@router.post("", response_model=TipoRecursoResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo(data: TipoRecursoCreate, db: Session = Depends(get_db)):
    service = _build_service(db)
    return service.crear(data)


@router.get("/{tipo_id}", response_model=TipoRecursoResponse)
def obtener_tipo(tipo_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.obtener(tipo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{tipo_id}", response_model=TipoRecursoResponse)
def actualizar_tipo(tipo_id: int, data: TipoRecursoUpdate, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.actualizar(tipo_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{tipo_id}", response_model=TipoRecursoResponse)
def eliminar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    service = _build_service(db)
    try:
        return service.eliminar(tipo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
