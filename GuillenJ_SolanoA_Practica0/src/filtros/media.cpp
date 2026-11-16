
#include "mascaras.h"

std::vector<float> crearMascaraMedia(int tamano) {
    return std::vector<float>(tamano * tamano, 1.0f / (tamano * tamano));
}
