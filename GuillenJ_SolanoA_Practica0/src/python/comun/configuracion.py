"""Parametros generales de las mediciones, filtros y rutas."""
from enum import IntEnum
from pathlib import Path


REPETICIONES = 10
SEGUNDOS_CALENTAMIENTO_GPU = 2.0


TOLERANCIA = 1e-2

REPETICIONES_PYTHON = 5


LIMITE_PYTHON_SEGUNDOS = 120
HILOS_POR_DEFECTO = 256
HILOS_EXPERIMENTO = (128, 256, 512)


class Filtro(IntEnum):
    MEDIA = 0
    NITIDEZ = 1
    LAPLACIANO = 2


NOMBRE_FILTRO = {Filtro.MEDIA: "media", Filtro.NITIDEZ: "nitidez",
                 Filtro.LAPLACIANO: "laplaciano"}


ARQUITECTURA = "sm_86"
OPCIONES_NVCC = ["-O3"]


RAIZ = Path(__file__).resolve().parents[3]
RAIZ_REPO = RAIZ.parent
P01 = RAIZ  
DATOS = RAIZ / "datos"
RESULTADOS = RAIZ / "resultados"
MEDICIONES = RESULTADOS / "mediciones"
PRUEBAS = RESULTADOS / "pruebas"
IMAGENES = RESULTADOS / "imagenes"
REFERENCIAS = RESULTADOS / "referencias"
KERNEL = RAIZ / "src" / "pycuda" / "kernels" / "convolucion.cu"


IMAGENES_P01 = {
    2000: DATOS / "base_2000.pgm",
    4000: DATOS / "base_4000.pgm",
    6000: DATOS / "base_6000.pgm",
}
NO_MULTIPLO = DATOS / "no_multiplo_1013x757.pgm"
HASHES_P01 = DATOS / "hashes_p01.json"


REFERENCIA_EXE = RAIZ / "src" / "cuda_c" / "referencia.exe"
VERSIONES = ("cpp_secuencial", "cuda_c", "python_secuencial", "pycuda")



EXPERIMENTOS = {
    "filtros": [(Filtro.MEDIA, 3, 4000, 256), (Filtro.NITIDEZ, 3, 4000, 256),
                (Filtro.LAPLACIANO, 3, 4000, 256)],
    "resolucion": [(Filtro.MEDIA, 9, 2000, 256), (Filtro.MEDIA, 9, 4000, 256),
                   (Filtro.MEDIA, 9, 6000, 256)],
    "mascara": [(Filtro.MEDIA, 3, 4000, 256), (Filtro.MEDIA, 9, 4000, 256),
                (Filtro.MEDIA, 21, 4000, 256)],
    "hilos": [(Filtro.MEDIA, 9, 4000, h) for h in HILOS_EXPERIMENTO],  
}

CONFIGURACIONES_NO_MULTIPLO = [(Filtro.MEDIA, 3), (Filtro.NITIDEZ, 3),
                               (Filtro.LAPLACIANO, 3), (Filtro.MEDIA, 9)]

CONFIGURACIONES_PEQUENAS = [(Filtro.MEDIA, 3), (Filtro.NITIDEZ, 3), (Filtro.LAPLACIANO, 3),
                            (Filtro.MEDIA, 9), (Filtro.MEDIA, 21)]
RESOLUCIONES_VALIDACION_PYTHON = (250,)


def ruta_imagen(resolucion):
    """Imagenes de P01 desde su carpeta; las nuevas desde datos/ de P02."""
    return IMAGENES_P01.get(resolucion, DATOS / f"base_{resolucion}.pgm")


def configuraciones_unicas():
    """(filtro, k, resolucion, hilos) sin repetir, en orden de aparicion."""
    vistas = []
    for configuraciones in EXPERIMENTOS.values():
        for configuracion in configuraciones:
            if configuracion not in vistas:
                vistas.append(configuracion)
    return vistas
