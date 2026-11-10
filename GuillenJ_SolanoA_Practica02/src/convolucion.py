"""Convolucion comun para CPU y GPU, medicion de tiempos y comparacion (equivale a filtros.cu)."""
import time

import numpy as np

from src.configuracion import Filtro
from src.filtros.mascaras import (crear_mascara_laplaciano, crear_mascara_media,
                                  crear_mascara_nitidez)


class TiempoExcedido(Exception):
    """La convolucion secuencial supero su limite de tiempo y se aborto."""

    def __init__(self, transcurrido, filas_procesadas, limite):
        self.transcurrido = transcurrido          # segundos reales medidos
        self.filas_procesadas = filas_procesadas  # filas y completas
        self.limite = limite
        super().__init__(f"limite de {limite:.0f} s excedido tras {transcurrido:.1f} s "
                         f"({filas_procesadas} filas procesadas)")


# Escoge los coeficientes del filtro solicitado.
def crear_mascara(filtro, k):
    if filtro == Filtro.MEDIA:
        return crear_mascara_media(k)
    return crear_mascara_nitidez() if filtro == Filtro.NITIDEZ else crear_mascara_laplaciano()


# Version secuencial: recorre todos los pixeles y sus vecinos (port literal de convolucionCPU).
def convolucion_cpu(entrada, salida, mascara, ancho, alto, k, limite_segundos=None):
    radio = k // 2
    # Listas de escalares np.float32: solo almacenan los datos (indexar una lista es mas
    # rapido que indexar un ndarray). Toda la aritmetica sigue siendo float32.
    datos = list(entrada)
    coeficientes = list(mascara)
    cero = np.float32(0)
    inicio = time.perf_counter()
    for y in range(alto):
        # El reloj se consulta una vez por fila para poder abortar.
        if limite_segundos is not None:
            transcurrido = time.perf_counter() - inicio
            if transcurrido > limite_segundos:
                raise TiempoExcedido(transcurrido, y, limite_segundos)
        for x in range(ancho):
            suma = cero
            for j in range(-radio, radio + 1):
                for i in range(-radio, radio + 1):
                    yy = y + j
                    xx = x + i
                    if yy >= 0 and yy < alto and xx >= 0 and xx < ancho:
                        # float32 * float32 -> float32; float32 + float32 -> float32
                        suma += datos[yy * ancho + xx] * coeficientes[(j + radio) * k + i + radio]
            salida[y * ancho + x] = suma


# Mide solamente la convolucion secuencial (ms, como P01).
def ejecutar_cpu(entrada, salida, mascara, ancho, alto, k, limite_segundos=None):
    inicio = time.perf_counter()
    convolucion_cpu(entrada, salida, mascara, ancho, alto, k, limite_segundos)
    return (time.perf_counter() - inicio) * 1000.0


# Obtiene el error maximo y el error medio respecto de la referencia (como compararCPUyGPU).
def comparar(referencia, otra):
    # La resta y el valor absoluto en float32, como fabs(cpu[i] - gpu[i]) en P01;
    # el promedio se acumula en float64 (double en P01).
    error = np.abs(referencia.astype(np.float32, copy=False) - otra.astype(np.float32, copy=False))
    return float(error.max()), float(error.mean(dtype=np.float64))
