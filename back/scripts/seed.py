"""Script de datos de ejemplo para desarrollo local."""

from datetime import date

from app.database import SessionLocal
from app.models.actividad import Actividad
from app.models.proyecto import Proyecto
from app.models.tipo_recurso import TipoRecurso
from app.models.recurso import Recurso


def seed():
    db = SessionLocal()
    try:
        proyecto = Proyecto(
            nombre="Migración a plataforma cloud",
            descripcion="Migración de infraestructura on-premise a AWS",
            fecha_inicio=date(2026, 1, 1),
            fecha_fin=date(2026, 12, 31),
        )
        db.add(proyecto)
        db.flush()

        actividades = [
            Actividad(
                proyecto_id=proyecto.id,
                nombre="Levantamiento de inventario",
                presupuesto=10000,
                porcentaje_avance_planificado=100,
                porcentaje_avance_real=100,
                costo_real=9500,
                recursos="2 ingenieros, 1 semana",
            ),
            Actividad(
                proyecto_id=proyecto.id,
                nombre="Migración de base de datos",
                presupuesto=25000,
                porcentaje_avance_planificado=60,
                porcentaje_avance_real=40,
                costo_real=14000,
                recursos="1 DBA, 2 backend, 3 semanas",
            ),
            Actividad(
                proyecto_id=proyecto.id,
                nombre="Pruebas de integración",
                presupuesto=15000,
                porcentaje_avance_planificado=30,
                porcentaje_avance_real=20,
                costo_real=4000,
                recursos="1 QA, 1 DevOps, 2 semanas",
            ),
        ]
        for act in actividades:
            db.add(act)
        db.flush()

        tipo = TipoRecurso(nombre="Humano", descripcion="Recurso humano")
        db.add(tipo)
        db.flush()

        db.add(Recurso(nombre="Ingeniero de software", tipo_recurso_id=tipo.id))
        db.add(Recurso(nombre="DBA", tipo_recurso_id=tipo.id))
        db.add(Recurso(nombre="QA", tipo_recurso_id=tipo.id))

        db.commit()
        print("Datos de ejemplo insertados correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
