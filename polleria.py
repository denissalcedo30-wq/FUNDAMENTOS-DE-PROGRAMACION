# ==========================================================
# RESTAURANTE Y POLLERIA LA FORTUNA
# SISTEMA DE CONTROL DE ALMUERZOS
# ==========================================================

import unicodedata
from difflib import SequenceMatcher


# ==========================================================
# 1. COLORES PARA LA TERMINAL
# ==========================================================

ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CIAN = "\033[96m"
BLANCO = "\033[97m"
NEGRITA = "\033[1m"
RESET = "\033[0m"


# ==========================================================
# 2. LISTAS PARA ALMACENAR LOS PEDIDOS
# ==========================================================

codigos = []
clientes = []
dnis = []
productos = []
cantidades = []
precios = []
subtotales = []
observaciones = []
estados = []
formas_pago = []


# ==========================================================
# 3. MENU DE PLATOS Y PRECIOS
# ==========================================================

menu = {
    "arroz con pollo": 12.00,
    "lomo saltado": 15.00,
    "pollo a la plancha": 13.00,
    "tallarin saltado": 12.00,
    "caldo de gallina": 12.00,
    "milanesa de pollo": 14.00,
    "seco de res con frejoles": 15.00,
    "aji de gallina": 12.00
}


# ==========================================================
# 4. FUNCIONES PARA VALIDAR Y NORMALIZAR DATOS
# ==========================================================

def normalizar(texto):
    """Convierte el texto a minusculas y elimina las tildes."""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def leer_entero(mensaje, minimo=None, maximo=None):
    while True:
        entrada = input(mensaje).strip()

        try:
            numero = int(entrada)

            if minimo is not None and numero < minimo:
                print(
                    f"{ROJO}El valor minimo permitido es "
                    f"{minimo}.{RESET}"
                )
                continue

            if maximo is not None and numero > maximo:
                print(
                    f"{ROJO}El valor maximo permitido es "
                    f"{maximo}.{RESET}"
                )
                continue

            return numero

        except ValueError:
            print(
                f"{ROJO}Error: debes ingresar un numero entero "
                f"valido.{RESET}"
            )


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print(
            f"{ROJO}Error: este campo no puede quedar vacio.{RESET}"
        )


def leer_dni():
    while True:
        dni = input("DNI del cliente (8 digitos): ").strip()

        if len(dni) == 8 and dni.isdigit():
            return dni

        print(
            f"{ROJO}DNI incorrecto. Debe contener exactamente "
            f"8 digitos numericos, sin letras.{RESET}"
        )


# ==========================================================
# 5. GENERAR CODIGOS UNICOS PARA LOS PEDIDOS
# ==========================================================

def generar_codigo():
    """
    Genera codigos consecutivos:
    F0001, F0002, F0003...
    Comprueba que el codigo no este registrado.
    """

    numero = 1

    while True:
        codigo = f"F{numero:04d}"

        if codigo not in codigos:
            return codigo

        numero += 1


def buscar_pedido(codigo):
    codigo = codigo.strip().upper()

    for i, cod in enumerate(codigos):
        if cod.upper() == codigo:
            return i

    return -1


# ==========================================================
# 6. MOSTRAR EL MENU DE ALMUERZOS
# ==========================================================

