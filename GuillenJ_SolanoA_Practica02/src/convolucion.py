"""Convolucion comun para CPU y GPU, medicion de tiempos y comparacion (equivale a filtros.cu)."""
import time
from typing import NamedTuple

import numpy as np
import pycuda.driver as cuda

from src.configuracion import Filtro
from src.contexto_cuda import kernel_convolucion
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


class TiemposGPU(NamedTuple):
    h2d: float     # CPU -> GPU (imagen y mascara), ms
    kernel: float  # ejecucion del kernel, ms
    d2h: float     # GPU -> CPU (salida), ms
    total: float   # e0 -> e3, ms


def verificar_arreglo(arreglo, nombre):
    """Los arreglos transferidos deben ser float32 y C-contiguos (el kernel lee float*)."""
    if arreglo.dtype != np.float32:
        raise TypeError(f"{nombre} debe ser float32, no {arreglo.dtype}")
    if not arreglo.flags.c_contiguous:
        raise TypeError(f"{nombre} debe ser contiguo (use np.ascontiguousarray)")


def escalares_kernel(ancho, alto, k):
    """ancho, alto y k son int en el kernel: se pasan como np.int32 explicitos."""
    return np.int32(ancho), np.int32(alto), np.int32(k)


def reservar_memoria_gpu(n, k):
    """cudaMalloc de P01: una vez por configuracion, fuera del tiempo medido."""
    bytes_imagen = n * np.dtype(np.float32).itemsize
    bytes_mascara = k * k * np.dtype(np.float32).itemsize
    return cuda.mem_alloc(bytes_imagen), cuda.mem_alloc(bytes_imagen), cuda.mem_alloc(bytes_mascara)


def liberar_memoria_gpu(*punteros):
    for puntero in punteros:
        puntero.free()


# Mide transferencia CPU-GPU, kernel y transferencia GPU-CPU (misma secuencia que ejecutarGPU).
def ejecutar_gpu(entrada, salida, mascara, d_entrada, d_salida, d_mascara,
                 ancho, alto, k, hilos):
    for arreglo, nombre in ((entrada, "entrada"), (salida, "salida"), (mascara, "mascara")):
        verificar_arreglo(arreglo, nombre)
    n = ancho * alto
    bloques = (n + hilos - 1) // hilos  # ceil(n / hilos)
    ancho_k, alto_k, k_k = escalares_kernel(ancho, alto, k)
    kernel = kernel_convolucion()
    e = [cuda.Event() for _ in range(4)]

    e[0].record()
    cuda.memcpy_htod(d_entrada, entrada)
    cuda.memcpy_htod(d_mascara, mascara)
    e[1].record()

    kernel(d_entrada, d_salida, d_mascara, ancho_k, alto_k, k_k,
           block=(hilos, 1, 1), grid=(bloques, 1))
    e[2].record()
    cuda.memcpy_dtoh(salida, d_salida)
    e[3].record()
    e[3].synchronize()

    return TiemposGPU(h2d=e[0].time_till(e[1]), kernel=e[1].time_till(e[2]),
                      d2h=e[2].time_till(e[3]), total=e[0].time_till(e[3]))


# Calcula una vez en GPU, con su propia reserva (calcularAmbas de P01, parte GPU).
def calcular_gpu(entrada, mascara, ancho, alto, k, hilos, salida_inicial=None):
    n = ancho * alto
    salida = np.empty(n, dtype=np.float32)
    d_entrada, d_salida, d_mascara = reservar_memoria_gpu(n, k)
    try:
        if salida_inicial is not None:  # p. ej. NaN para comprobar cobertura
            cuda.memcpy_htod(d_salida, salida_inicial)
        ejecutar_gpu(entrada, salida, mascara, d_entrada, d_salida, d_mascara,
                     ancho, alto, k, hilos)
    finally:
        liberar_memoria_gpu(d_entrada, d_salida, d_mascara)
    return salida


# Obtiene el error maximo y el error medio respecto de la referencia (como compararCPUyGPU).
def comparar(referencia, otra):
    # La resta y el valor absoluto en float32, como fabs(cpu[i] - gpu[i]) en P01;
    # el promedio se acumula en float64 (double en P01).
    error = np.abs(referencia.astype(np.float32, copy=False) - otra.astype(np.float32, copy=False))
    return float(error.max()), float(error.mean(dtype=np.float64))
