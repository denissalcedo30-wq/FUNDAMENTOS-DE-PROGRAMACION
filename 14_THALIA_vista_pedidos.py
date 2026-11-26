# Trabajo colaborativo La Fortuna | DIA_3_INTEGRACION_PRUEBAS | YTALIA
# Archivo de referencia: views/pedido_view.py
# Propósito: Vista de pedidos en consola.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

from config import MENU, FORMAS_PAGO, ESTADOS

def solicitar_pedido():
    print("\n--- REGISTRO DE PEDIDO ---")
    cliente=input("Nombres y apellidos: ").strip(); dni=input("DNI (8 dígitos): ").strip()
    platos=list(MENU)
    for i,p in enumerate(platos,1): print(f"{i}. {p} - S/ {MENU[p]:.2f}")
    try: producto=platos[int(input("Plato: "))-1]
    except (ValueError,IndexError): raise ValueError("Opción de plato no válida.")
    try: cantidad=int(input("Cantidad (1-50): "))
    except ValueError: raise ValueError("La cantidad debe ser un número entero.")
    observacion=input("Observaciones (opcional): ").strip()
    for i,p in enumerate(FORMAS_PAGO,1): print(f"{i}. {p}")
    try: pago=FORMAS_PAGO[int(input("Forma de pago: "))-1]
    except (ValueError,IndexError): raise ValueError("Forma de pago no válida.")
    return cliente,dni,producto,cantidad,observacion,pago

def mostrar_pedido(p):
    if not p: print("Pedido no encontrado."); return
    for k,v in p.items(): print(f"{k.replace('_',' ').title()}: {v}")

def mostrar_pedidos(filas):
    if not filas: print("No hay pedidos registrados."); return
    print("\nCODIGO | CLIENTE | PLATO | CANT. | TOTAL | ESTADO")
    for p in filas: print(f"{p['codigo']} | {p['cliente']} | {p['producto']} | {p['cantidad']} | S/ {p['subtotal']:.2f} | {p['estado']}")

def solicitar_codigo(): return input("Código del pedido: ").strip().upper()
