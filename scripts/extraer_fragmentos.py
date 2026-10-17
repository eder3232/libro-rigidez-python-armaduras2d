"""Extrae los fragmentos de código marcados en codigo/ a recursos/fragmentos/.

Un fragmento se marca así:

    # [inicio: rigidez_barra]
    ...
    # [fin: rigidez_barra]

LaTeX lo incluye con \\fragmento{rigidez_barra} y la web lo importa por nombre.

Uso: uv run python scripts/extraer_fragmentos.py
"""

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import CODIGO, PATRON_FIN, PATRON_INICIO, RECURSOS


def leer_fragmentos(archivo):
    """Devuelve {nombre: código} de los fragmentos marcados en un archivo."""
    fragmentos = {}
    abierto = None
    lineas = []
    for numero, linea in enumerate(
        Path(archivo).read_text(encoding="utf-8").splitlines(), 1
    ):
        if inicio := PATRON_INICIO.match(linea):
            if abierto:
                raise ValueError(f"{archivo}:{numero}: '{abierto}' no se cerró")
            abierto, lineas = inicio.group(1), []
        elif fin := PATRON_FIN.match(linea):
            if fin.group(1) != abierto:
                raise ValueError(
                    f"{archivo}:{numero}: fin de '{fin.group(1)}' sin inicio"
                )
            fragmentos[abierto] = textwrap.dedent("\n".join(lineas)).strip("\n") + "\n"
            abierto = None
        elif abierto:
            lineas.append(linea)
    if abierto:
        raise ValueError(f"{archivo}: '{abierto}' no se cerró")
    return fragmentos


def extraer(codigo=CODIGO, destino=RECURSOS / "fragmentos"):
    """Escribe cada fragmento en su archivo y devuelve los nombres extraídos."""
    todos = {}
    for archivo in sorted(codigo.rglob("*.py")):
        if "tests" in archivo.parts:
            continue
        for nombre, fuente in leer_fragmentos(archivo).items():
            if nombre in todos:
                raise ValueError(f"fragmento duplicado: '{nombre}' en {archivo}")
            todos[nombre] = fuente

    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("*.py"):
        if viejo.stem not in todos:
            viejo.unlink()
    for nombre, fuente in todos.items():
        (destino / f"{nombre}.py").write_text(fuente, encoding="utf-8", newline="\n")
    return sorted(todos)


if __name__ == "__main__":
    nombres = extraer()
    print(f"{len(nombres)} fragmentos extraídos")
