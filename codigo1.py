# ============================================================
# SISTEMA DE ORIENTACIÓN Y REGISTRO DE ATENCIONES
# MÓDULO DE SOPORTE ACADÉMICO
# Lenguaje: Python
# ============================================================
# ------------------------------------------------------------
# COLORES
# ------------------------------------------------------------
RESET = "\033[0m"
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLANCO = "\033[97m"
# ------------------------------------------------------------
# FUNCIÓN 1: Mostrar menú principal
# Función sin retorno
# ------------------------------------------------------------
def mostrar_menu():
    print(CYAN + "\n==============================================" + RESET)
    print(CYAN + "       SOPORTE ACADÉMICO - MENÚ PRINCIPAL" + RESET)
    print(CYAN + "==============================================" + RESET)

    print(AMARILLO + "1." + RESET + " Registrar solicitud")
    print(AMARILLO + "2." + RESET + " Mostrar solicitudes registradas")
    print(AMARILLO + "3." + RESET + " Salir")

    print(CYAN + "==============================================" + RESET)
# ------------------------------------------------------------
# FUNCIÓN 2: Mostrar tipos de consulta
# Función sin retorno
# ------------------------------------------------------------
def mostrar_tipos_consulta():
    print(MAGENTA + "\n==============================================" + RESET)
    print(MAGENTA + "          TIPOS DE CONSULTA" + RESET)
    print(MAGENTA + "==============================================" + RESET)

    print(AMARILLO + "1." + RESET + " Matrícula")
    print(AMARILLO + "2." + RESET + " Pagos")
    print(AMARILLO + "3." + RESET + " Constancia")
    print(AMARILLO + "4." + RESET + " Plataforma")
    print(AMARILLO + "5." + RESET + " Otro")

    print(MAGENTA + "==============================================" + RESET)


# ------------------------------------------------------------
# FUNCIÓN 3: Validar texto obligatorio
# Función con retorno
# ------------------------------------------------------------
def validar_texto(texto):
    if texto.strip() != "":
        return True

    return False


# ------------------------------------------------------------
# FUNCIÓN 4: Validar código del estudiante
# Función con retorno
# ------------------------------------------------------------
def validar_codigo(codigo, longitud_minima=5):
    codigo = codigo.strip()

    if codigo != "" and len(codigo) >= longitud_minima:
        return True

    return False


# ------------------------------------------------------------
# FUNCIÓN 5: Validar tipo de consulta
# Función con retorno
# ------------------------------------------------------------
def validar_tipo_consulta(opcion):
    if opcion >= 1 and opcion <= 5:
        return True

    return False


# ------------------------------------------------------------
# FUNCIÓN 6: Obtener tipo de consulta
# Función con retorno
# ------------------------------------------------------------
def obtener_tipo_consulta(opcion):

    if opcion == 1:
        return "Matrícula"

    elif opcion == 2:
        return "Pagos"

    elif opcion == 3:
        return "Constancia"

    elif opcion == 4:
        return "Plataforma"

    elif opcion == 5:
        return "Otro"


# ------------------------------------------------------------
# FUNCIÓN 7: Asignar prioridad
# Función con retorno
# ------------------------------------------------------------
def asignar_prioridad(tipo_consulta):

    tipo = tipo_consulta.strip().lower()

    if tipo == "plataforma":
        return "Alta"

    elif tipo == "pagos":
        return "Alta"

    elif tipo == "matrícula":
        return "Media"

    elif tipo == "constancia":
        return "Baja"

    else:
        return "Baja"


# ------------------------------------------------------------
# FUNCIÓN 8: Mostrar resumen de una solicitud
# ------------------------------------------------------------
def mostrar_resumen(solicitud):
    print(CYAN + "\n----------------------------------------------" + RESET)
    print(CYAN + "          RESUMEN DE SOLICITUD" + RESET)
    print(CYAN + "----------------------------------------------" + RESET)

    print(VERDE + "Código de estudiante :" + RESET,
          solicitud["codigo"])

    print(VERDE + "Nombre               :" + RESET,
          solicitud["nombre"])

    print(VERDE + "Tipo de consulta     :" + RESET,
          solicitud["tipo"])

    print(VERDE + "Descripción          :" + RESET,
          solicitud["descripcion"])

    print(VERDE + "Prioridad            :" + RESET,
          solicitud["prioridad"])

    print(CYAN + "----------------------------------------------" + RESET)


