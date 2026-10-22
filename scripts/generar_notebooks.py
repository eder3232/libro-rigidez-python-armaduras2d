"""Genera los notebooks del libro a partir de codigo/.

Por cada capítulo capNN_nombre.py se generan:

- capNN_nombre.ipynb: la lección, precedida por una celda oculta con el
  código acumulable de los capítulos anteriores.
- control_capNN.ipynb: solo las celdas acumulables de los capítulos 1 a NN.
- soluciones_capNN.ipynb: si existe codigo/soluciones/capNN_nombre.py.

Además, mi_calculadora.ipynb: el notebook final del estudiante, con el motor
(las definiciones de todo el código acumulable) y las celdas "calculadora";
y calculadora.py: el mismo motor como módulo de Python. Y
validacion_opensees.ipynb: el motor, los datos de los ejemplos B y C y las
celdas "validacion" del anexo D, que los analizan también con OpenSees.

Uso: uv run python scripts/generar_notebooks.py
"""

import ast
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

# "libro": celdas que solo registran valores para el texto y las figuras del
# libro (con valor_libro); no forman parte de los notebooks.
# "calculadora": celdas de la lección que forman además las secciones Datos y
# Resultados del notebook final mi_calculadora.ipynb.
# Los anexos no exigen etiquetas: sus celdas "validacion" (anexo D) forman el
# notebook validacion_opensees.ipynb.
ETIQUETAS = {"acumulable", "exploracion", "libro", "calculadora"}

INTRODUCCION_CALCULADORA = """\
# Mi calculadora de armaduras

Análisis de armaduras planas por el método de rigidez, construido a lo largo
del libro *Análisis matricial de armaduras con Python*.

1. **Motor**: todas las funciones de la calculadora. Ejecute la celda una vez.
2. **Datos**: la armadura a analizar. Reemplace estos datos por los de su
   armadura (unidades: kN y m).
3. **Resultados**: el análisis, su verificación, los gráficos y las tablas."""

ENCABEZADO_MODULO = '''\
"""Motor de la calculadora de armaduras planas por el método de rigidez.

Construido a lo largo del libro *Análisis matricial de armaduras con Python*.
Es el mismo código de la sección Motor de mi_calculadora.ipynb.

Uso, desde un archivo o notebook en la misma carpeta:

    from calculadora import analizar_armadura, mostrar_resultados
"""

'''

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
            if "libro" in etiquetas:
                continue
            celda.source = quitar_marcas_de_fragmentos(celda.source)
        celdas.append(celda)
    return celdas


def es_acumulable(celda):
    """Las celdas "calculadora" también se acumulan: el punto de control del
    último capítulo es la calculadora completa, con sus datos."""
    etiquetas = celda.metadata.get("tags", [])
    return celda.cell_type == "code" and (
        "acumulable" in etiquetas or "calculadora" in etiquetas
    )


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


