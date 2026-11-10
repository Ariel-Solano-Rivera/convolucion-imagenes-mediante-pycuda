@echo off
REM Flujo completo de P02: entorno, pruebas, validacion, mediciones y graficas.
REM Uso: ejecutar_todo.bat   (siempre trabaja dentro de GuillenJ_SolanoA_Practica02)
cd /d "%~dp0"
call scripts\entorno_vs.bat || exit /b 1
if not exist .venv\Scripts\python.exe (
    echo Falta el entorno virtual .venv. Vea EJECUCION.md.
    exit /b 1
)
set "PY=.venv\Scripts\python.exe"

echo [1] Registrando el entorno...
%PY% -m scripts.registrar_entorno || exit /b 1

echo [2] Verificando datos de P01 y generando imagenes nuevas...
%PY% -m scripts.preparar_imagenes || exit /b 1

echo [3] Compilando la referencia C++/CUDA C (fuentes de P01 sin modificar)...
call referencia_cpp\compilar_referencia.bat || exit /b 1

echo [4] Exportando salidas float32 de C++ y CUDA C...
%PY% -m scripts.generar_referencias || exit /b 1

echo [5] Ejecutando pruebas...
%PY% -m pytest || exit /b 1

echo [6] Prueba manual, prueba de no multiplo y validacion de las cuatro versiones...
%PY% main.py validar || exit /b 1

echo.
echo Listo. Revise la carpeta resultados.
