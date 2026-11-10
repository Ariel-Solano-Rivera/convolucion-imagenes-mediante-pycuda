# Plan — Práctica 02 · Convolución de imágenes con PyCUDA

## Contexto

P01 (CUDA C/C++, tag `practica01-entrega` = `08b155e…`) ya está entregada. P02 migra a Python el programa anfitrión, ejecuta **el mismo kernel `convolucionGPU`** desde PyCUDA, agrega una versión Python secuencial con bucles explícitos y compara las 4 versiones (`cpp_secuencial`, `cuda_c`, `python_secuencial`, `pycuda`). Todo lo nuevo va en `GuillenJ_SolanoA_Practica02/`; P01 no se toca. Entrega: lun 16-nov-2026 14:00.

Entorno comprobado (solo lectura): RTX 3070 8 GB, compute capability **8.6 → sm_86 confirmado**, driver 596.36, nvcc 12.9.86, VS 2022 Community (vswhere disponible), `py -3.12` = 3.12.10, `git diff --stat practica01-entrega -- GuillenJ_SolanoA_Practica0` vacío.

---

## 1. Resumen de lo que exige la guía (PDF)

1. Reutilizar filtros, coeficientes e imágenes de P01 (2000², 4000², 6000²) e identificar el commit de P01.
2. Programa Python: carga, gris, máscaras, arreglos, selección de filtro, ejecución, validación, CSV y guardado.
3. Python secuencial con recorridos explícitos; NumPy solo para datos y errores; sin JIT, filtrado de bibliotecas, multiproceso ni llamadas a C.
4. PyCUDA con el kernel propio de P01 (`SourceModule`), memoria/transferencias explícitas, tipos compatibles, bloques/hilos explícitos.
5. Distribución 1D en X, un píxel por hilo, vecinos en memoria global, control de límites, entrada/salida separadas.
6. Equivalencia: misma precisión (float32), extensión con ceros y tratamiento del resultado; arreglos contiguos; tipos documentados.
7. Validación: prueba manual pequeña, prueba de no múltiplo, error máx/medio vs C++ **antes del recorte**, tolerancia justificada, evidencia visual con recorte.
8. Experimentos: filtros, resolución, máscara (4 versiones) e hilos (CUDA C y PyCUDA); un factor a la vez; Python secuencial con piloto, «no completada» documentada y resolución menor común.
9. Medición: calentamiento, ≥5 repeticiones, mediana y variabilidad; `perf_counter` en CPU; eventos CUDA (H2D, kernel, D2H, total); init de contexto y compilación aparte; declarar si `mem_alloc` está en el tiempo.
10. Aceleraciones (CUDA C/C++, PyCUDA/Python sec., kernel y con transferencias; CUDA C vs PyCUDA), CSV completos, entorno registrado, README reproducible y trazabilidad (commit P01, commit P02, nuevo vs reutilizado).

## 2. Qué se reutiliza, qué es nuevo y qué P01 no cubre

