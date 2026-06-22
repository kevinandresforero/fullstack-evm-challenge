CREATE TABLE IF NOT EXISTS proyecto (
    id                SERIAL PRIMARY KEY,
    nombre            VARCHAR(255) NOT NULL,
    descripcion       TEXT,
    fecha_inicio      DATE NOT NULL,
    fecha_fin         DATE NOT NULL,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado            VARCHAR(20) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS actividad (
    id                          SERIAL PRIMARY KEY,
    proyecto_id                 INTEGER NOT NULL REFERENCES proyecto(id),
    nombre                      VARCHAR(255) NOT NULL,
    descripcion                 TEXT,
    presupuesto                 NUMERIC(12,2) NOT NULL,
    porcentaje_avance_planificado NUMERIC(5,2) NOT NULL DEFAULT 0,
    porcentaje_avance_real      NUMERIC(5,2) NOT NULL DEFAULT 0,
    costo_real                  NUMERIC(12,2) NOT NULL DEFAULT 0,
    recursos                    TEXT,
    fecha_inicio                DATE,
    fecha_fin                   DATE,
    fecha_modificacion          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado                      VARCHAR(20) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS tipo_recurso (
    id                SERIAL PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    descripcion       TEXT,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado            VARCHAR(20) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS recurso (
    id                SERIAL PRIMARY KEY,
    nombre            VARCHAR(255) NOT NULL,
    tipo_recurso_id   INTEGER NOT NULL REFERENCES tipo_recurso(id),
    descripcion       TEXT,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado            VARCHAR(20) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS actividad_detalle (
    id                SERIAL PRIMARY KEY,
    actividad_id      INTEGER NOT NULL REFERENCES actividad(id),
    concepto          VARCHAR(255) NOT NULL,
    cantidad          NUMERIC(12,2) DEFAULT 1,
    costo_unitario    NUMERIC(12,2) DEFAULT 0,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado            VARCHAR(20) DEFAULT 'activo'
);
