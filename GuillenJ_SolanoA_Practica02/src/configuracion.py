"""Parametros generales de las mediciones, filtros y rutas."""
from enum import IntEnum
from pathlib import Path

# Mismos valores que configuracion.h de P01.
REPETICIONES = 10
SEGUNDOS_CALENTAMIENTO_GPU = 2.0
TOLERANCIA = 1e-2
# Python secuencial: minimo de la guia (P01 no tenia esta version).
REPETICIONES_PYTHON = 5
HILOS_POR_DEFECTO = 256
HILOS_EXPERIMENTO = (128, 256, 512)


class Filtro(IntEnum):
    MEDIA = 0
    NITIDEZ = 1
    LAPLACIANO = 2


NOMBRE_FILTRO = {Filtro.MEDIA: "media", Filtro.NITIDEZ: "nitidez",
                 Filtro.LAPLACIANO: "laplaciano"}

# Compilacion del kernel: mismos flags que compilar.bat de P01, sin --use_fast_math.
ARQUITECTURA = "sm_86"
OPCIONES_NVCC = ["-O3"]

# Rutas relativas a la carpeta de P02 (nunca absolutas).
RAIZ = Path(__file__).resolve().parent.parent
RAIZ_REPO = RAIZ.parent
P01 = RAIZ_REPO / "GuillenJ_SolanoA_Practica0"
DATOS_P01 = P01 / "datos"
DATOS = RAIZ / "datos"
RESULTADOS = RAIZ / "resultados"
MEDICIONES = RESULTADOS / "mediciones"
PRUEBAS = RESULTADOS / "pruebas"
IMAGENES = RESULTADOS / "imagenes"
GRAFICAS = RESULTADOS / "graficas"
REFERENCIAS = RESULTADOS / "referencias"
KERNEL = RAIZ / "src" / "kernels" / "convolucion.cu"
