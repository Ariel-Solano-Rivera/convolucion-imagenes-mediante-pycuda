"""Pruebas, validacion y experimentos de la practica."""
import numpy as np

from src.configuracion import Filtro

# Prueba manual: matriz 5x5 y mascara de la figura 1 de la guia (pruebaManual de P01).
IMAGEN_MANUAL = np.array([35, 40, 41, 45, 50,
                          40, 40, 42, 46, 52,
                          42, 46, 50, 55, 55,
                          48, 52, 56, 58, 60,
                          56, 60, 65, 70, 75], dtype=np.float32)
MASCARA_FIGURA1 = np.array([-2, -1, 0, -1, 1, 1, 0, 1, 2], dtype=np.float32)
NOMBRES_MANUALES = ("figura1", "media", "nitidez", "laplaciano")
# (indice de mascara, fila, columna, esperado). Los cocientes se hacen en float32 como 155.f / 9.
CASOS_MANUALES = (
    (0, 1, 1, np.float32(78)), (0, 1, 2, np.float32(87)),
    (1, 0, 0, np.float32(155) / np.float32(9)), (1, 2, 2, np.float32(445) / np.float32(9)),
    (1, 4, 4, np.float32(263) / np.float32(9)), (2, 0, 0, np.float32(95)),
    (2, 1, 1, np.float32(32)), (2, 2, 2, np.float32(51)),
    (3, 0, 0, np.float32(-60)), (3, 1, 1, np.float32(8)),
    (3, 2, 2, np.float32(-1)), (3, 4, 4, np.float32(-170)),
)
TOLERANCIA_MANUAL = 1e-3  # la misma de pruebaManual en P01


def mascaras_manuales():
    """Las cuatro mascaras de la prueba manual, en el orden de NOMBRES_MANUALES."""
    from src.convolucion import crear_mascara
    return (MASCARA_FIGURA1, crear_mascara(Filtro.MEDIA, 3),
            crear_mascara(Filtro.NITIDEZ, 3), crear_mascara(Filtro.LAPLACIANO, 3))
