-- Trabajo colaborativo La Fortuna | DIA_1_BASE_Y_ANALISIS | ANGHIE
-- Archivo de referencia: database/schema.sql
-- Propósito: Estructura de tablas y relaciones SQLite.
-- Revisar antes de integrar; no ejecutar como migración automáticamente.

CREATE TABLE IF NOT EXISTS menu_platos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nombre TEXT NOT NULL UNIQUE,
 precio REAL NOT NULL CHECK(precio >= 0),
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1))
);
-- Esquema equivalente al definido en models/database.py
CREATE TABLE IF NOT EXISTS pedidos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 codigo TEXT NOT NULL UNIQUE,
 cliente TEXT NOT NULL CHECK(length(trim(cliente)) BETWEEN 3 AND 80),
 dni TEXT NOT NULL CHECK(length(dni)=8 AND dni NOT GLOB '*[^0-9]*'),
 producto TEXT NOT NULL,
 cantidad INTEGER NOT NULL CHECK(cantidad BETWEEN 1 AND 50),
 precio REAL NOT NULL CHECK(precio >= 0),
 subtotal REAL NOT NULL CHECK(subtotal BETWEEN 0 AND 10000),
 observacion TEXT NOT NULL CHECK(length(observacion)<=200),
 estado TEXT NOT NULL CHECK(estado IN ('Pendiente','En preparación','Atendido')),
 forma_pago TEXT NOT NULL CHECK(forma_pago IN ('Yape','Efectivo','Plin')),
 fecha_registro TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS usuarios (
 id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL UNIQUE, email TEXT UNIQUE,
 password_hash TEXT NOT NULL, salt TEXT NOT NULL,
 rol TEXT NOT NULL CHECK(rol IN ('admin','operador')),
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1)), creado_en TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS auditoria (
 id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL,
 accion TEXT NOT NULL, entidad TEXT NOT NULL, clave_entidad TEXT,
 detalle TEXT, fecha TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_pedidos_dni ON pedidos(dni);
CREATE INDEX IF NOT EXISTS idx_pedidos_estado ON pedidos(estado);
CREATE INDEX IF NOT EXISTS idx_pedidos_fecha ON pedidos(fecha_registro);\n