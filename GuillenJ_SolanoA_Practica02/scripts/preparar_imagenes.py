"""Genera las imagenes nuevas de P02 con el mismo procedimiento de P01."""
import hashlib
import io
import json
import sys
from importlib import metadata

from PIL import Image

from src.configuracion import (DATOS, HASHES_P01, IMAGEN_ORIGEN_P01, IMAGENES_P01,
                               NO_MULTIPLO, RAIZ_REPO, RESOLUCIONES_NUEVAS)
from src.imagenes import sha256, verificar_datos_p01

Image.MAX_IMAGE_PIXELS = None


def registrar_hashes_p01():
    """Registra una sola vez el SHA-256 de los .pgm de P01; despues solo los verifica."""
    if HASHES_P01.exists():
        print(f"Datos de P01 verificados ({verificar_datos_p01()} archivos).")
        return
    rutas = list(IMAGENES_P01.values()) + [NO_MULTIPLO]
    registro = {
        "descripcion": "SHA-256 de las imagenes de P01 (tag practica01-entrega). "
                       "Se comprueban al inicio de cada ejecucion; no se regeneran.",
        "sha256": {r.relative_to(RAIZ_REPO).as_posix(): sha256(r) for r in rutas},
    }
    HASHES_P01.write_text(json.dumps(registro, indent=2), encoding="utf-8")
    print(f"Hashes de P01 registrados en {HASHES_P01.relative_to(RAIZ_REPO)}")


def base_cuadrada():
    """Recorte cuadrado centrado en gris, igual que preparar_imagenes.py de P01."""
    original = Image.open(IMAGEN_ORIGEN_P01)
    base = original.convert("L")
    lado = min(base.size)
    x = (base.width - lado) // 2
    y = (base.height - lado) // 2
    return original.size, (x, y, x + lado, y + lado), base.crop((x, y, x + lado, y + lado))


def hash_pgm_en_memoria(imagen):
    memoria = io.BytesIO()
    imagen.save(memoria, format="PPM")  # Pillow guarda "L" como P5 (PGM), igual que P01
    return hashlib.sha256(memoria.getvalue()).hexdigest()


def main(resoluciones):
    DATOS.mkdir(exist_ok=True)
    registrar_hashes_p01()

    tamano_original, recorte, base = base_cuadrada()
    registro = {"origen": IMAGEN_ORIGEN_P01.relative_to(RAIZ_REPO).as_posix(),
                "base_original": tamano_original, "recorte": recorte,
                "procedimiento": "convert('L') + recorte cuadrado centrado + resize LANCZOS",
                "pillow": metadata.version("pillow")}

    for n in resoluciones:
        destino = DATOS / f"base_{n}.pgm"
        base.resize((n, n), Image.LANCZOS).save(destino)
        registro[destino.name] = {"tamano": [n, n], "sha256": sha256(destino)}
        print(f"Generada {destino.relative_to(RAIZ_REPO)}")

    # Diagnostico (solo en memoria, no escribe en P01): este Pillow reproduce base_2000 de P01?
    base_2000 = base.resize((2000, 2000), Image.LANCZOS)
    reproduce = hash_pgm_en_memoria(base_2000) == sha256(IMAGENES_P01[2000])
    registro["pillow_reproduce_base_2000_p01"] = reproduce
    print(f"Este Pillow reproduce base_2000.pgm de P01 bit a bit: {reproduce}")

    (DATOS / "preparacion.json").write_text(json.dumps(registro, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main([int(n) for n in sys.argv[1:]] or RESOLUCIONES_NUEVAS)
