"""Ejecuta el código de cada capítulo y guarda la salida de cada fragmento.

Las celdas se ejecutan en orden, igual que en el notebook de la lección:
primero el código acumulable de los capítulos anteriores y después las celdas
del capítulo. Si una celda contiene el fragmento "nombre" y produce salida,
esa salida se guarda en recursos/salidas/nombre.txt. Como en Jupyter, si la
última línea de una celda es una expresión, se muestra su valor.

LaTeX la incluye con \\salida{nombre} y la web con <Salida nombre="..." />.

Uso: uv run python scripts/generar_salidas.py
"""

import ast
import contextlib
import io
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import jupytext

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import CODIGO, PATRON_INICIO, RECURSOS, archivos_de_capitulos


def ejecutar_celda(fuente, espacio):
    """Ejecuta una celda en el espacio de nombres dado y devuelve lo que imprime."""
    arbol = ast.parse(fuente)
    ultima = None
    if arbol.body and isinstance(arbol.body[-1], ast.Expr):
        ultima = ast.Expression(arbol.body.pop().value)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        # Ejecutar el código del libro es justamente el propósito de este script.
        exec(compile(arbol, "<celda>", "exec"), espacio)  # noqa: S102
        if ultima is not None:
            valor = eval(compile(ultima, "<celda>", "eval"), espacio)
            if valor is not None:
                print(repr(valor))
    return salida.getvalue()


def fragmentos_de(fuente):
    return [
        m.group(1) for linea in fuente.splitlines() if (m := PATRON_INICIO.match(linea))
    ]


def celdas_de_codigo(archivo):
    return [c for c in jupytext.read(archivo).cells if c.cell_type == "code"]


def ejecutar_archivo(archivo, codigo_previo, salidas):
    """Ejecuta un archivo de capítulo y anota la salida de sus fragmentos."""
    espacio = {"__name__": "__main__"}
    for fuente in codigo_previo:
        ejecutar_celda(fuente, espacio)
    for celda in celdas_de_codigo(archivo):
        texto = ejecutar_celda(celda.source, espacio)
        for nombre in fragmentos_de(celda.source):
            if texto:
                salidas[nombre] = texto


def generar(codigo=CODIGO, destino=RECURSOS / "salidas"):
    """Genera todas las salidas y devuelve sus nombres."""
    salidas = {}
    acumulado = []
    for archivo in archivos_de_capitulos(codigo):
        ejecutar_archivo(archivo, acumulado, salidas)
        acumulado += [
            c.source
            for c in celdas_de_codigo(archivo)
            if "acumulable" in c.metadata.get("tags", [])
        ]
        soluciones = codigo / "soluciones" / archivo.name
        if soluciones.exists():
            ejecutar_archivo(soluciones, acumulado, salidas)

    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("*.txt"):
        if viejo.stem not in salidas:
            viejo.unlink()
    for nombre, texto in salidas.items():
        (destino / f"{nombre}.txt").write_text(texto, encoding="utf-8", newline="\n")
    return sorted(salidas)


if __name__ == "__main__":
    nombres = generar()
    print(f"{len(nombres)} salidas generadas")
