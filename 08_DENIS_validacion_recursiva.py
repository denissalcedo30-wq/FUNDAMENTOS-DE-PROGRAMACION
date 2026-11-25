# Trabajo colaborativo La Fortuna | DIA_2_IMPLEMENTACION | DENIS
# Archivo de referencia: services/recursividad.py
# Propósito: Validación recursiva.
# Copia de referencia del proyecto final; no sobrescribir sin revisar y probar.

"""Ejemplo aplicado de recursividad para revisar caracteres de un DNI.
Caso base: cadena vacía. Caso recursivo: validar el primer carácter y continuar con el resto.
"""
def solo_digitos_recursivo(texto: str) -> bool:
    if texto == "":
        return True
    if texto[0] not in "0123456789":
        return False
    return solo_digitos_recursivo(texto[1:])
