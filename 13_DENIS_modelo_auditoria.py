# Trabajo colaborativo La Fortuna | DIA_3_INTEGRACION_PRUEBAS | DENIS
# Archivo de referencia: models/auditoria_model.py
# Propósito: Registro de auditoría.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

from datetime import datetime
from models.database import conectar

class AuditoriaModel:
    def registrar(self, usuario, accion, entidad, clave="", detalle=""):
        with conectar() as db:
            db.execute("INSERT INTO auditoria(usuario,accion,entidad,clave_entidad,detalle,fecha) VALUES(?,?,?,?,?,?)",
                       (usuario, accion, entidad, str(clave), detalle, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    def listar(self, limite=100):
        with conectar() as db:
            return [dict(r) for r in db.execute("SELECT * FROM auditoria ORDER BY id DESC LIMIT ?", (limite,)).fetchall()]