| Se reutiliza de P01 | Es nuevo en P02 | Lo que P01 no cubre y la guía sí exige |
|---|---|---|
| Kernel `convolucionGPU` (`src/filtros.cu:40-59`), copiado sin cambios de lógica a `src/kernels/convolucion.cu` | Programa anfitrión en Python (`main.py`, `src/*.py`) | Python secuencial con bucles explícitos y límite de tiempo |
| Máscaras: `media.cpp` (`1.0f/(k*k)`), `nitidez.cpp`, `laplaciano.cpp` | Python secuencial (`convolucion_cpu`) con acumulación `np.float32` | Referencias float32 **antes del recorte** (P01 solo guardó PGM recortados) |
| Algoritmo `convolucionCPU` (orden y, x, j, i; ceros por límites) como especificación | Host PyCUDA: contexto manual, `SourceModule`, `mem_alloc`, `memcpy_htod/dtoh`, eventos | Columnas `version`, `estado`, `observaciones`, `origen` en el CSV |
| Secuencia de eventos de `ejecutarGPU` (`filtros.cu:71-101`) | `referencia_cpp/`: herramienta que **enlaza** las fuentes de P01 por ruta relativa | `entorno.json` (CPU, RAM, GPU, versiones, driver, toolkit, commit, árbol limpio) |
| 12 casos de `pruebaManual` y la prueba de no múltiplo (`experimentos.cu:124-186`) | `inicializacion.csv` (contexto y compilación/carga del kernel) | Tiempos de init de contexto y compilación aparte |
| Imágenes `.pgm` de P01 (leídas en su carpeta, verificadas por SHA-256) | Imagen de resolución menor común (+ piloto) generada con el mismo procedimiento | Resolución menor común con las 4 versiones, incluidos C++ y CUDA C |
| Estructura de carpetas, nombres en español, `REPETICIONES=10`, `TOLERANCIA=1e-2`, calentamiento GPU de 2 s | Tests `pytest` | Aceleraciones PyCUDA vs Python sec. y CUDA C vs PyCUDA |
| `generar_graficas.py` (se adapta a 4 versiones) | Gráficas/tablas Markdown de 4 versiones, evidencia PNG con recorte | Trazabilidad: commit P01/P02, `nuevo` vs `reutilizado_p01` |

## 3. Árbol propuesto (espejo de P01, según CLAUDE.md)

```
GuillenJ_SolanoA_Practica02/
├── README.md  EJECUCION.md  requirements.txt  .gitignore  pytest.ini
├── ejecutar_todo.bat          # vcvars64 (vía vswhere, fallback a la ruta de P01) → preparar, tests, validar, medir, graficar
├── main.py                    # equivale a main.cu: llama a src.experimentos
├── datos/                     # hashes_p01.json, preparacion.json, base_<N>.pgm (menor común), piloto_250/500.pgm
├── referencia_cpp/            # referencia.cu (main propio) + compilar_referencia.bat; enlaza ../../GuillenJ_SolanoA_Practica0/src/*
├── resultados/{mediciones,pruebas,imagenes,graficas,referencias}/
├── scripts/                   # preparar_imagenes.py, limpiar_resultados.py, generar_graficas.py,
│                              # registrar_entorno.py, piloto_python.py, (convertir_p01.py si se reutiliza)
├── src/
│   ├── __init__.py  configuracion.py  experimentos.py  convolucion.py  imagenes.py  contexto_cuda.py
│   ├── filtros/      __init__, mascaras.py, media.py, nitidez.py, laplaciano.py
│   ├── secuencial/   __init__, filtros_secuenciales.py, media.py, nitidez.py, laplaciano.py
│   ├── paralelo/     __init__, filtros_paralelos.py, media.py, nitidez.py, laplaciano.py
│   └── kernels/convolucion.cu
└── tests/  test_mascaras.py, test_prueba_manual.py, test_no_multiplo.py, test_tipos.py, test_humo_pycuda.py
```

**Choques de nombres en Python (avisos):**
- `src/filtros.py` chocaría con el paquete `src/filtros/` → se usa `convolucion.py` (ya lo fija CLAUDE.md).
- Hay tres `media.py`/`nitidez.py`/`laplaciano.py` (en `filtros/`, `secuencial/`, `paralelo/`): no chocan si todo es paquete con `__init__.py` e imports absolutos (`from src.secuencial import media`). Nunca se mete una subcarpeta de `src/` en `sys.path`.
- `scripts/` y `tests/` importan `src` desde la raíz de P02: `python -m scripts.x` y `pytest.ini` con `pythonpath = .`.
- Único archivo extra respecto a CLAUDE.md: `src/contexto_cuda.py` (contexto manual + carga del kernel, para no mezclarlo con la medición). Si prefieren, va dentro de `paralelo/filtros_paralelos.py`.

