@echo off
REM Compila referencia.exe enlazando las fuentes de P01 por ruta relativa (sin copiarlas
REM ni modificarlas), con los mismos flags que compilar.bat de P01: -O3 -arch=sm_86.
REM No incluye experimentos.cu ni main.cu de P01 (traen su propio main y rutas fijas).
cd /d "%~dp0"
call ..\scripts\entorno_vs.bat || exit /b 1
set "P01=..\..\GuillenJ_SolanoA_Practica0\src"
nvcc -O3 -arch=sm_86 -I%P01% -o referencia.exe referencia.cu %P01%\imagenes.cpp %P01%\filtros.cu %P01%\filtros\media.cpp %P01%\filtros\nitidez.cpp %P01%\filtros\laplaciano.cpp %P01%\secuencial\media.cpp %P01%\secuencial\nitidez.cpp %P01%\secuencial\laplaciano.cpp %P01%\paralelo\media.cu %P01%\paralelo\nitidez.cu %P01%\paralelo\laplaciano.cu || exit /b 1
del /q referencia.exp referencia.lib 2>nul
exit /b 0
