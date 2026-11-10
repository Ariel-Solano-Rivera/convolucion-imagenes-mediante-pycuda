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

# Imagenes de P01: se leen desde su carpeta, sin duplicarlas ni regenerarlas.
IMAGENES_P01 = {
    2000: DATOS_P01 / "base_2000.pgm",
    4000: DATOS_P01 / "base_4000.pgm",
    6000: DATOS_P01 / "base_6000.pgm",
}
NO_MULTIPLO = DATOS_P01 / "no_multiplo_1013x757.pgm"
HASHES_P01 = DATOS / "hashes_p01.json"
IMAGEN_ORIGEN_P01 = P01 / "imagenes" / "ImagenGrande.jpg"
# Imagenes nuevas de P02 (piloto de Python secuencial), en DATOS.
RESOLUCIONES_NUEVAS = (250, 500)
