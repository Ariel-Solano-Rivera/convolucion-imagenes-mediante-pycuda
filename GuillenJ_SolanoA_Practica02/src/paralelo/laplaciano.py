"""Filtro laplaciano usando PyCUDA."""
from src.convolucion import ejecutar_gpu
from src.filtros.mascaras import crear_mascara_laplaciano


def laplaciano_gpu(entrada, salida, d_entrada, d_salida, d_mascara, ancho, alto, k, hilos):
    mascara = crear_mascara_laplaciano()
    return ejecutar_gpu(entrada, salida, mascara, d_entrada, d_salida, d_mascara,
                        ancho, alto, k, hilos)
