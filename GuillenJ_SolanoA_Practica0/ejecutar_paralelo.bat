@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    echo Falta .venv. Revise el README.
    exit /b 1
)
set "PY=.venv\Scripts\python.exe"

echo [1/3] Preparando Visual Studio (cl.exe para nvcc)...
call scripts\entorno_vs.bat || exit /b 1

echo [2/3] Compilando CUDA C (src\cuda_c\referencia.exe)...
call scripts\compilar_referencia.bat || exit /b 1

echo [3/3] Ejecutando los 4 experimentos con CUDA C y PyCUDA...
%PY% -m scripts.ejecutar_paralelo %* || exit /b 1
echo.
echo Listo. Revise resultados\paralelo\
