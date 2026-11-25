# Trabajo colaborativo La Fortuna | DIA_2_IMPLEMENTACION | ANDRIU
# Archivo de referencia: controllers/auth_controller.py
# Propósito: Controlador de autenticación.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

"""Controlador de autenticación y altas de usuarios."""
class AuthController:
    def __init__(self, modelo):
        self.modelo = modelo

    def crear_admin_inicial(self, usuario, password, email=None):
        self.modelo.crear_admin(usuario, password, email)

    def crear_cuenta(self, usuario, email, password):
        self.modelo.crear_operador(usuario, email, password)

    def autenticar(self, usuario, password):
        return self.modelo.autenticar(usuario, password)
