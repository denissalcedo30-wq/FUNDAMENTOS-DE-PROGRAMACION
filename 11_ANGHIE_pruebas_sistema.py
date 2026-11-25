# Trabajo colaborativo La Fortuna | DIA_3_INTEGRACION_PRUEBAS | ANGHIE
# Archivo de referencia: tests/test_sistema.py
# Propósito: Pruebas del sistema.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from models import database
from models.pedido_model import PedidoModel
from models.auditoria_model import AuditoriaModel
from controllers.pedido_controller import PedidoController
from services.exportacion_service import ExportacionService
from services.validaciones import validar_dni, validar_nombre, validar_cantidad

class SistemaMVC_Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.p1=patch.object(database,'DB_PATH',Path(self.tmp.name)/'test.db')
        self.p2=patch.object(database,'DATA_DIR',Path(self.tmp.name))
        self.p1.start(); self.p2.start(); database.inicializar()
        self.modelo=PedidoModel(); self.audit=AuditoriaModel(); self.ctrl=PedidoController(self.modelo,self.audit)
    def tearDown(self): self.p1.stop(); self.p2.stop(); self.tmp.cleanup()
    def registrar(self,dni='48271635'):
        return self.ctrl.registrar('María Fernanda Pérez',dni,'Arroz con pollo',2,'Sin observaciones','Yape')
    def test_validaciones(self):
        self.assertTrue(validar_dni('48271635')); self.assertFalse(validar_dni('12345678'))
        self.assertFalse(validar_dni('00000000')); self.assertTrue(validar_nombre('María Fernanda Pérez'))
        self.assertFalse(validar_nombre('Juan2 Perez')); self.assertTrue(validar_cantidad(50)); self.assertFalse(validar_cantidad(0))
    def test_crud_persistencia_y_resumen(self):
        codigo=self.registrar(); self.assertEqual(self.modelo.contar(),1)
        self.assertEqual(self.modelo.obtener(codigo)['subtotal'],24.0)
        self.ctrl.cambiar_estado(codigo,'En preparación')
        self.assertEqual(self.modelo.obtener(codigo)['estado'],'En preparación')
        self.assertEqual(self.modelo.resumen()['total'],1)
        self.ctrl.eliminar(codigo); self.assertEqual(self.modelo.contar(),0)
    def test_cliente_puede_registrar_mas_de_50_pedidos(self):
        for i in range(51):
            codigo = self.ctrl.registrar('María Fernanda Pérez','48271635',
                'Arroz con pollo',1,'','Yape')
        self.assertEqual(self.modelo.contar_por_dni('48271635'),51)

    def test_exportaciones_cinco_formatos(self):
        self.registrar(); servicio=ExportacionService(self.modelo)
        for formato in ('csv','json','txt','bin','pdf'):
            ruta=servicio.exportar(formato); self.assertTrue(ruta.exists()); self.assertGreater(ruta.stat().st_size,10)
            self.assertEqual(ruta.suffix,'.'+formato)

    def test_no_modifica_pedido_atendido(self):
        codigo=self.registrar()
        self.ctrl.cambiar_estado(codigo,'En preparación')
        self.ctrl.cambiar_estado(codigo,'Atendido')
        with self.assertRaises(ValueError):
            self.ctrl.modificar(codigo,'María Fernanda Pérez','48271635','Arroz con pollo',1,'','Yape')

    def test_no_permite_retroceder_estado(self):
        codigo=self.registrar()
        self.ctrl.cambiar_estado(codigo,'En preparación')
        with self.assertRaises(ValueError):
            self.ctrl.cambiar_estado(codigo,'Pendiente')

    def test_observacion_maxima(self):
        with self.assertRaises(ValueError):
            self.ctrl.registrar('María Fernanda Pérez','48271635','Arroz con pollo',1,'x'*201,'Yape')


    def test_cuenta_usuario_correo_y_password_hash(self):
        from models.usuario_model import UsuarioModel
        usuarios = UsuarioModel()
        usuarios.crear_operador("operador01", "operador@example.com", "ClaveSegura123!")
        self.assertTrue(usuarios.autenticar("operador01", "ClaveSegura123!"))
        self.assertTrue(usuarios.autenticar("operador@example.com", "ClaveSegura123!"))
        self.assertFalse(usuarios.autenticar("operador01", "incorrecta"))

    def test_auditoria(self):
        codigo=self.registrar(); filas=self.audit.listar()
        self.assertTrue(any(r['clave_entidad']==codigo for r in filas))

if __name__=='__main__': unittest.main(verbosity=2)
