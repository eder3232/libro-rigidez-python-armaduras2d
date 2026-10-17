"""Ejecuta el código de cada capítulo y guarda la salida de cada fragmento.

Las celdas se ejecutan en orden, igual que en el notebook de la lección:
primero el código acumulable de los capítulos anteriores y después las celdas
del capítulo. Si una celda contiene el fragmento "nombre":

- y produce texto, se guarda en recursos/salidas/nombre.txt. Como en Jupyter,
  si la última línea de la celda es una expresión, se muestra su valor;
- y dibuja un gráfico de Matplotlib, se guarda en recursos/graficos/nombre.pdf
  (para el libro) y en web/public/graficos/nombre.svg (para la web).

LaTeX las incluye con \\salida{nombre} y \\grafico{nombre}; la web con
<Salida nombre="..." /> y <Grafico nombre="..." />.

Uso: uv run python scripts/generar_salidas.py
"""

import ast
import contextlib
import io
import os
import re
import sys
import warnings
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import jupytext
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import CODIGO, PATRON_INICIO, RAIZ, RECURSOS, archivos_de_capitulos

FUENTES = RAIZ / "web" / "src" / "fuentes"


def configurar_graficos():
    """Aplica la tipografía y los tamaños del libro a los gráficos.

    Solo afecta a las figuras del libro: en Colab, el estudiante ve el estilo
    por defecto de Matplotlib con el mismo código.
    """
    for fuente in FUENTES.glob("Libertinus*.otf"):
        font_manager.fontManager.addfont(str(fuente))
    mpl.rcParams.update(
        {
            "font.family": "Libertinus Sans",
            "mathtext.fontset": "stix",
            "font.size": 10,
            "figure.figsize": (4.5, 3.2),
            "savefig.bbox": "tight",
            "svg.fonttype": "path",
            "pdf.fonttype": 42,
        }
    )


def ejecutar_celda(fuente, espacio):
    """Ejecuta una celda en el espacio de nombres dado y devuelve lo que imprime."""
    arbol = ast.parse(fuente)
    ultima = None
    if arbol.body and isinstance(arbol.body[-1], ast.Expr):
        ultima = ast.Expression(arbol.body.pop().value)
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida), warnings.catch_warnings():
        # plt.show() avisa que el modo sin pantalla no muestra ventanas.
        warnings.filterwarnings("ignore", message=".*non-interactive.*")
        # Ejecutar el código del libro es justamente el propósito de este script.
        exec(compile(arbol, "<celda>", "exec"), espacio)  # noqa: S102
        if ultima is not None:
            valor = eval(compile(ultima, "<celda>", "eval"), espacio)
            if valor is not None and not _es_objeto_grafico(valor):
                print(repr(valor))
    return salida.getvalue()


def _es_objeto_grafico(valor):
    """Los objetos de Matplotlib no se muestran como texto, sino como gráfico."""
    return type(valor).__module__.startswith("matplotlib") or (
        isinstance(valor, list)
        and valor
        and type(valor[0]).__module__.startswith("matplotlib")
    )


def fragmentos_de(fuente):
    return [
        m.group(1) for linea in fuente.splitlines() if (m := PATRON_INICIO.match(linea))
    ]


def celdas_de_codigo(archivo):
    return [c for c in jupytext.read(archivo).cells if c.cell_type == "code"]


# Metadatos fijos: regenerar sin cambios no produce diferencias en git.
METADATOS = {"pdf": {"CreationDate": None, "Producer": None}, "svg": {"Date": None}}


def ejecutar_archivo(archivo, codigo_previo, salidas, graficos, destinos, valores):
    """Ejecuta un archivo de capítulo y guarda las salidas de sus fragmentos.

    destinos: {extensión: carpeta} donde se guardan los gráficos.
    valores: diccionario donde las celdas "libro" registran los números que
    cita el texto, con valor_libro(nombre, numero, decimales).
    """

    def valor_libro(nombre, numero, decimales=2):
        if not re.fullmatch(r"[a-z0-9_]+", nombre):
            raise ValueError(f"nombre de valor inválido: {nombre}")
        valores[nombre] = f"{round(float(numero), decimales) + 0.0:.{decimales}f}"

    espacio = {"__name__": "__main__", "valor_libro": valor_libro}
    for fuente in codigo_previo:
        ejecutar_celda(fuente, espacio)
    plt.close("all")
    for celda in celdas_de_codigo(archivo):
        texto = ejecutar_celda(celda.source, espacio)
        figuras = plt.get_fignums()
        for nombre in fragmentos_de(celda.source):
            if texto:
                salidas[nombre] = texto
            if figuras:
                figura = plt.figure(figuras[-1])
                for extension, carpeta in destinos.items():
                    carpeta.mkdir(parents=True, exist_ok=True)
                    figura.savefig(
                        carpeta / f"{nombre}.{extension}",
                        metadata=METADATOS[extension],
                    )
                graficos.add(nombre)
        plt.close("all")


def generar(
    codigo=CODIGO,
    destino=RECURSOS / "salidas",
    destino_pdf=RECURSOS / "graficos",
    destino_svg=RAIZ / "web" / "public" / "graficos",
    destino_valores=RECURSOS / "valores.tex",
):
    """Genera todas las salidas, gráficos y valores, y devuelve sus nombres."""
    configurar_graficos()
    destinos = {"pdf": destino_pdf, "svg": destino_svg}
    salidas, graficos, valores = {}, set(), {}
    acumulado = []
    for archivo in archivos_de_capitulos(codigo):
        ejecutar_archivo(archivo, acumulado, salidas, graficos, destinos, valores)
        # Las celdas "calculadora" también se acumulan (ver generar_notebooks)
        acumulado += [
            c.source
            for c in celdas_de_codigo(archivo)
            if {"acumulable", "calculadora"} & set(c.metadata.get("tags", []))
        ]
        soluciones = codigo / "soluciones" / archivo.name
        if soluciones.exists():
            ejecutar_archivo(
                soluciones, acumulado, salidas, graficos, destinos, valores
            )

    escribir_valores(valores, destino_valores)
    _limpiar(destino, "txt", salidas)
    _limpiar(destino_pdf, "pdf", graficos)
    _limpiar(destino_svg, "svg", graficos)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, texto in salidas.items():
        (destino / f"{nombre}.txt").write_text(texto, encoding="utf-8", newline="\n")
    return sorted(salidas) + sorted(graficos)


def escribir_valores(valores, archivo):
    """Escribe los valores como definiciones de LaTeX, leídas por \\valor{nombre}.

    Solo reescribe el archivo si cambió, para no forzar a regenerar las figuras.
    """
    lineas = ["% Generado por scripts/generar_salidas.py. No editar a mano."]
    for nombre in sorted(valores):
        lineas.append(
            rf"\expandafter\def\csname valor@{nombre}\endcsname{{{valores[nombre]}}}"
        )
    contenido = "\n".join(lineas) + "\n"
    if not archivo.exists() or archivo.read_text(encoding="utf-8") != contenido:
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(contenido, encoding="utf-8", newline="\n")


def _limpiar(carpeta, extension, vigentes):
    """Elimina los archivos de fragmentos que ya no existen."""
    for viejo in carpeta.glob(f"*.{extension}"):
        if viejo.stem not in vigentes:
            viejo.unlink()


if __name__ == "__main__":
    nombres = generar()
    print(f"{len(nombres)} salidas y gráficos generados")
