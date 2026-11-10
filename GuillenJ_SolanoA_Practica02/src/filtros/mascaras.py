"""Declaraciones de las tres mascaras de convolucion."""
from src.filtros.laplaciano import crear_mascara_laplaciano
from src.filtros.media import crear_mascara_media
from src.filtros.nitidez import crear_mascara_nitidez

__all__ = ["crear_mascara_media", "crear_mascara_nitidez", "crear_mascara_laplaciano"]