def mostrar_menu_almuerzos():
    print()
    print(f"{AMARILLO}{NEGRITA}")
    print("╔══════════════════════════════════════════════════╗")
    print("║          RESTAURANTE LA FORTUNA                  ║")
    print("║                MENU DE ALMUERZOS                 ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"{RESET}")

    for numero, (plato, precio) in enumerate(menu.items(), start=1):
        print(
            f"  {CIAN}{numero:>2}.{RESET} "
            f"{BLANCO}{plato.title():<32}{RESET}"
            f"{VERDE} S/ {precio:5.2f}{RESET}"
        )

    print(f"{AMARILLO}{NEGRITA}")
    print("╚══════════════════════════════════════════════════╝")
    print(f"{RESET}")


# ==========================================================
# 7. BUSCADOR INTELIGENTE Y SELECCION DE PLATOS
# ==========================================================

def seleccionar_plato():
    platos = list(menu.keys())

    while True:
        print()
        print(f"{MAGENTA}{NEGRITA}BUSCADOR DE PLATOS{RESET}")
        print(
            f"{BLANCO}Escribe el nombre, una parte del nombre "
            f"o el numero del plato.{RESET}"
        )
        print(
            f"{AMARILLO}Ejemplos: arroz, ARROS, pollo, 1. "
            f"Escribe 0 para cancelar.{RESET}"
        )

        entrada = input(
            f"{CIAN}¿Que plato deseas?: {RESET}"
        ).strip()

        if entrada == "0":
            print(f"{AMARILLO}Seleccion cancelada.{RESET}")
            return None

        if not entrada:
            print(f"{ROJO}Escribe un nombre o numero.{RESET}")
            continue

        # Seleccionar directamente mediante el numero del menu
        if entrada.isdigit():
            numero = int(entrada)

            if 1 <= numero <= len(platos):
                plato = platos[numero - 1]

                print(
                    f"{VERDE}Plato seleccionado: "
                    f"{plato.title()} - S/ {menu[plato]:.2f}{RESET}"
                )

                return plato

            print(
                f"{ROJO}Numero no valido. Selecciona una opcion "
                f"del menu.{RESET}"
            )
            continue

        busqueda = normalizar(entrada)

        # Buscar nombres que contengan el texto ingresado
        coincidencias = [
            plato for plato in platos
            if busqueda in normalizar(plato)
        ]

        # Si no hay coincidencias directas, buscar errores
        # pequenos de escritura, como ARROS en lugar de arroz.
        if not coincidencias:
            puntuaciones = []

            for plato in platos:
                palabras_plato = normalizar(plato).split()
                mejor_puntaje = 0

                for palabra in busqueda.split():
                    for palabra_plato in palabras_plato:
                        puntaje = SequenceMatcher(
                            None,
                            palabra,
                            palabra_plato
                        ).ratio()

                        mejor_puntaje = max(
                            mejor_puntaje,
                            puntaje
                        )

                if mejor_puntaje >= 0.65:
                    puntuaciones.append((plato, mejor_puntaje))

            puntuaciones.sort(
                key=lambda elemento: elemento[1],
                reverse=True
            )

            coincidencias = [
                plato for plato, puntaje in puntuaciones
            ]

        # Mostrar las coincidencias para que el cliente elija
        if coincidencias:
            print()
            print(
                f"{VERDE}{NEGRITA}¡ENCONTRAMOS ESTAS OPCIONES!{RESET}"
            )

            for numero, plato in enumerate(coincidencias, start=1):
                print(
                    f"{CIAN}{numero}.{RESET} "
                    f"{BLANCO}{plato.title()}{RESET}"
                    f"{VERDE} - S/ {menu[plato]:.2f}{RESET}"
                )

            print(
                f"{AMARILLO}0. Volver a escribir la busqueda{RESET}"
            )

            opcion = leer_entero(
                f"{MAGENTA}Selecciona el plato: {RESET}",
                0,
                len(coincidencias)
            )

            if opcion == 0:
                continue

            plato_elegido = coincidencias[opcion - 1]

            print()
            print(
                f"{VERDE}{NEGRITA}¡PLATO CONFIRMADO!{RESET}"
            )
            print(f"Plato: {plato_elegido.title()}")
            print(f"Precio: S/ {menu[plato_elegido]:.2f}")

            return plato_elegido

        print(
            f"{ROJO}No encontramos una coincidencia clara.{RESET}"
        )
        print(
            f"{AMARILLO}Puedes escribir otra vez el nombre "
            f"o seleccionar un numero del menu.{RESET}"
        )
        mostrar_menu_almuerzos()


# ==========================================================
# 8. SELECCIONAR FORMA DE PAGO
# ==========================================================

def seleccionar_forma_pago():
    print()
    print(f"{MAGENTA}{NEGRITA}")
    print("╔══════════════════════════════════════╗")
    print("║             FORMAS DE PAGO           ║")
    print("╠══════════════════════════════════════╣")
    print(f"{RESET}")
    print(f"  {CIAN}1.{RESET} Yape")
    print(f"  {CIAN}2.{RESET} Efectivo")
    print(f"  {CIAN}3.{RESET} Plin")
    print(f"{MAGENTA}{NEGRITA}╚══════════════════════════════════════╝{RESET}")

    opcion = leer_entero(
        "Selecciona tu forma de pago (1-3): ", 1, 3
    )

    formas = {
        1: "Yape",
        2: "Efectivo",
        3: "Plin"
    }

    return formas[opcion]


# ==========================================================
# 9. REGISTRAR UN PEDIDO
# ==========================================================

def registrar_pedido():
    if len(codigos) >= 100:
        print(
            f"{ROJO}Se alcanzo el limite de 100 pedidos.{RESET}"
        )
        return

    print()
    print(f"{AZUL}{NEGRITA}========== REGISTRO DE PEDIDO =========={RESET}")

    cliente = leer_texto("Nombre completo del cliente: ")
    dni = leer_dni()

    mostrar_menu_almuerzos()

    producto_elegido = seleccionar_plato()

    if producto_elegido is None:
        print(
            f"{AMARILLO}Registro cancelado. "
            f"No se guardo el pedido.{RESET}"
        )
        return

    producto = producto_elegido.title()
    precio = menu[producto_elegido]

    cantidad = leer_entero("Cantidad de platos: ", 1)

    observacion = input(
        "Observaciones (Enter si no hay): "
    ).strip()

    if not observacion:
        observacion = "Sin observaciones"

    forma_pago = seleccionar_forma_pago()

    subtotal = precio * cantidad
    codigo = generar_codigo()

    # Guardar todos los datos del pedido
    codigos.append(codigo)
    clientes.append(cliente)
    dnis.append(dni)
    productos.append(producto)
    cantidades.append(cantidad)
    precios.append(precio)
    subtotales.append(subtotal)
    observaciones.append(observacion)
    estados.append("Pendiente")
    formas_pago.append(forma_pago)

    # Mostrar comprobante del pedido
    print()
    print(f"{VERDE}{NEGRITA}")
    print("╔══════════════════════════════════════════════╗")
    print("║            ¡PEDIDO REGISTRADO!               ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"{RESET}")
    print(f"  Codigo:          {CIAN}{codigo}{RESET}")
    print(f"  Cliente:         {cliente}")
    print(f"  DNI:             {dni}")
    print(f"  Plato:           {producto}")
    print(f"  Precio unitario: S/ {precio:.2f}")
    print(f"  Cantidad:        {cantidad}")
    print(f"  Forma de pago:   {forma_pago}")
    print(f"  Estado:          {AMARILLO}Pendiente{RESET}")
    print(f"  Observaciones:   {observacion}")
    print(f"{VERDE}{NEGRITA}  TOTAL A PAGAR: S/ {subtotal:.2f}{RESET}")
    print(f"{VERDE}{NEGRITA}╚══════════════════════════════════════════════╝{RESET}")


# ==========================================================
# 10. CONSULTAR UN PEDIDO
# ==========================================================

def consultar_pedido():
    print()
    print(f"{AZUL}{NEGRITA}========== CONSULTAR PEDIDO =========={RESET}")
    print(
        f"{CIAN}Ingresa un codigo como F0001, F0002 o F0003.{RESET}"
    )

    codigo = input("Codigo del pedido: ").strip().upper()

    posicion = buscar_pedido(codigo)

    if posicion == -1:
        print(
            f"{ROJO}No se encontro el pedido con codigo "
            f"{codigo}.{RESET}"
        )
        print(
            f"{AMARILLO}Verifica el codigo e intentalo nuevamente.{RESET}"
        )
        return

    print()
    print(f"{CIAN}{NEGRITA}========== DATOS DEL PEDIDO =========={RESET}")
    print("Codigo:", codigos[posicion])
    print("Cliente:", clientes[posicion])
    print("DNI:", dnis[posicion])
    print("Plato:", productos[posicion])
    print(f"Precio unitario: S/ {precios[posicion]:.2f}")
    print("Cantidad:", cantidades[posicion])
    print(f"Total: S/ {subtotales[posicion]:.2f}")
    print("Forma de pago:", formas_pago[posicion])
    print("Observaciones:", observaciones[posicion])
    print("Estado:", estados[posicion])


# ==========================================================
# 11. MOSTRAR TODOS LOS PEDIDOS
# ==========================================================

def listar_pedidos():
    print()
    print(f"{AZUL}{NEGRITA}========== LISTA DE PEDIDOS =========={RESET}")

    if not codigos:
        print(
            f"{AMARILLO}Todavia no hay pedidos registrados.{RESET}"
        )
        return

    for i in range(len(codigos)):
        print(f"\n{AMARILLO}{'─' * 48}{RESET}")
        print(f"{CIAN}{NEGRITA}Codigo: {codigos[i]}{RESET}")
        print("Cliente:", clientes[i])
        print("DNI:", dnis[i])
        print("Plato:", productos[i])
        print(f"Precio unitario: S/ {precios[i]:.2f}")
        print("Cantidad:", cantidades[i])
        print(f"Total: S/ {subtotales[i]:.2f}")
        print("Forma de pago:", formas_pago[i])
        print("Observaciones:", observaciones[i])
        print("Estado:", estados[i])


# ==========================================================
# 12. ACTUALIZAR ESTADO DE UN PEDIDO
# ==========================================================

def actualizar_estado():
    print()
    print(f"{AZUL}{NEGRITA}")
    print("╔══════════════════════════════════════════════╗")
    print("║          ACTUALIZAR ESTADO DEL PEDIDO        ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"{RESET}")

    if not codigos:
        print(
            f"{AMARILLO}No hay pedidos registrados para actualizar.{RESET}"
        )
        return

    print(
        f"{CIAN}Ingresa el codigo del pedido, por ejemplo F0001.{RESET}"
    )

    codigo = input(
        f"{MAGENTA}Codigo del pedido: {RESET}"
    ).strip().upper()

    # Comprobar que tenga el formato F0001
    if (
        len(codigo) != 5
        or not codigo.startswith("F")
        or not codigo[1:].isdigit()
    ):
        print(f"{ROJO}El formato del codigo es incorrecto.{RESET}")
        print(
            f"{AMARILLO}Debes ingresar un codigo como "
            f"F0001, F0002 o F0003.{RESET}"
        )
        return

    posicion = buscar_pedido(codigo)

    if posicion == -1:
        print(
            f"{ROJO}No existe un pedido registrado con el codigo "
            f"{codigo}.{RESET}"
        )
        print(
            f"{AMARILLO}Verifica el codigo en la lista de pedidos.{RESET}"
        )
        return

    print()
    print(f"{CIAN}{NEGRITA}DATOS DEL PEDIDO{RESET}")
    print(f"Codigo: {codigos[posicion]}")
    print(f"Cliente: {clientes[posicion]}")
    print(f"Plato: {productos[posicion]}")
    print(f"Estado actual: {AMARILLO}{estados[posicion]}{RESET}")

    print()
    print(f"{MAGENTA}{NEGRITA}SELECCIONA EL NUEVO ESTADO{RESET}")
    print(f"{CIAN}1. Pendiente{RESET}")
    print(f"{AMARILLO}2. En preparacion{RESET}")
    print(f"{VERDE}3. Atendido{RESET}")

    opcion = leer_entero(
        "Selecciona el nuevo estado (1-3): ", 1, 3
    )

    estados_nuevos = {
        1: "Pendiente",
        2: "En preparacion",
        3: "Atendido"
    }

    estados[posicion] = estados_nuevos[opcion]

    print()
    print(
        f"{VERDE}{NEGRITA}¡ESTADO ACTUALIZADO CORRECTAMENTE!{RESET}"
    )
    print(f"Codigo del pedido: {codigos[posicion]}")
    print(f"Nuevo estado: {VERDE}{estados[posicion]}{RESET}")


# ==========================================================
# 13. CONTAR PEDIDOS REGISTRADOS
# ==========================================================

def contar_pedidos():
    print()
    print(f"{CIAN}{NEGRITA}")
    print("╔══════════════════════════════════════╗")
    print(f"║ PEDIDOS REGISTRADOS: {len(codigos):<13}║")
    print("╚══════════════════════════════════════╝")
    print(f"{RESET}")


# ==========================================================
# 14. MENU PRINCIPAL
# ==========================================================

def menu_principal():
    while True:
        print()
        print(f"{AZUL}{NEGRITA}")
        print("╔══════════════════════════════════════════════╗")
        print("║       RESTAURANTE Y POLLERIA LA FORTUNA      ║")
        print("║            SISTEMA DE ALMUERZOS              ║")
        print("╠══════════════════════════════════════════════╣")
        print(f"{RESET}")
        print(f"  {VERDE}1.{RESET} Registrar un pedido")
        print(f"  {CIAN}2.{RESET} Consultar un pedido")
        print(f"  {AMARILLO}3.{RESET} Mostrar todos los pedidos")
        print(f"  {MAGENTA}4.{RESET} Actualizar estado del pedido")
        print(f"  {AZUL}5.{RESET} Contar pedidos registrados")
        print(f"  {VERDE}6.{RESET} Ver menu y precios")
        print(f"  {ROJO}7.{RESET} Salir")
        print(f"{AZUL}{NEGRITA}╚══════════════════════════════════════════════╝{RESET}")

        opcion = leer_entero(
            f"{MAGENTA}{NEGRITA}Selecciona una opcion (1-7): {RESET}",
            1,
            7
        )

        if opcion == 1:
            registrar_pedido()

        elif opcion == 2:
            consultar_pedido()

        elif opcion == 3:
            listar_pedidos()

        elif opcion == 4:
            actualizar_estado()

        elif opcion == 5:
            contar_pedidos()

        elif opcion == 6:
            mostrar_menu_almuerzos()

        elif opcion == 7:
            print()
            print(
                f"{VERDE}{NEGRITA}¡Gracias por utilizar "
                f"el sistema de La Fortuna!{RESET}"
            )
            break


# ==========================================================
# 15. INICIAR EL PROGRAMA
# ==========================================================

if __name__ == "__main__":
    menu_principal()
