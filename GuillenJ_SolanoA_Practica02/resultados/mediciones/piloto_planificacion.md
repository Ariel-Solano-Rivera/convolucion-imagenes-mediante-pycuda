# Piloto de Python secuencial — ESTIMACIÓN PARA PLANIFICAR, NO ES RESULTADO

Los tiempos de esta tabla **no son mediciones**: se extrapolan del piloto con
costo ∝ píxeles × k × k. No se usan en el informe como tiempos medidos.

## Costo medido en el piloto (ns por píxel × coeficiente, mediana)

| k | 250×250 | 500×500 |
|---|---|---|
| 3 | 192.8 | 185.1 |
| 9 | 154.3 | 150.9 |
| 21 | 149.4 | 150.5 |

## Estimación de UNA corrida (minutos) — no es resultado

| resolución | media 3×3 | media 9×9 | media 21×21 |
|---|---|---|---|
| 750×750 | 0.0 | 0.1 | 0.6 |
| 1000×1000 | 0.0 | 0.2 | 1.1 |
| 1500×1500 | 0.1 | 0.5 | 2.5 |
| 2000×2000 | 0.1 | 0.8 | 4.4 |
| 4000×4000 | 0.4 | 3.3 | 17.7 |
| 6000×6000 | 1.0 | 7.3 | 39.8 |

## Estimación del plan completo (horas) — no es resultado

Cada configuración viable = 1 calentamiento + 5 repeticiones = 6 corridas.

- Experimentos a 2000/4000/6000 si todo se completara: 3.0 h
- Resolución menor común 750×750 (5 configuraciones × 6 corridas): 0.08 h
- Resolución menor común 1000×1000 (5 configuraciones × 6 corridas): 0.14 h
- Resolución menor común 1500×1500 (5 configuraciones × 6 corridas): 0.31 h
