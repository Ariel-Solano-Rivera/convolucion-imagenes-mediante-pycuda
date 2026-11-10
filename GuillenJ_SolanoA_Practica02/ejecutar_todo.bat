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

echo [2] Ejecutando pruebas...
%PY% -m pytest || exit /b 1

echo.
echo Listo. Revise la carpeta resultados.
