"""
create initial tables

Revision ID: 001
Revises:
Create Date: 2026-06-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "proyecto",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_inicio", sa.Date(), nullable=False),
        sa.Column("fecha_fin", sa.Date(), nullable=False),
        sa.Column("fecha_modificacion", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("estado", sa.String(20), default="activo"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tipo_recurso",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_modificacion", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("estado", sa.String(20), default="activo"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "actividad",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("proyecto_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("presupuesto", sa.Numeric(12, 2), nullable=False),
        sa.Column("porcentaje_avance_planificado", sa.Numeric(5, 2), nullable=False, default=0),
        sa.Column("porcentaje_avance_real", sa.Numeric(5, 2), nullable=False, default=0),
        sa.Column("costo_real", sa.Numeric(12, 2), nullable=False, default=0),
        sa.Column("recursos", sa.Text(), nullable=True),
        sa.Column("fecha_inicio", sa.Date(), nullable=True),
        sa.Column("fecha_fin", sa.Date(), nullable=True),
        sa.Column("fecha_modificacion", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("estado", sa.String(20), default="activo"),
        sa.ForeignKeyConstraint(["proyecto_id"], ["proyecto.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "recurso",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("tipo_recurso_id", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_modificacion", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("estado", sa.String(20), default="activo"),
        sa.ForeignKeyConstraint(["tipo_recurso_id"], ["tipo_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "actividad_detalle",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("actividad_id", sa.Integer(), nullable=False),
        sa.Column("concepto", sa.String(255), nullable=False),
        sa.Column("cantidad", sa.Numeric(12, 2), default=1),
        sa.Column("costo_unitario", sa.Numeric(12, 2), default=0),
        sa.Column("fecha_modificacion", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("estado", sa.String(20), default="activo"),
        sa.ForeignKeyConstraint(["actividad_id"], ["actividad.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("actividad_detalle")
    op.drop_table("recurso")
    op.drop_table("actividad")
    op.drop_table("tipo_recurso")
    op.drop_table("proyecto")
