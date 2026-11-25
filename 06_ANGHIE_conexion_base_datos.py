# Trabajo colaborativo La Fortuna | DIA_2_IMPLEMENTACION | ANGHIE
# Archivo de referencia: models/database.py
# Propósito: Conexión e inicialización SQLite.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

"""Conexión, esquema y acceso persistente a SQLite."""
import sqlite3
from contextlib import contextmanager
from config import DATA_DIR, DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS pedidos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 codigo TEXT NOT NULL UNIQUE,
 cliente TEXT NOT NULL CHECK(length(trim(cliente)) BETWEEN 3 AND 80),
 dni TEXT NOT NULL CHECK(length(dni)=8 AND dni NOT GLOB '*[^0-9]*'),
 producto TEXT NOT NULL,
 cantidad INTEGER NOT NULL CHECK(cantidad BETWEEN 1 AND 50),
 precio REAL NOT NULL CHECK(precio >= 0),
 subtotal REAL NOT NULL CHECK(subtotal >= 0 AND subtotal <= 10000),
 observacion TEXT NOT NULL CHECK(length(observacion)<=200),
 estado TEXT NOT NULL CHECK(estado IN ('Pendiente','En preparación','Atendido')),
 forma_pago TEXT NOT NULL CHECK(forma_pago IN ('Yape','Efectivo','Plin')),
 fecha_registro TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS menu_platos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nombre TEXT NOT NULL UNIQUE,
 precio REAL NOT NULL CHECK(precio >= 0),
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1))
);
CREATE TABLE IF NOT EXISTS usuarios (
 id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, email TEXT UNIQUE,
 password_hash TEXT NOT NULL, salt TEXT NOT NULL,
 rol TEXT NOT NULL DEFAULT 'admin', activo INTEGER NOT NULL DEFAULT 1,
 creado_en TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS auditoria (
 id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL,
 accion TEXT NOT NULL, entidad TEXT NOT NULL, clave_entidad TEXT,
 detalle TEXT, fecha TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_pedidos_dni ON pedidos(dni);
CREATE INDEX IF NOT EXISTS idx_pedidos_estado ON pedidos(estado);
CREATE INDEX IF NOT EXISTS idx_pedidos_fecha ON pedidos(fecha_registro);
"""

@contextmanager
def conectar():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def inicializar():
    with conectar() as db:
        db.executescript(SCHEMA)
        # El máximo de 50 es por cantidad de platos en cada pedido, no por cliente.
        db.execute("DROP TRIGGER IF EXISTS trg_max_50_pedidos")
        db.execute("DROP TRIGGER IF EXISTS trg_max_50_pedidos_update")
        columnas = {fila["name"] for fila in db.execute("PRAGMA table_info(usuarios)").fetchall()}
        if "email" not in columnas:
            db.execute("ALTER TABLE usuarios ADD COLUMN email TEXT")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email) WHERE email IS NOT NULL")

def consultar(sql, parametros=()):
    with conectar() as db:
        return [dict(r) for r in db.execute(sql, parametros).fetchall()]

def ejecutar(sql, parametros=()):
    with conectar() as db:
        cur = db.execute(sql, parametros)
        return cur.lastrowid