# ------------------------------------------------------------
# FUNCIÓN 9: Registrar una solicitud
# ------------------------------------------------------------
def registrar_solicitud():

    print(MAGENTA + "\n==============================================" + RESET)
    print(MAGENTA + "          REGISTRO DE SOLICITUD" + RESET)
    print(MAGENTA + "==============================================" + RESET)


    # --------------------------------------------------------
    # VALIDACIÓN DEL CÓDIGO
    # --------------------------------------------------------
    while True:

        codigo = input(AZUL + "Código de estudiante: " + RESET)

        if validar_codigo(codigo):
            break

        print(ROJO + "Error: el código no puede estar vacío." + RESET)
        print(ROJO + "Debe tener como mínimo 5 caracteres." + RESET)


    # --------------------------------------------------------
    # VALIDACIÓN DEL NOMBRE
    # --------------------------------------------------------
    while True:

        nombre = input(AZUL + "Nombre del estudiante: " + RESET)

        if validar_texto(nombre):
            break

        print(ROJO + "Error: el nombre es obligatorio." + RESET)


    # --------------------------------------------------------
    # SELECCIÓN DEL TIPO DE CONSULTA
    # --------------------------------------------------------
    while True:

        mostrar_tipos_consulta()

        try:

            opcion_consulta = int(
                input(VERDE + "Seleccione una opción (1-5): " + RESET)
            )

            if validar_tipo_consulta(opcion_consulta):
                break

            print(
                ROJO +
                "Error: seleccione una opción del 1 al 5." +
                RESET
            )

        except ValueError:

            print(
                ROJO +
                "Error: debe ingresar solamente un número." +
                RESET
            )


    # --------------------------------------------------------
    # OBTENER EL TIPO DE CONSULTA
    # --------------------------------------------------------
    tipo = obtener_tipo_consulta(opcion_consulta)


    # --------------------------------------------------------
    # VALIDACIÓN DE DESCRIPCIÓN
    # --------------------------------------------------------
    while True:

        descripcion = input(AZUL + "Descripción breve: " + RESET)

        if validar_texto(descripcion):
            break

        print(ROJO + "Error: la descripción es obligatoria." + RESET)


    # --------------------------------------------------------
    # ASIGNACIÓN DE PRIORIDAD
    # --------------------------------------------------------
    prioridad = asignar_prioridad(tipo)


    # --------------------------------------------------------
    # SE CREA LA SOLICITUD
    # --------------------------------------------------------
    solicitud = {
        "codigo": codigo,
        "nombre": nombre,
        "tipo": tipo,
        "descripcion": descripcion,
        "prioridad": prioridad
    }

    return solicitud


# ------------------------------------------------------------
# FUNCIÓN 10: Mostrar todas las solicitudes
# ------------------------------------------------------------
def mostrar_solicitudes(solicitudes):

    if len(solicitudes) == 0:

        print(
            ROJO +
            "\nNo existen solicitudes registradas." +
            RESET
        )

        return


    print(CYAN + "\n==============================================" + RESET)
    print(CYAN + "       SOLICITUDES REGISTRADAS" + RESET)
    print(CYAN + "==============================================" + RESET)


    for i, solicitud in enumerate(solicitudes, start=1):

        print(
            AMARILLO +
            "\nSolicitud N° " +
            str(i) +
            RESET
        )

        mostrar_resumen(solicitud)

# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------
def main():

    # Variable local del programa principal
    solicitudes = []


    while True:

        mostrar_menu()

        opcion = input(
            VERDE +
            "Seleccione una opción (1-3): " +
            RESET
        )


        # ----------------------------------------------------
        # OPCIÓN 1: REGISTRAR SOLICITUD
        # ----------------------------------------------------
        if opcion == "1":

            solicitud = registrar_solicitud()

            solicitudes.append(solicitud)

            print(
                VERDE +
                "\nSolicitud registrada correctamente." +
                RESET
            )

            mostrar_resumen(solicitud)


        # ----------------------------------------------------
        # OPCIÓN 2: MOSTRAR SOLICITUDES
        # ----------------------------------------------------
        elif opcion == "2":

            mostrar_solicitudes(solicitudes)


        # ----------------------------------------------------
        # OPCIÓN 3: SALIR
        # ----------------------------------------------------
        elif opcion == "3":

            print(CYAN + "\n==============================================" + RESET)
            print(VERDE + "             PROGRAMA FINALIZADO" + RESET)
            print(CYAN + "==============================================" + RESET)
            print("Gracias por utilizar el sistema.")

            break


        # ----------------------------------------------------
        # OPCIÓN INCORRECTA
        # ----------------------------------------------------
        else:

            print(
                ROJO +
                "\nError: opción no válida." +
                RESET
            )

            print(
                ROJO +
                "Seleccione solamente 1, 2 o 3." +
                RESET
            )


# ------------------------------------------------------------
# INICIO DEL PROGRAMA
# ------------------------------------------------------------
if __name__ == "__main__":
    main()