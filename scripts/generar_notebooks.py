"""Genera los notebooks del libro a partir de codigo/.

Por cada capítulo capNN_nombre.py se generan:

- capNN_nombre.ipynb: la lección, precedida por una celda oculta con el
  código acumulable de los capítulos anteriores.
- control_capNN.ipynb: solo las celdas acumulables de los capítulos 1 a NN.
- soluciones_capNN.ipynb: si existe codigo/soluciones/capNN_nombre.py.

Uso: uv run python scripts/generar_notebooks.py
"""

import sys
from pathlib import Path

import jupytext
import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import (
    CODIGO,
    NOTEBOOKS,
    archivos_de_capitulos,
    numero_de_capitulo,
    quitar_marcas_de_fragmentos,
)

ETIQUETAS = {"acumulable", "exploracion"}

METADATOS_NOTEBOOK = {
    "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
    "language_info": {"name": "python"},
}


def leer_celdas(archivo, exigir_etiquetas):
    """Lee un archivo en formato percent y devuelve sus celdas limpias."""
    notebook = jupytext.read(archivo)
    celdas = []
    for celda in notebook.cells:
        if celda.cell_type == "code":
            etiquetas = set(celda.metadata.get("tags", []))
            if exigir_etiquetas and len(etiquetas & ETIQUETAS) != 1:
                raise ValueError(
                    f"{Path(archivo).name}: toda celda de código debe tener "
                    f"exactamente una etiqueta {sorted(ETIQUETAS)}.\n"
                    f"Celda:\n{celda.source[:200]}"
                )
            celda.source = quitar_marcas_de_fragmentos(celda.source)
        celdas.append(celda)
    return celdas


def es_acumulable(celda):
    return celda.cell_type == "code" and "acumulable" in celda.metadata.get("tags", [])


def celda_estado_previo(codigo_previo):
    """Celda plegada (formulario de Colab) con el código de capítulos anteriores."""
    fuente = (
        "# @title Código de los capítulos anteriores (ejecutar primero)\n"
        + codigo_previo
    )
    return nbformat.v4.new_code_cell(fuente, metadata={"cellView": "form"})


def nuevo_notebook(celdas):
    notebook = nbformat.v4.new_notebook(metadata=METADATOS_NOTEBOOK)
    for numero, celda in enumerate(celdas, 1):
        # Identificadores fijos: regenerar sin cambios no produce diferencias en git.
        celda["id"] = f"celda-{numero:03d}"
        celda.metadata.pop("lines_to_next_cell", None)
    notebook.cells = celdas
    return notebook


def copiar(celda):
    return nbformat.from_dict(dict(celda))


def generar(codigo=CODIGO, destino=NOTEBOOKS):
    """Genera todos los notebooks y devuelve la lista de archivos escritos."""
    destino.mkdir(parents=True, exist_ok=True)
    escritos = []
    acumuladas = []

    for archivo in archivos_de_capitulos(codigo):
        numero = numero_de_capitulo(archivo)
        celdas = leer_celdas(archivo, exigir_etiquetas=True)
        previas = "\n\n".join(c.source for c in acumuladas)

        leccion = [copiar(c) for c in celdas]
        if previas:
            leccion.insert(0, celda_estado_previo(previas))
        escritos.append(escribir(leccion, destino / f"{archivo.stem}.ipynb"))

        acumuladas += [copiar(c) for c in celdas if es_acumulable(c)]

        titulo = nbformat.v4.new_markdown_cell(
            f"# Punto de control: capítulo {numero}\n\n"
            "Todo el código de la calculadora hasta este capítulo. "
            "Ejecute las celdas en orden y continúe con el capítulo siguiente."
        )
        control = [titulo] + [copiar(c) for c in acumuladas]
        escritos.append(escribir(control, destino / f"control_cap{numero:02d}.ipynb"))

        soluciones = codigo / "soluciones" / archivo.name
        if soluciones.exists():
            celdas_sol = leer_celdas(soluciones, exigir_etiquetas=False)
            estado = "\n\n".join(c.source for c in acumuladas)
            if estado:
                celdas_sol.insert(0, celda_estado_previo(estado))
            nombre = f"soluciones_cap{numero:02d}.ipynb"
            escritos.append(escribir(celdas_sol, destino / nombre))

    return escritos


def escribir(celdas, ruta):
    # Saltos de línea de Unix también en Windows, para no generar cambios en git.
    with open(ruta, "w", encoding="utf-8", newline="\n") as archivo:
        nbformat.write(nuevo_notebook(celdas), archivo)
    return ruta


if __name__ == "__main__":
    for ruta in generar():
        print(f"generado: {ruta.relative_to(NOTEBOOKS.parent)}")
