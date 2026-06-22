from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.actividad import Actividad
from app.models.proyecto import Proyecto

TEST_DATABASE_URL = "sqlite:///./test_evm.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def proyecto_data():
    return {
        "nombre": "Proyecto de prueba",
        "descripcion": "Descripción del proyecto",
        "fecha_inicio": date(2026, 1, 1),
        "fecha_fin": date(2026, 12, 31),
    }


@pytest.fixture
def actividad_data():
    return {
        "nombre": "Actividad de prueba",
        "descripcion": "Descripción de actividad",
        "presupuesto": Decimal("10000"),
        "porcentaje_avance_planificado": Decimal("50"),
        "porcentaje_avance_real": Decimal("30"),
        "costo_real": Decimal("4000"),
        "recursos": "2 ingenieros",
        "fecha_inicio": date(2026, 3, 1),
        "fecha_fin": date(2026, 6, 30),
    }


@pytest.fixture
def proyecto_db(db_session):
    p = Proyecto(
        nombre="Test Proyecto",
        descripcion="Test",
        fecha_inicio=date(2026, 1, 1),
        fecha_fin=date(2026, 12, 31),
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def actividad_db(db_session, proyecto_db):
    a = Actividad(
        proyecto_id=proyecto_db.id,
        nombre="Test Actividad",
        presupuesto=Decimal("10000"),
        porcentaje_avance_planificado=Decimal("50"),
        porcentaje_avance_real=Decimal("30"),
        costo_real=Decimal("4000"),
    )
    db_session.add(a)
    db_session.commit()
    db_session.refresh(a)
    return a
