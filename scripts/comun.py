"""Utilidades compartidas por los generadores y verificadores del libro."""

import re
import sys
from pathlib import Path

# Acentos correctos también en la consola de Windows
sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
CODIGO = RAIZ / "codigo"
NOTEBOOKS = RAIZ / "notebooks"
RECURSOS = RAIZ / "recursos"

PATRON_CAPITULO = re.compile(r"^cap(\d{2})_[a-z0-9_]+\.py$")
PATRON_INICIO = re.compile(r"^\s*# \[inicio: ([a-z0-9_]+)\]\s*$")
PATRON_FIN = re.compile(r"^\s*# \[fin: ([a-z0-9_]+)\]\s*$")


def archivos_de_capitulos(carpeta):
    """Devuelve los archivos capNN_*.py de una carpeta, ordenados por número."""
    archivos = [a for a in carpeta.glob("cap*.py") if PATRON_CAPITULO.match(a.name)]
    return sorted(archivos, key=numero_de_capitulo)


def numero_de_capitulo(archivo):
    """Número de capítulo de un archivo capNN_*.py."""
    return int(PATRON_CAPITULO.match(Path(archivo).name).group(1))


def quitar_marcas_de_fragmentos(codigo):
    """Elimina las líneas de marca de fragmento; el estudiante no las necesita."""
    lineas = codigo.splitlines()
    return "\n".join(
        linea
        for linea in lineas
        if not (PATRON_INICIO.match(linea) or PATRON_FIN.match(linea))
    )
