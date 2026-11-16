# Convolución de imágenes mediante CUDA - PyCUDA

Implementación y evaluación de filtros de convolución sobre imágenes de alta resolución en cuatro versiones: C++ secuencial, CUDA C, Python secuencial y PyCUDA.

Proyecto desarrollado por **Juan Alberto Guillén** y **Ariel Solano** para la asignatura Computación Paralela de la Universidad Politécnica Salesiana.

## Resumen

La práctica migra a Python el programa anfitrión de una implementación previa en C++/CUDA C. PyCUDA compila y ejecuta el mismo kernel CUDA C, mientras Python administra las imágenes, máscaras, memoria, transferencias, validación y mediciones.

Se evalúan los filtros de media, nitidez y laplaciano, variando la resolución, el tamaño de la máscara y los hilos por bloque. Las cuatro versiones se comparan mediante pruebas numéricas, evidencia visual y mediciones repetidas.

## Inicio rápido

Los comandos se ejecutan desde `GuillenJ_SolanoA_Practica0/`.

```powershell
cd GuillenJ_SolanoA_Practica0
py -3.12 -m venv .venv
cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m pip install -r requirements.txt"
.\ejecutar_cuda.bat
.\ejecutar_pycuda.bat
```


## Comandos principales

| Comando | Función |
|---|---|
| `.\ejecutar_cuda.bat` | Compila y ejecuta C++ secuencial y CUDA C |
| `.\ejecutar_pycuda.bat` | Ejecuta pruebas, validación y mediciones de Python y PyCUDA |
| `.\ejecutar_paralelo.bat [imagen]` | Ejecuta los cuatro experimentos paralelos con las imágenes de la práctica o una imagen propia |
| `.\generar_documentos.bat` | Genera el informe y la presentación a partir de los CSV |
| `.venv\Scripts\python.exe -m pytest -m "not gpu"` | Ejecuta las pruebas que no lanzan kernels GPU |
| `cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m pytest"` | Ejecuta todas las pruebas |

