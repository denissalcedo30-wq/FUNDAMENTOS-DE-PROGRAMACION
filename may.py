# ============================================================
# SISTEMA DE ORIENTACIÓN Y REGISTRO DE ATENCIONES
# MÓDULO DE SOPORTE ACADÉMICO
# Lenguaje: Python
# ============================================================

# Lista de tipos de consulta permitidos
TIPOS_CONSULTA = ["matrícula", "pagos", "constancia", "plataforma", "otro"]


# ------------------------------------------------------------
# FUNCIÓN 1: Mostrar menú principal
# Función sin retorno
# ------------------------------------------------------------
def mostrar_menu():
    print("\n==============================================")
    print("   SOPORTE ACADÉMICO - MENÚ PRINCIPAL")
    print("==============================================")
    print("1. Registrar solicitud")
    print("2. Mostrar solicitudes registradas")
    print("3. Salir")
    print("==============================================")


# ------------------------------------------------------------
# FUNCIÓN 2: Validar texto obligatorio
# Función con retorno
# ------------------------------------------------------------
def validar_texto(texto):
    if texto.strip() != "":
        return True
    return False


# ------------------------------------------------------------
# FUNCIÓN 3: Validar código del estudiante
# Función con retorno
# ------------------------------------------------------------
def validar_codigo(codigo, longitud_minima=5):
    codigo = codigo.strip()

    if codigo != "" and len(codigo) >= longitud_minima:
        return True

    return False


# ------------------------------------------------------------
# FUNCIÓN 4: Validar tipo de consulta
# Función con retorno
# ------------------------------------------------------------
def validar_tipo_consulta(tipo):
    tipo = tipo.strip().lower()

    if tipo in TIPOS_CONSULTA:
        return True

    return False


# ------------------------------------------------------------
# FUNCIÓN 5: Asignar prioridad
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
# FUNCIÓN 6: Mostrar resumen de una solicitud
# ------------------------------------------------------------
def mostrar_resumen(solicitud):
    print("\n----------------------------------------------")
    print("          RESUMEN DE SOLICITUD")
    print("----------------------------------------------")
    print("Código de estudiante :", solicitud["codigo"])
    print("Nombre               :", solicitud["nombre"])
    print("Tipo de consulta     :", solicitud["tipo"])
    print("Descripción          :", solicitud["descripcion"])
    print("Prioridad            :", solicitud["prioridad"])
    print("----------------------------------------------")


# ------------------------------------------------------------
# FUNCIÓN 7: Registrar una solicitud
# ------------------------------------------------------------
def registrar_solicitud():
    print("\n==============================================")
    print("          REGISTRO DE SOLICITUD")
    print("==============================================")

    # Validación del código
    while True:
        codigo = input("Código de estudiante: ")

        if validar_codigo(codigo):
            break

        print("Error: el código no puede estar vacío")
        print("y debe tener como mínimo 5 caracteres.")

    # Validación del nombre
    while True:
        nombre = input("Nombre del estudiante: ")

        if validar_texto(nombre):
            break

        print("Error: el nombre es obligatorio.")

    # Validación del tipo de consulta
    while True:
        print("\nTipos de consulta permitidos:")
        print("matrícula")
        print("pagos")
        print("constancia")
        print("plataforma")
        print("otro")

        tipo = input("Tipo de consulta: ").strip().lower()

        if validar_tipo_consulta(tipo):
            break

        print("Error: tipo de consulta incorrecto.")

    # Validación de descripción
    while True:
        descripcion = input("Descripción breve: ")

        if validar_texto(descripcion):
            break

        print("Error: la descripción es obligatoria.")

    # Asignación de prioridad
    prioridad = asignar_prioridad(tipo)

    # Se crea la solicitud
    solicitud = {
        "codigo": codigo,
        "nombre": nombre,
        "tipo": tipo,
        "descripcion": descripcion,
        "prioridad": prioridad
    }

    return solicitud


# ------------------------------------------------------------
# FUNCIÓN 8: Mostrar todas las solicitudes
# ------------------------------------------------------------
def mostrar_solicitudes(solicitudes):
    if len(solicitudes) == 0:
        print("\nNo existen solicitudes registradas.")
        return

    print("\n==============================================")
    print("       SOLICITUDES REGISTRADAS")
    print("==============================================")

    for i, solicitud in enumerate(solicitudes, start=1):
        print("\nSolicitud N°", i)
        mostrar_resumen(solicitud)


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

def main():

    # Variable local del programa principal
    solicitudes = []

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            # Permitimos registrar varias solicitudes
            solicitud = registrar_solicitud()

            solicitudes.append(solicitud)

            print("\nSolicitud registrada correctamente.")
            mostrar_resumen(solicitud)

        elif opcion == "2":

            mostrar_solicitudes(solicitudes)

        elif opcion == "3":

            print("\nPrograma finalizado.")
            print("Gracias por utilizar el sistema.")
            break

        else:

            print("\nError: opción no válida.")


# ------------------------------------------------------------
# INICIO DEL PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":
    main()