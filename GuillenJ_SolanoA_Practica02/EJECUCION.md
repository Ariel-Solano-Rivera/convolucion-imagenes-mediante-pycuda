# Ejecución de la práctica 02

Todos los comandos se ejecutan desde la carpeta `GuillenJ_SolanoA_Practica02/`.

## Requisitos

- Windows 10/11 x64 con GPU NVIDIA (probado con RTX 3070, compute capability 8.6 → `sm_86`).
- CUDA Toolkit 12.9 (`nvcc` en el PATH y variable `CUDA_PATH` definida por el instalador).
- Visual Studio 2022 con "Desarrollo para el escritorio con C++" (provee `cl.exe`).
- Python 3.12 (se invoca con `py -3.12`; no se usa el Python por defecto del sistema).

## Preparar el entorno

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
cmd /c "call scripts\entorno_vs.bat && .venv\Scripts\python.exe -m pip install -r requirements.txt"
```

### Qué hizo falta para instalar PyCUDA en Windows

1. **PyCUDA no publica wheel para Windows** (`pip download pycuda --only-binary=:all:` no encuentra
   ninguna), así que `pip` lo compila desde el código fuente. Eso requiere `cl.exe` en el PATH.
2. `scripts\entorno_vs.bat` localiza `vcvars64.bat` con `vswhere.exe` (si no lo encuentra usa la
   misma ruta que `compilar.bat` de P01) y lo carga. También agrega la carpeta de `vswhere.exe` al
   PATH, porque `vcvars64.bat` la busca ahí y si no muestra un error.
3. Con el entorno de Visual Studio cargado, setuptools igual responde
   `error: Unable to find a compatible Visual Studio installation`. Se resuelve con
   `DISTUTILS_USE_SDK=1` y `MSSdk=1`, que le indican usar el compilador ya activo;
   `entorno_vs.bat` define ambas variables.
4. Con eso, `pycuda==2026.1` se compila para CPython 3.12 contra CUDA 12.9 (`CUDA_PATH`).

`cl.exe` también hace falta **al ejecutar**: `SourceModule` llama a `nvcc`, y `nvcc` usa `cl.exe`
como compilador anfitrión. Por eso las pruebas y el programa se lanzan siempre después de
`scripts\entorno_vs.bat`.

## Ejecutar

```powershell
.\ejecutar_todo.bat
```

Por pasos (dentro de una consola donde ya se ejecutó `call scripts\entorno_vs.bat`):

```powershell
.venv\Scripts\python.exe -m scripts.registrar_entorno   # resultados/mediciones/entorno.json
.venv\Scripts\python.exe -m pytest                      # pruebas
```
