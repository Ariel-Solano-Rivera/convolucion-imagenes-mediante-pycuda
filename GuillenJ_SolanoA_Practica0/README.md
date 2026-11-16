# Convolución de imágenes de alta resolución con Python y PyCUDA

Práctica 02 de Computación Paralela de la Universidad Politécnica Salesiana.

**Integrantes:** Juan Alberto Guillén y Ariel Solano

**Implementaciones comparadas:** C++ secuencial, CUDA C, Python secuencial y PyCUDA

## Resumen

El proyecto migra a Python el programa anfitrión desarrollado en la práctica 01 y ejecuta mediante PyCUDA el mismo kernel de convolución escrito en CUDA C. Las cuatro implementaciones procesan las mismas imágenes, utilizan precisión `float32`, aplican extensión con ceros en los bordes y almacenan la entrada y la salida en arreglos diferentes.

La práctica estudia tres filtros:

| Filtro | Configuración | Propósito |
|---|---|---|
| Media | Máscaras 3×3, 9×9 y 21×21 con coeficientes `1/(k×k)` | Suavizar la imagen |
| Nitidez | Máscara 3×3 `[0,-1,0; -1,5,-1; 0,-1,0]` | Realzar detalles y contornos |
| Laplaciano | Máscara 3×3 `[0,1,0; 1,-4,1; 0,1,0]` | Detectar bordes |

Las mediciones comparan el efecto del filtro, la resolución, el tamaño de la máscara y la cantidad de hilos por bloque. Los resultados se guardan en CSV y se presentan mediante tablas, gráficas e imágenes.

## Resultados principales

Los valores siguientes corresponden al equipo utilizado en la práctica: Intel Core i9-12900K y NVIDIA GeForce RTX 3070.

- Python secuencial coincide bit a bit con C++ secuencial.
- PyCUDA coincide bit a bit con CUDA C porque ambas versiones ejecutan el mismo kernel.
- El mayor error observado entre CPU y GPU fue `1,678e-04`, dentro de la tolerancia calculada para `float32`.
- El kernel ejecutado desde PyCUDA presentó entre 0 % y 4,9 % de diferencia respecto a CUDA C.
- Python secuencial fue aproximadamente entre 210 y 280 veces más lento que C++ con el mismo algoritmo.
- Las transferencias CPU-GPU representaron entre 58 % y 98 % del tiempo total de GPU.
- Las configuraciones de 128, 256 y 512 hilos por bloque mostraron diferencias pequeñas en el equipo evaluado.

Estos resultados no deben generalizarse a otras CPU, GPU o versiones de software sin repetir las mediciones.

## Implementaciones

| Versión | Procesador | Programa anfitrión | Ubicación |
|---|---|---|---|
| C++ secuencial | CPU, un núcleo | C++ | `src/secuencial_c/` y `src/filtros.cu` |
| CUDA C | GPU, un hilo por píxel | C++ | `src/cuda_c/` y `src/filtros.cu` |
| Python secuencial | CPU, un núcleo | Python | `src/python/` |
| PyCUDA | GPU, un hilo por píxel | Python | `src/pycuda/` |

La versión secuencial en Python utiliza recorridos explícitos de filas, columnas y coeficientes. NumPy se usa para almacenar datos, mantener la precisión `float32` y calcular los errores, pero no sustituye la convolución con funciones ya implementadas.

PyCUDA compila el kernel de `src/pycuda/kernels/convolucion.cu` mediante `SourceModule`. La reserva de memoria, las transferencias, los tipos de los argumentos, el bloque y la cuadrícula se configuran explícitamente desde Python.

## Validación

La referencia numérica es C++ secuencial. La validación incluye:

1. Una matriz 5×5 con valores calculados manualmente.
2. Una imagen de 1013×757 píxeles, cuyo número de píxeles no es múltiplo de 128, 256 ni 512.
3. Comparación del error absoluto máximo y medio antes del recorte visual.
4. Comprobación de tipos `float32`, escalares `int32` y arreglos contiguos.
5. Comparación de las imágenes producidas por las cuatro implementaciones.