## 4. Plan por fases con criterio de aceptación

| Fase | Qué se hace | Criterio de aceptación |
|---|---|---|
| **0** | Este plan → `docs/plan_practica02.md` + commit | Aprobado por ustedes; commit solo agrega ese archivo |
| **1** | `.gitignore` **antes** del `.venv`; `py -3.12 -m venv .venv`; `requirements.txt` con versiones fijas; esqueleto con docstring de una línea; `registrar_entorno.py`; humo PyCUDA; `ejecutar_todo.bat` con vcvars64 | `pip install` OK en el `.venv` (si PyCUDA falla: diagnóstico + opciones, sin cambiar de Python); kernel trivial compila y corre; `entorno.json` con todos los campos; `git status` sin `.venv` |
| **2** | `imagenes.py`, máscaras, `convolucion.py` (`crear_mascara`, `convolucion_cpu` con límite por fila y excepción `TiempoExcedido`, `ejecutar_cpu`, `comparar`), `secuencial/`, `hashes_p01.json` (generado por script) | 12 casos manuales leídos de `experimentos.cu` pasan en CPU (±1e-3 como P01); test de máscaras float32 pasa; test del límite de tiempo pasa; ningún `float64` en datos ni acumulación |
| **3** | `kernels/convolucion.cu`, contexto manual, `SourceModule(-O3, arch=sm_86)`, `inicializacion.csv`, `ejecutar_gpu` con e0..e3, `paralelo/` | 12 casos manuales en GPU; no múltiplo 1013×757 con 128/256/512: cobertura total (centinela NaN) y bordes; test de tipos (float32, C-contiguo, `np.int32`) |
| **4** | `referencia_cpp/` (enlaza P01), `.bin` float32 de C++ y CUDA C, `prueba_manual.csv` y `validacion.csv` con las 4 versiones, tolerancia razonada | Python sec. vs C++ y CUDA C vs PyCUDA esperados **bit a bit** (error 0); CUDA C/PyCUDA vs C++ ≤ tolerancia; máscaras bit a bit vs C++; `git diff` de P01 vacío |
| **5** | Piloto Python sec. (250², 500²; media 3/9/21; 3 reps) → tabla «estimación para planificar, no es resultado» | **PARADA B**: ustedes fijan límite, resolución N y reutilizar/repetir C++ y CUDA C |
| **6** | `generar_graficas.py` y tablas listos **antes** de medir (para no tocar `scripts/` después); commit; `entorno.json`; rápidas (C++, CUDA C, PyCUDA); luego Python sec. en segundo plano | **PARADA C** antes de Python sec.; CSV con el esquema de CLAUDE.md; reanudable; log de progreso |
| **7** | Gráficas, aceleraciones, tablas CSV/MD, evidencia visual (original + 3 filtros + recorte) | Todo sale de CSV; `no_completada` aparece como texto, nunca como aceleración |
| **8** | READMEs, EJECUCION.md, trazabilidad, auditoría vs rúbrica con evidencia, prueba en clon limpio | Cada criterio con archivo/línea/fila; código de medición sin cambios desde el commit de `entorno.json` |
| **9** | `docs/defensa.md` + 5 preguntas | **PARADA D**: resumen final |

Cada fase: `pytest` → comprobar P01 intacta → `git add` por nombre/carpeta → `git status` sin `.venv/.bin/.exe` → commit (nunca push) → resumen ≤10 líneas + explicación breve de cada archivo importante.

**Calendario propuesto:** hoy 10-nov F0–F3 · 11-nov F4–F5 (parada B) y F6 rápidas · noche 11→12 arranca Python sec. · 12–13-nov Python sec. sigue; ustedes avanzan el informe · 14-nov F7–F9 · 15-nov margen. Presupuesto máximo de Python sec.: ~60 h de reloj (debe terminar el 14-nov por la mañana); el límite por corrida se elige para respetarlo.

