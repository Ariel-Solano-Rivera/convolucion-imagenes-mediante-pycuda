# Práctica 02 · Convolución de imágenes con PyCUDA

Guillén J. y Solano A. — Computación Paralela (UPS).

Migración a Python del programa anfitrión de la práctica 01 (`../GuillenJ_SolanoA_Practica0/`,
etiqueta git `practica01-entrega`) y ejecución del mismo kernel CUDA C mediante PyCUDA.
Se comparan cuatro versiones: C/C++ secuencial, CUDA C, Python secuencial y PyCUDA.

Instalación y ejecución: ver [EJECUCION.md](EJECUCION.md).

> Documento en construcción: se completa en la fase de documentación.

## Validación numérica y tolerancia

La referencia es C/C++ secuencial (`convolucionCPU` de P01). Su salida float32 **antes del
recorte** se exporta con `referencia_cpp/referencia.exe`, que enlaza las fuentes de P01 sin
modificarlas. Los errores absolutos máximo y medio de Python secuencial, CUDA C y PyCUDA están
en `resultados/pruebas/validacion.csv`. También se compara PyCUDA con CUDA C.

**Tolerancia.** Cada píxel es un producto punto de n = k·k términos en float32
(u = 2⁻²⁴, ε = 2⁻²³ ≈ 1.19·10⁻⁷). Cualquier implementación que acumule en float32, con o sin
FMA, cumple |calculado − exacto| ≤ γₙ·S, donde γₙ = n·u/(1 − n·u) y
S = Σ|píxel·coeficiente| ≤ 255·Σ|coeficiente|. Entre dos implementaciones, entonces:

  tolerancia(k) = 2·γₙ·255·Σ|coeficiente| ≈ n · ε · 255 · Σ|coeficiente|

| máscara | n | Σ\|coef\| | tolerancia |
|---|---|---|---|
| media 3×3 | 9 | 1 | 2.74·10⁻⁴ |
| media 9×9 | 81 | 1 | 2.46·10⁻³ |
| media 21×21 | 441 | 1 | 1.34·10⁻² |
| nitidez 3×3 | 9 | 9 | 2.46·10⁻³ |
| laplaciano 3×3 | 9 | 8 | 2.19·10⁻³ |

(Valores que da `src/convolucion.py::tolerancia`. Es una cota garantizada, no un número elegido.)

P01 usó una tolerancia fija de 10⁻². Esa cifra queda por encima de la cota para k ≤ 9, pero
para 21×21 la cota pesimista (1.34·10⁻²) la supera. Por eso P02 valida cada configuración con
su propia cota. Los errores observados quedan muy por debajo de ella (y de 10⁻²), porque
los errores de redondeo se compensan entre sí en lugar de acumularse en el peor caso.

**Diferencias esperadas y observadas:**
- *Python secuencial vs C++*: mismo orden de suma; cada producto y cada suma se redondean
  a float32 (`np.float32`). MSVC x64 no genera FMA, así que el resultado es idéntico bit a bit.
- *CUDA C/PyCUDA vs C++*: nvcc contrae `suma += a*b` en una FMA (un solo redondeo), por eso
  hay diferencias pequeñas en la media (coeficientes 1/k² no exactos). En nitidez y laplaciano
  todos los valores son enteros exactos en float32 y el error es 0.
- *PyCUDA vs CUDA C*: mismo kernel compilado con los mismos flags; resultado idéntico.
