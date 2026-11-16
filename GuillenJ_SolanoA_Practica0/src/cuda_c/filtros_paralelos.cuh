
#pragma once
#include "../filtros.cuh"

TiemposGPU mediaGPU(const float*, float*, float*, float*, float*, int, int, int, int);
TiemposGPU nitidezGPU(const float*, float*, float*, float*, float*, int, int, int, int);
TiemposGPU laplacianoGPU(const float*, float*, float*, float*, float*, int, int, int, int);


inline TiemposGPU ejecutarFiltroGPU(int filtro, const float* entrada,
                                    float* salida, float* dEntrada,
                                    float* dSalida, float* dMascara,
                                    int ancho, int alto, int k, int hilos) {
    if (filtro == MEDIA)
        return mediaGPU(entrada, salida, dEntrada, dSalida, dMascara,
                        ancho, alto, k, hilos);
    if (filtro == NITIDEZ)
        return nitidezGPU(entrada, salida, dEntrada, dSalida, dMascara,
                          ancho, alto, k, hilos);
    return laplacianoGPU(entrada, salida, dEntrada, dSalida, dMascara,
                         ancho, alto, k, hilos);
}
