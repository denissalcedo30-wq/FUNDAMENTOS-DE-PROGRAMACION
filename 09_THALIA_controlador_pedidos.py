# Trabajo colaborativo La Fortuna | DIA_2_IMPLEMENTACION | YTALIA
# Archivo de referencia: controllers/pedido_controller.py
# Propósito: Registro, modificación y estados de pedidos.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

"""Controlador: valida entradas y coordina vista, modelo y auditoría."""
from datetime import datetime
from config import MENU, ESTADOS, FORMAS_PAGO
from services.validaciones import validar_dni, validar_nombre, validar_cantidad, validar_observacion, limpiar_espacios

class PedidoController:
    def __init__(self, modelo, auditoria, usuario="admin"):
        self.modelo, self.auditoria, self.usuario = modelo, auditoria, usuario
    def registrar(self, cliente, dni, producto, cantidad, observacion, forma_pago):
        cliente=limpiar_espacios(cliente)
        if not validar_nombre(cliente): raise ValueError("Ingrese nombres y apellidos válidos.")
        if not validar_dni(dni): raise ValueError("El DNI debe tener 8 dígitos válidos; no se admiten secuencias ni dígitos repetidos.")
        if producto not in MENU: raise ValueError("Seleccione un plato incluido en el menú.")
        if not validar_cantidad(cantidad): raise ValueError("La cantidad debe estar entre 1 y 50.")
        if forma_pago not in FORMAS_PAGO: raise ValueError("Forma de pago no válida.")
        observacion=limpiar_espacios(observacion) or "Sin observaciones"
        if len(observacion)>200: raise ValueError("La observación supera 200 caracteres.")
        precio=MENU[producto]; subtotal=round(precio*cantidad,2)
        if subtotal>10000: raise ValueError("El importe supera el máximo permitido.")
        datos={"codigo":self.modelo.siguiente_codigo(),"cliente":cliente.title(),"dni":dni,"producto":producto,"cantidad":cantidad,"precio":precio,"subtotal":subtotal,"observacion":observacion,"estado":ESTADOS[0],"forma_pago":forma_pago,"fecha_registro":datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        codigo=self.modelo.crear(datos)
        self.auditoria.registrar(self.usuario,"REGISTRAR","Pedido",codigo,"Pedido registrado")
        return codigo
    def cambiar_estado(self,codigo,estado):
        pedido=self.modelo.obtener(codigo)
        if not pedido: raise ValueError("No se encontró el pedido.")
        if estado not in ESTADOS: raise ValueError("Estado no válido.")
        if ESTADOS.index(estado)<ESTADOS.index(pedido["estado"]): raise ValueError("No se permite retroceder el estado.")
        if estado==pedido["estado"]: raise ValueError("El pedido ya tiene ese estado.")
        self.modelo.actualizar_estado(codigo,estado)
        self.auditoria.registrar(self.usuario,"CAMBIAR_ESTADO","Pedido",codigo,f"{pedido['estado']} -> {estado}")
    def eliminar(self,codigo):
        if not self.modelo.eliminar(codigo): raise ValueError("No se encontró el pedido.")
        self.auditoria.registrar(self.usuario,"ELIMINAR","Pedido",codigo,"Pedido eliminado")
    def modificar(self,codigo,cliente,dni,producto,cantidad,observacion,forma_pago):
        actual=self.modelo.obtener(codigo)
        if not actual: raise ValueError("No se encontró el pedido.")
        if actual["estado"] == ESTADOS[-1]:
            raise ValueError("No se puede modificar un pedido que ya fue atendido.")
        cliente = limpiar_espacios(cliente)
        observacion = limpiar_espacios(observacion)
        if not validar_nombre(cliente) or not validar_dni(dni) or producto not in MENU or not validar_cantidad(cantidad) or forma_pago not in FORMAS_PAGO:
            raise ValueError("Datos inválidos. Verifique nombre, DNI, plato, cantidad y pago.")
        if not validar_observacion(observacion):
            raise ValueError("La observación no puede superar 200 caracteres.")
        subtotal = round(MENU[producto] * cantidad, 2)
        if subtotal > 10000:
            raise ValueError("El importe supera el máximo permitido de S/ 10,000.00.")
        self.modelo.actualizar_datos(codigo,cliente.title(),dni,producto,cantidad,MENU[producto],observacion or "Sin observaciones",forma_pago)
        self.auditoria.registrar(self.usuario,"MODIFICAR","Pedido",codigo,"Datos del pedido actualizados")