## 5. Dudas y riesgos

**(a) Exportar float32 de C++ y CUDA C sin modificar P01.** `referencia_cpp/referencia.cu` tiene su propio `main` y se compila con `nvcc -O3 -arch=sm_86` enlazando **por ruta relativa** las fuentes de P01 sin copiarlas: `filtros.cu`, `imagenes.cpp`, `filtros/*.cpp`, `secuencial/*.cpp`, `paralelo/*.cu` (no `experimentos.cu` ni `main.cu`, que traen rutas fijas y su propio `main`). Llama a `leerPGM`, `crearMascara`, `convolucionCPU` y `ejecutarGPU` de P01 tal cual y escribe la salida cruda (`float32`, little-endian, sin cabecera) en `resultados/referencias/<version>_<filtro><k>_<ancho>x<alto>[_h<hilos>].bin`, también para la matriz 5×5 y las máscaras (test bit a bit). Los `.bin` van en `.gitignore` (≈2 GB en disco en total) y se regeneran con un script. El `.exe` queda en `referencia_cpp/` (ignorado) y se ejecuta con directorio de trabajo en P02.

**(b) C++ y CUDA C sobre una imagen más pequeña sin alterar su lógica.** El mismo `referencia.cu` tiene un modo `medir <imagen> <filtro> <k> <hilos>` que replica el bucle de `ejecutar()` de P01 (`experimentos.cu:49-121`: 1 calentamiento CPU + 10 reps con `ejecutarFiltroCPU`; 2 s de calentamiento GPU + 10 reps con `ejecutarFiltroGPU`; `cudaMalloc` fuera del tiempo). Ese bucle hay que reescribirlo (~30 líneas) porque `ejecutar()` está en un `namespace` anónimo con rutas y CSV fijos; **las funciones que miden (`ejecutarCPU` con `steady_clock`, `ejecutarGPU` con eventos) y el kernel son los de P01 sin tocar**. Sirve para la resolución N y, si ustedes deciden repetir, para todas las configuraciones de P01. Si se reutiliza, `convertir_p01.py` lee (sin modificar) el `mediciones.csv` de P01 y lo pasa al esquema nuevo con `origen=reutilizado_p01`. Mi recomendación previa: **repetir** (son minutos y deja todo con el mismo binario, driver y sesión), pero lo deciden en la parada B.

**(c) Inicialización de contexto y compilación por separado.** Sin `pycuda.autoinit`: `cuda.init()` + `Device(0).make_context()` cronometrado con `perf_counter` → fila `contexto`. Compilación: `SourceModule(codigo, options=["-O3"], arch="sm_86", cache_dir=False)` (fuerza `nvcc`) → fila `compilacion_sin_cache`; luego una carga con la caché por defecto → `carga_con_cache` (columna `uso_cache`); y `get_function` aparte. Se hace una vez por proceso, nunca dentro de las repeticiones. Opcional útil para la pregunta 4: medir también `cudaFree(0)` en `referencia.cu` para tener la init de contexto de CUDA C. Nota: `SourceModule` envuelve el código en `extern "C"`, lo que no cambia la lógica del kernel.

**(d) Acotar Python secuencial.** `convolucion_cpu(..., limite_segundos)` consulta `perf_counter()` al inicio de cada fila; si se excede lanza `TiempoExcedido(transcurrido, filas_procesadas)`. El experimento lo captura y escribe `estado=no_completada`, `t_total`=tiempo transcurrido real y `observaciones="límite X min; filas Y/alto"`. Corre como proceso aparte en segundo plano, con log en `resultados/mediciones/progreso_python.log`, escribe cada fila con `flush` y al reanudar salta lo que ya está en el CSV. Calentamiento: 1 corrida completa no medida cuando sea viable; las inviables se intentan una vez sin calentamiento.

