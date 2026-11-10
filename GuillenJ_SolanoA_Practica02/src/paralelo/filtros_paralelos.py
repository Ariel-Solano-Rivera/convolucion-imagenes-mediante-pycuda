"""Entradas de los tres filtros ejecutados en paralelo mediante PyCUDA."""
from src.configuracion import Filtro
from src.paralelo.laplaciano import laplaciano_gpu
from src.paralelo.media import media_gpu
from src.paralelo.nitidez import nitidez_gpu


# Escoge el filtro PyCUDA solicitado por el experimento (devuelve TiemposGPU en ms).
def ejecutar_filtro_gpu(filtro, entrada, salida, d_entrada, d_salida, d_mascara,
                        ancho, alto, k, hilos):
    if filtro == Filtro.MEDIA:
        return media_gpu(entrada, salida, d_entrada, d_salida, d_mascara, ancho, alto, k, hilos)
    if filtro == Filtro.NITIDEZ:
        return nitidez_gpu(entrada, salida, d_entrada, d_salida, d_mascara, ancho, alto, k, hilos)
    return laplaciano_gpu(entrada, salida, d_entrada, d_salida, d_mascara, ancho, alto, k, hilos)