## Experimentos

Cada experimento modifica un solo factor y mantiene los demás constantes.

| Experimento | Configuración | Versiones |
|---|---|---|
| Filtro | Media, nitidez y laplaciano 3×3 sobre 4000×4000 | Las cuatro |
| Resolución | Media 9×9 sobre 2000², 4000² y 6000² | Las cuatro |
| Máscara | Media 3×3, 9×9 y 21×21 sobre 4000×4000 | Las cuatro |
| Hilos por bloque | Media 9×9 sobre 4000×4000 con 128, 256 y 512 hilos | CUDA C y PyCUDA |

Las versiones de GPU realizan 2 segundos de calentamiento y 10 repeticiones por configuración. Los eventos CUDA separan la transferencia CPU-GPU, el kernel, la transferencia GPU-CPU y el tiempo total. Python secuencial realiza cinco repeticiones cuando la configuración termina dentro del límite establecido.

Las ejecuciones de Python que superan 120 segundos se registran como interrumpidas junto con el tiempo transcurrido y las filas procesadas. Esas ejecuciones no se utilizan para calcular aceleraciones.

## Requisitos

- Windows 10 u 11 de 64 bits.
- GPU NVIDIA compatible con CUDA.
- Controlador NVIDIA actualizado.
- CUDA Toolkit 12.9 con `nvcc` disponible.
- Visual Studio 2022 con la carga de trabajo **Desarrollo para el escritorio con C++**.
- Python 3.12 de 64 bits.
- Microsoft Word y PowerPoint únicamente para exportar el informe y la presentación a PDF.

El proyecto está configurado para `sm_86`, arquitectura de la RTX 3070 utilizada. Para otra GPU se debe actualizar `-arch=sm_86` en `compilar.bat` y `scripts/compilar_referencia.bat`, además de `ARQUITECTURA` en `src/python/comun/configuracion.py`.

## Instalación

Abra PowerShell en la carpeta `GuillenJ_SolanoA_Practica0` y ejecute:

```powershell
py -3.12 -m venv .venv
cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m pip install -r requirements.txt"
```

