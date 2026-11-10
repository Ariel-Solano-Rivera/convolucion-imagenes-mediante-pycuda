"""Piloto de viabilidad de Python secuencial en imagenes pequenas.

Mide convolucion_cpu (media 3x3, 9x9 y 21x21; 3 repeticiones) en 250x250 y 500x500 y
escribe:
  resultados/mediciones/piloto_python.csv      tiempos MEDIDOS del piloto
  resultados/mediciones/piloto_planificacion.md ESTIMACION PARA PLANIFICAR (no es resultado)
"""
import csv
from statistics import median

import numpy as np

from src.configuracion import MEDICIONES, Filtro, ruta_imagen
from src.convolucion import crear_mascara, ejecutar_cpu
from src.imagenes import leer_pgm

RESOLUCIONES_PILOTO = (250, 500)
MASCARAS_PILOTO = (3, 9, 21)
REPETICIONES_PILOTO = 3
# Para planificar: resoluciones de los experimentos y candidatas a "resolucion menor comun".
RESOLUCIONES_PLAN = (750, 1000, 1500, 2000, 4000, 6000)
# Configuraciones que Python secuencial debe intentar (las 4 versiones), por resolucion.
CONFIG_EXPERIMENTOS = [(4000, 3), (4000, 3), (4000, 3), (4000, 9), (4000, 21),
                       (2000, 9), (6000, 9)]  # media/nitidez/laplaciano 3 cuestan igual
CONFIG_MENOR_COMUN = [3, 3, 3, 9, 21]          # los mismos filtros/mascaras en N x N


def medir():
    filas = []
    for resolucion in RESOLUCIONES_PILOTO:
        entrada, ancho, alto = leer_pgm(ruta_imagen(resolucion))
        salida = np.zeros_like(entrada)
        for k in MASCARAS_PILOTO:
            mascara = crear_mascara(Filtro.MEDIA, k)
            for r in range(1, REPETICIONES_PILOTO + 1):
                t = ejecutar_cpu(entrada, salida, mascara, ancho, alto, k)
                filas.append({"version": "python_secuencial", "filtro": "media", "mascara": k,
                              "ancho": ancho, "alto": alto, "repeticion": r,
                              "t_total": f"{t:.4f}", "unidad": "ms"})
                print(f"media{k} {ancho}x{alto} rep {r}: {t / 1000:.2f} s", flush=True)
    MEDICIONES.mkdir(parents=True, exist_ok=True)
    with open(MEDICIONES / "piloto_python.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)
    return filas


def costo_por_iteracion(filas):
    """ns por (pixel x coeficiente), con la mediana de cada configuracion del piloto."""
    costos = {}
    for k in MASCARAS_PILOTO:
        for resolucion in RESOLUCIONES_PILOTO:
            tiempos = [float(f["t_total"]) for f in filas
                       if f["mascara"] == k and f["ancho"] == resolucion]
            costos[(resolucion, k)] = median(tiempos) * 1e6 / (resolucion ** 2 * k * k)
    return costos


def planificar(filas):
    costos = costo_por_iteracion(filas)
    # Se usa el costo medido en 500x500 (menos efecto de bordes que 250x250).
    costo = {k: costos[(500, k)] for k in MASCARAS_PILOTO}

    def estimar_s(resolucion, k):
        return costo[k] * resolucion ** 2 * k * k / 1e9

    lineas = ["# Piloto de Python secuencial — ESTIMACIÓN PARA PLANIFICAR, NO ES RESULTADO", "",
              "Los tiempos de esta tabla **no son mediciones**: se extrapolan del piloto con",
              "costo ∝ píxeles × k × k. No se usan en el informe como tiempos medidos.", "",
              "## Costo medido en el piloto (ns por píxel × coeficiente, mediana)", "",
              "| k | 250×250 | 500×500 |", "|---|---|---|"]
    for k in MASCARAS_PILOTO:
        lineas.append(f"| {k} | {costos[(250, k)]:.1f} | {costos[(500, k)]:.1f} |")
    lineas += ["", "## Estimación de UNA corrida (minutos) — no es resultado", "",
               "| resolución | " + " | ".join(f"media {k}×{k}" for k in MASCARAS_PILOTO) + " |",
               "|---|" + "---|" * len(MASCARAS_PILOTO)]
    for resolucion in RESOLUCIONES_PLAN:
        celdas = " | ".join(f"{estimar_s(resolucion, k) / 60:.1f}" for k in MASCARAS_PILOTO)
        lineas.append(f"| {resolucion}×{resolucion} | {celdas} |")

    lineas += ["", "## Estimación del plan completo (horas) — no es resultado", "",
               "Cada configuración viable = 1 calentamiento + 5 repeticiones = 6 corridas.", ""]
    total_experimentos = sum(6 * estimar_s(r, k) for r, k in CONFIG_EXPERIMENTOS) / 3600
    lineas.append(f"- Experimentos a 2000/4000/6000 si todo se completara: "
                  f"{total_experimentos:.1f} h")
    for n in (750, 1000, 1500):
        total = sum(6 * estimar_s(n, k) for k in CONFIG_MENOR_COMUN) / 3600
        lineas.append(f"- Resolución menor común {n}×{n} (5 configuraciones × 6 corridas): "
                      f"{total:.2f} h")
    (MEDICIONES / "piloto_planificacion.md").write_text("\n".join(lineas) + "\n",
                                                         encoding="utf-8")
    print("\n".join(lineas))


if __name__ == "__main__":
    planificar(medir())
