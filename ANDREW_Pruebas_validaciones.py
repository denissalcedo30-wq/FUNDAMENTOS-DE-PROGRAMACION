# Trabajo colaborativo La Fortuna | DIA_3_INTEGRACION_PRUEBAS | ANDRIU
# Archivo de referencia: tests/test_validaciones.py
# Propósito: Pruebas de validaciones.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

import unittest
from services.validaciones import validar_dni,validar_nombre,validar_cantidad
from services.recursividad import solo_digitos_recursivo
class ValidacionesTests(unittest.TestCase):
 def test_dni(self):
  for x in ['00000000','11111111','12345678','87654321','1234AB78','1234567','123456789',' 48271635','12000123','45111234','12121212','48277735'] : self.assertFalse(validar_dni(x))
  self.assertTrue(validar_dni('48271635'))
 def test_nombre(self):
  self.assertTrue(validar_nombre('María Fernanda Pérez')); self.assertFalse(validar_nombre('Juan2 Perez')); self.assertFalse(validar_nombre('Fernando'))
 def test_cantidad(self):
  self.assertTrue(validar_cantidad(1)); self.assertTrue(validar_cantidad(50)); self.assertFalse(validar_cantidad(0)); self.assertFalse(validar_cantidad(True))
 def test_recursividad_digitos(self):
  self.assertTrue(solo_digitos_recursivo('48271635')); self.assertFalse(solo_digitos_recursivo('4827A635')); self.assertTrue(solo_digitos_recursivo(''))
if __name__=='__main__': unittest.main(verbosity=2)
