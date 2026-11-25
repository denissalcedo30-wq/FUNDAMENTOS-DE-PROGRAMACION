# Trabajo colaborativo La Fortuna | DIA_1_BASE_Y_ANALISIS | ANDRIU
# Archivo de referencia: models/usuario_model.py
# Propósito: Modelo de usuarios y credenciales.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

"""Modelo de usuarios: contraseñas derivadas con PBKDF2 y sal aleatoria."""
import hashlib, hmac, secrets, re
from datetime import datetime
from models.database import conectar

class UsuarioModel:
    ITERACIONES = 240000

    def existe_admin(self):
        with conectar() as db:
            return db.execute("SELECT 1 FROM usuarios WHERE activo=1 AND rol='admin' LIMIT 1").fetchone() is not None

    def crear_admin(self, usuario, password, email=None):
        self._crear(usuario, password, email, "admin")

    def crear_operador(self, usuario, email, password):
        self._crear(usuario, password, email, "operador")

    def _crear(self, usuario, password, email, rol):
        usuario = usuario.strip()
        email = (email or "").strip().lower() or None
        if not 4 <= len(usuario) <= 40:
            raise ValueError("El usuario debe tener entre 4 y 40 caracteres.")
        if len(password) < 12:
            raise ValueError("La contraseña debe tener al menos 12 caracteres.")
        if email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise ValueError("Ingrese un correo electrónico válido.")
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, self.ITERACIONES).hex()
        with conectar() as db:
            db.execute("""INSERT INTO usuarios(usuario,email,password_hash,salt,rol,activo,creado_en)
                          VALUES(?,?,?,?,?,1,?)""",
                       (usuario, email, digest, salt.hex(), rol, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    def autenticar(self, usuario, password):
        with conectar() as db:
            fila = db.execute("SELECT * FROM usuarios WHERE (usuario=? OR email=?) AND activo=1",
                              (usuario.strip(), usuario.strip().lower())).fetchone()
        if not fila:
            # Trabajo ficticio para reducir diferencias de tiempo ante usuario inexistente.
            hashlib.pbkdf2_hmac("sha256", password.encode(), b"la-fortuna-salt", self.ITERACIONES)
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(fila["salt"]), self.ITERACIONES).hex()
        return hmac.compare_digest(actual, fila["password_hash"])

    def listar(self):
        with conectar() as db:
            return [dict(x) for x in db.execute("SELECT id,usuario,email,rol,activo,creado_en FROM usuarios ORDER BY id").fetchall()]