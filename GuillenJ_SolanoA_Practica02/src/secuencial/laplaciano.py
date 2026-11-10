"""Filtro laplaciano en CPU."""
from src.convolucion import ejecutar_cpu
from src.filtros.mascaras import crear_mascara_laplaciano


def laplaciano_cpu(entrada, salida, ancho, alto, k, limite_segundos=None):
    mascara = crear_mascara_laplaciano()
    return ejecutar_cpu(entrada, salida, mascara, ancho, alto, k, limite_segundos)