Para generar también el informe y la presentación:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-documentos.txt
```

## Ejecución completa

El orden recomendado para reproducir toda la práctica es:

```powershell
.\ejecutar_cuda.bat
.\ejecutar_pycuda.bat
.\generar_documentos.bat
```

### C++ secuencial y CUDA C

```powershell
.\ejecutar_cuda.bat
```

Este comando prepara las imágenes, compila el programa con `nvcc`, ejecuta las pruebas y realiza los experimentos de C++ secuencial y CUDA C.

Archivos principales generados:

- `resultados/mediciones/mediciones.csv`
- `resultados/pruebas/prueba_manual.csv`
- `resultados/pruebas/validacion.csv`
- `resultados/imagenes/*.pgm`

### Python secuencial y PyCUDA

```powershell
.\ejecutar_pycuda.bat
```

El comando comprueba los hashes de las imágenes, genera referencias C++/CUDA C, registra el entorno, ejecuta `pytest`, valida las cuatro versiones, mide Python y PyCUDA y actualiza las gráficas.

Archivos principales generados:

- `resultados/mediciones/mediciones_python_pycuda.csv`
- `resultados/mediciones/inicializacion.csv`
- `resultados/mediciones/entorno.json`
- `resultados/pruebas/prueba_manual_python_pycuda.csv`
- `resultados/pruebas/validacion_python_pycuda.csv`
- `resultados/pruebas/evidencia_visual.csv`

La ejecución completa puede tardar aproximadamente 25 minutos debido a los bucles explícitos de Python secuencial.

Para repetir únicamente las mediciones de PyCUDA y conservar las filas existentes de Python:

```powershell
cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m scripts.medir_python_pycuda --solo-pycuda"
```

### Experimentos paralelos con otra imagen

```powershell
.\ejecutar_paralelo.bat
.\ejecutar_paralelo.bat C:\ruta\imagen.jpg
.\ejecutar_paralelo.bat imagen1.jpg imagen2.png
.\ejecutar_paralelo.bat imagen.jpg --resoluciones 1000,2000,3000
```

Sin argumentos se utilizan las imágenes de `datos/`. Al proporcionar una imagen JPG, PNG o PGM, el programa la convierte a escala de grises, toma el recorte cuadrado central y genera las resoluciones necesarias.

Los resultados se guardan en `resultados/paralelo/<nombre_imagen>/` e incluyen mediciones, resumen estadístico, validación, gráficas e imágenes de CUDA C y PyCUDA.

### Pruebas

Pruebas que no ejecutan kernels en la GPU:

```powershell
.venv\Scripts\python.exe -m pytest -m "not gpu"
```

Todas las pruebas, incluidas las de PyCUDA:

```powershell
cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m pytest"
```

### Informe y presentación

```powershell
.\generar_documentos.bat
```

El comando lee los CSV de `resultados/` y genera:

- `../docs/informe/informe_practica02.docx`
- `../docs/informe/informe_practica02.pdf`
- `../docs/presentacion/presentacion_practica02.pptx`
- `../docs/presentacion/presentacion_practica02.pdf`

## Estructura del proyecto

```text
GuillenJ_SolanoA_Practica0/
├── datos/                     Imágenes de entrada y hashes SHA-256
├── imagenes/                  Imagen original
├── resultados/
│   ├── graficas/              Gráficas comparativas
│   ├── imagenes/              Evidencia visual
│   ├── mediciones/            CSV de tiempos y descripción del entorno
│   ├── pruebas/               Validación manual y numérica
│   └── paralelo/              Experimentos CUDA C y PyCUDA por imagen
├── scripts/                   Preparación, medición y generación de documentos
├── src/
│   ├── cuda_c/                Implementación y referencia CUDA C
│   ├── filtros/               Máscaras en C++
│   ├── pycuda/                Contexto, lanzamiento y kernel usado por PyCUDA
│   ├── python/                Implementación secuencial en Python
│   └── secuencial_c/          Implementación secuencial en C++
├── tests/                     Pruebas de pytest
├── compilar.bat
├── ejecutar_cuda.bat
├── ejecutar_paralelo.bat
├── ejecutar_pycuda.bat
├── generar_documentos.bat
├── main.cu
├── main.py
└── requirements.txt
```

## Archivos de resultados

| Ruta | Contenido |
|---|---|
| `resultados/mediciones/mediciones.csv` | Repeticiones de C++ secuencial y CUDA C |
| `resultados/mediciones/mediciones_python_pycuda.csv` | Repeticiones de Python secuencial y PyCUDA |
| `resultados/mediciones/inicializacion.csv` | Creación del contexto y compilación o carga del kernel |
| `resultados/mediciones/entorno.json` | CPU, RAM, GPU, sistema operativo y versiones |
| `resultados/pruebas/` | Prueba manual, prueba de límites y errores numéricos |
| `resultados/graficas/` | Gráficas utilizadas en el informe |
| `resultados/imagenes/` | Original y salidas de los filtros |

## Trazabilidad

- **Repositorio de la práctica 02:** añadir la URL del nuevo repositorio antes de entregar.
- **Commit evaluado de la práctica 02:** añadir el hash final después de subir el código y los CSV.
- **Práctica 01:** etiqueta `practica01-entrega`, commit `08b155eab3bbc991cc9a20f9e633f25b41ac223f`.
- Los archivos de entrada se verifican mediante los hashes almacenados en `datos/hashes_p01.json`.
- `resultados/mediciones/entorno.json` registra el entorno y el estado del repositorio usado durante las mediciones.
- `resultados/mediciones/corrida_descartada_2026-11-13/` conserva una corrida reemplazada por falta de calentamiento suficiente de la GPU.

## Documentación

- Informe: `../docs/informe/informe_practica02.pdf`
- Presentación: `../docs/presentacion/presentacion_practica02.pdf`
