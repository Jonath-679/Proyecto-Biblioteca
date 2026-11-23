"""
rutas.py
========
Modulo central de rutas del sistema.

Todas las rutas del programa (base de datos, imagenes, sonidos) se calculan
a partir de la carpeta donde vive el proyecto, NUNCA con rutas absolutas.
Gracias a esto la carpeta completa puede copiarse a otra computadora (o a
una USB) y el programa sigue funcionando sin cambiar nada.

Tambien soporta el modo "congelado" (ejecutable generado con PyInstaller):
en ese caso la carpeta base es la carpeta donde esta el .exe.
"""

import os
import sys

# carpeta base del proyecto
if getattr(sys, "frozen", False):
    # ejecutable generado con pyinstaller: los datos viven junto al .exe
    CARPETA_BASE = os.path.dirname(os.path.abspath(sys.executable))
else:
    # ejecucion normal con python: carpeta donde esta este archivo
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# archivo de base de datos sqlite
RUTA_DB = os.path.join(CARPETA_BASE, "biblioteca.db")

# carpeta de recursos
RUTA_RECURSOS = os.path.join(CARPETA_BASE, "recursos")

# carpeta donde se guardan las portadas (nombre = codigo del libro)
RUTA_IMAGENES = os.path.join(RUTA_RECURSOS, "imagenes")

# sonido que se reproduce al prestar / devolver
RUTA_SONIDO_EXITO = os.path.join(RUTA_RECURSOS, "sonidos", "exito.wav")

# extensiones de imagen aceptadas para portadas
EXTENSIONES_PORTADA = ["png", "jpg", "jpeg"]


def buscar_portada(codigo_libro):
    """Regresa la ruta de la portada de un libro o None si no tiene."""
    for extension in EXTENSIONES_PORTADA:
        posible_ruta = os.path.join(RUTA_IMAGENES, f"{codigo_libro}.{extension}")
        if os.path.exists(posible_ruta):
            return posible_ruta
    return None


def borrar_portadas(codigo_libro):
    """Borra todas las portadas de un libro. Regresa True si borro alguna."""
    borrada = False
    for extension in EXTENSIONES_PORTADA:
        ruta = os.path.join(RUTA_IMAGENES, f"{codigo_libro}.{extension}")
        if os.path.exists(ruta):
            os.remove(ruta)
            borrada = True
    return borrada


def guardar_portada(ruta_origen, codigo_libro):
    """Copia una imagen como portada del libro (reemplaza la anterior)."""
    import shutil

    os.makedirs(RUTA_IMAGENES, exist_ok=True)

    # extension siempre en minusculas para que se encuentre en cualquier sistema
    extension = os.path.splitext(ruta_origen)[1].lstrip(".").lower()
    if extension not in EXTENSIONES_PORTADA:
        extension = "png"

    ruta_destino = os.path.join(RUTA_IMAGENES, f"{codigo_libro}.{extension}")

    # si la imagen elegida ya es la portada actual no hay nada que hacer
    if os.path.exists(ruta_destino) and os.path.samefile(ruta_origen, ruta_destino):
        return ruta_destino

    # quita portadas viejas con otra extension para que no queden duplicadas
    borrar_portadas(codigo_libro)
    shutil.copy(ruta_origen, ruta_destino)
    return ruta_destino