def es_definicion(nodo):
    """Imports, funciones, constantes y la configuración de NumPy: lo que
    forma el motor de la calculadora, sin los cálculos de los ejemplos."""
    if isinstance(nodo, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
        return True
    if isinstance(nodo, ast.Assign):
        # Constante: nombre en mayúsculas con un valor literal (TRACCION = "...").
        # F = ensamblar_cargas(...) es un cálculo, aunque F sea mayúscula.
        nombres = [t.id for t in nodo.targets if isinstance(t, ast.Name)]
        return (
            bool(nombres)
            and all(n.isupper() for n in nombres)
            and isinstance(nodo.value, ast.Constant)
        )
    if isinstance(nodo, ast.Expr) and isinstance(nodo.value, ast.Call):
        funcion = nodo.value.func
        return isinstance(funcion, ast.Attribute) and funcion.attr == "set_printoptions"
    return False


def motor(celdas_acumulables):
    """Código de las definiciones de las celdas "acumulable" (las celdas
    "calculadora" van en las secciones Datos y Resultados)."""
    partes = []
    for celda in celdas_acumulables:
        if "acumulable" not in celda.metadata.get("tags", []):
            continue
        arbol = ast.parse(celda.source)
        for nodo in arbol.body:
            if es_definicion(nodo):
                partes.append(ast.get_source_segment(celda.source, nodo))
    return "\n\n\n".join(partes)


def notebook_calculadora(acumuladas, celdas_calculadora):
    """Celdas del notebook final: Motor, Datos y Resultados."""
    celda_motor = nbformat.v4.new_code_cell(
        "# @title Motor de la calculadora (ejecutar primero)\n" + motor(acumuladas),
        metadata={"cellView": "form"},
    )
    celdas = [
        nbformat.v4.new_markdown_cell(INTRODUCCION_CALCULADORA),
        nbformat.v4.new_markdown_cell("## 1. Motor"),
        celda_motor,
        nbformat.v4.new_markdown_cell("## 2. Datos"),
        copiar(celdas_calculadora[0]),
        nbformat.v4.new_markdown_cell("## 3. Resultados"),
    ]
    celdas += [copiar(c) for c in celdas_calculadora[1:]]
    return celdas


def celda_que_define(celdas, nombre):
    """La celda que asigna la variable nombre (los datos de un ejemplo)."""
    for celda in celdas:
        for nodo in ast.parse(celda.source).body:
            if isinstance(nodo, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == nombre for t in nodo.targets
            ):
                return celda
    raise ValueError(f"ninguna celda acumulable define {nombre}")


def notebook_validacion(acumuladas, anexo):
    """Celdas del notebook de la validación con OpenSees (anexo D): la
    instalación de OpenSees, el motor de la calculadora, los datos de los
    ejemplos B y C y las celdas "validacion" del anexo."""
    celdas_anexo = leer_celdas(anexo, exigir_etiquetas=False)
    introduccion = next(c for c in celdas_anexo if c.cell_type == "markdown")
    instalar = nbformat.v4.new_code_cell(
        "# OpenSees no viene instalado en Colab\n%pip install -q openseespy",
        metadata={"tags": ["instalar"]},
    )
    celda_motor = nbformat.v4.new_code_cell(
        "# @title Motor de la calculadora (ejecutar primero)\n" + motor(acumuladas),
        metadata={"cellView": "form"},
    )
    celdas = [
        copiar(introduccion),
        instalar,
        nbformat.v4.new_markdown_cell("## 1. Motor de la calculadora"),
        celda_motor,
        nbformat.v4.new_markdown_cell("## 2. Los ejemplos B y C"),
        copiar(celda_que_define(acumuladas, "nodos_b")),
        copiar(celda_que_define(acumuladas, "nodos_c")),
        nbformat.v4.new_markdown_cell("## 3. El análisis con OpenSees y la comparación"),
    ]
    celdas += [
        copiar(c)
        for c in celdas_anexo
        if "validacion" in c.metadata.get("tags", [])
    ]
    return celdas


def generar(codigo=CODIGO, destino=NOTEBOOKS):
    """Genera todos los notebooks y devuelve la lista de archivos escritos."""
    destino.mkdir(parents=True, exist_ok=True)
    escritos = []
    acumuladas = []
    celdas_calculadora = []

    for archivo in archivos_de_capitulos(codigo):
        numero = numero_de_capitulo(archivo)
        celdas = leer_celdas(archivo, exigir_etiquetas=True)
        celdas_calculadora += [
            copiar(c) for c in celdas if "calculadora" in c.metadata.get("tags", [])
        ]
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

    if celdas_calculadora:
        celdas = notebook_calculadora(acumuladas, celdas_calculadora)
        escritos.append(escribir(celdas, destino / "mi_calculadora.ipynb"))
        # El mismo motor como módulo, para trabajar en local (anexo C).
        modulo = destino / "calculadora.py"
        modulo.write_text(
            ENCABEZADO_MODULO + motor(acumuladas) + "\n", encoding="utf-8", newline="\n"
        )
        escritos.append(modulo)

    anexo = codigo / "anexoD_validacion.py"
    if anexo.exists():
        celdas = notebook_validacion(acumuladas, anexo)
        escritos.append(escribir(celdas, destino / "validacion_opensees.ipynb"))
    return escritos


def escribir(celdas, ruta):
    # Saltos de línea de Unix también en Windows, para no generar cambios en git.
    with open(ruta, "w", encoding="utf-8", newline="\n") as archivo:
        nbformat.write(nuevo_notebook(celdas), archivo)
    return ruta


if __name__ == "__main__":
    for ruta in generar():
        print(f"generado: {ruta.relative_to(NOTEBOOKS.parent)}")