**Otros puntos y riesgos:**
1. **Equivalencia numérica (para defenderla):** el host de C++ (MSVC x64, SSE2) no genera FMA, así que Python sec. con `np.float32` (producto redondeado y suma redondeada) debería coincidir **bit a bit** con C++. `nvcc` contrae `suma += a*b` en FMA por defecto (`--fmad=true`), y eso explica los errores ~1e-4 de P01 en media (nitidez y laplaciano dan 0 porque operan con enteros exactos). CUDA C y PyCUDA (mismo kernel y mismos flags) deberían dar error 0 entre sí. Tolerancia: la cota pesimista `n·ε·max|suma|` para 21×21 (441·1.19e-7·255 ≈ 1.3e-2) supera 1e-2; en la Fase 4 propongo la tolerancia con esa cota y la cota realista, y la comparo con los errores observados.
2. **Velocidad de Python sec.:** los escalares `np.float32` son lentos. La imagen se pasa a una lista de escalares `np.float32` **dentro** del tiempo medido (es lo honesto). Es probable que 9×9 y 21×21 en 4000²/6000² queden `no_completada`; el piloto lo dirá.
3. **PyCUDA en Windows/3.12:** no hay wheel oficial para Windows; `pip` lo compilará y necesita `cl.exe` y `CUDA_PATH` (se instala desde un entorno con vcvars64). Si falla, diagnóstico y opciones, sin cambiar de Python.
4. **`cl.exe` en PATH** también en ejecución (`SourceModule` llama a `nvcc`): tests y `main.py` se lanzan desde `ejecutar_todo.bat` o `cmd /c "vcvars64.bat && …"`.
5. **Contaminación de tiempos:** pidieron que Python sec. corra mientras preparan el informe, pero la guía dice no usar el equipo mientras mide. Propongo: rápidas sin uso del equipo; Python sec. preferentemente de noche, sin solaparlo con mediciones GPU, y anotar en `observaciones` si el equipo estuvo en uso. Lo confirmamos en la parada C.
6. **Resolución menor común N:** propongo correr en N las mismas configuraciones de las 4 versiones (media/nitidez/laplaciano 3×3, media 9×9, media 21×21) para tener la comparación completa de filtros y máscaras; lo confirman en la parada B.
7. **Imágenes nuevas:** se generan desde `ImagenGrande.jpg` de P01 (solo lectura) con Pillow 13 (`py -3.12` usará la versión fijada). Diagnóstico opcional: regenerar `base_2000` en memoria y comparar su hash con el de P01 para saber si la versión de Pillow reproduce P01 (sin escribir nada en P01).
8. **README raíz:** la guía `.md` dice «no se toca», pero CLAUDE.md y su mensaje permiten reescribirlo en la Fase 8 con su aprobación. Gana CLAUDE.md; se lo pido en la Fase 8 y la verificación de intactos se hace solo sobre `GuillenJ_SolanoA_Practica0`.
9. **Trazabilidad:** `generar_graficas.py` se escribe y prueba con datos del piloto **antes** del commit de medición, para que `scripts/` no cambie después. Si luego hubiera que corregirlo, se declara en la auditoría.
10. **«Los commits solo agregan archivos nuevos»:** lo interpreto como que solo se tocan archivos de `GuillenJ_SolanoA_Practica02/`, `docs/` y `CLAUDE.md` (los de P02 sí se editan entre fases).

## Verificación global

- `pytest` desde P02 (con vcvars): máscaras, 12 casos manuales en CPU/GPU, no múltiplo 128/256/512, tipos, humo.
- `git diff --stat practica01-entrega -- GuillenJ_SolanoA_Practica0` vacío antes de cada commit.
- `validacion.csv`: 4 versiones, errores antes del recorte, todos ≤ tolerancia.
- Fase 8: clon limpio → `py -3.12 -m venv .venv`, `pip install -r requirements.txt`, `pytest`, y pasos rápidos de `ejecutar_todo.bat`.
