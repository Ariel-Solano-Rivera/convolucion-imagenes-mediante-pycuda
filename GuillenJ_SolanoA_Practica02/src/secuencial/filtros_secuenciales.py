"""Entradas de los tres filtros ejecutados de forma secuencial en CPU."""
from src.configuracion import Filtro
from src.secuencial.laplaciano import laplaciano_cpu
from src.secuencial.media import media_cpu
from src.secuencial.nitidez import nitidez_cpu


# Escoge el filtro CPU solicitado por el experimento (devuelve ms).
def ejecutar_filtro_cpu(filtro, entrada, salida, ancho, alto, k, limite_segundos=None):
    if filtro == Filtro.MEDIA:
        return media_cpu(entrada, salida, ancho, alto, k, limite_segundos)
    if filtro == Filtro.NITIDEZ:
        return nitidez_cpu(entrada, salida, ancho, alto, k, limite_segundos)
    return laplaciano_cpu(entrada, salida, ancho, alto, k, limite_segundos)
