












__global__ void convolucionGPU(const float* entrada, float* salida,
                               const float* mascara, int ancho, int alto,
                               int k) {
    int id = blockIdx.x * blockDim.x + threadIdx.x;
    int n = ancho * alto;
    if (id >= n) return;

    int y = id / ancho, x = id % ancho, radio = k / 2;
    float suma = 0;
    for (int j = -radio; j <= radio; j++) {
        for (int i = -radio; i <= radio; i++) {
            int yy = y + j, xx = x + i;
            if (yy >= 0 && yy < alto && xx >= 0 && xx < ancho) {
                suma += entrada[yy * ancho + xx] *
                        mascara[(j + radio) * k + i + radio];
            }
        }
    }
    salida[id] = suma;
}
