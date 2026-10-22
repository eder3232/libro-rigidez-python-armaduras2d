"""Todo notebook generado debe ejecutarse de principio a fin sin errores, y
el módulo calculadora.py debe poder importarse y analizar una armadura."""

import importlib.util
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

NOTEBOOKS = Path(__file__).resolve().parent.parent.parent / "notebooks"


@pytest.mark.parametrize(
    "ruta", sorted(NOTEBOOKS.glob("*.ipynb")), ids=lambda ruta: ruta.name
)
def test_notebook_se_ejecuta(ruta):
    notebook = nbformat.read(ruta, as_version=4)
    # La instalación de OpenSees es para Colab: aquí ya está instalado
    notebook.cells = [
        c for c in notebook.cells if "instalar" not in c.metadata.get("tags", [])
    ]
    NotebookClient(notebook, timeout=120, kernel_name="python3").execute()


def test_modulo_calculadora_analiza_el_ejemplo_a():
    especificacion = importlib.util.spec_from_file_location(
        "calculadora", NOTEBOOKS / "calculadora.py"
    )
    calculadora = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(calculadora)

    def barra(i, j):
        return {"nodo_inicial": i, "nodo_final": j, "elasticidad": 2.0e8, "area": 0.0020}

    nodos = {1: {"x": 0.0, "y": 0.0}, 2: {"x": 6.0, "y": 0.0}, 3: {"x": 3.0, "y": 4.0}}
    barras = {1: barra(1, 2), 2: barra(2, 3), 3: barra(1, 3)}
    apoyos = {1: {"x": True, "y": True}, 2: {"x": False, "y": True}}
    cargas = {3: {"x": 20.0, "y": -50.0}}
    resultados = calculadora.analizar_armadura(nodos, barras, apoyos, cargas)
    assert resultados["N"][1] == pytest.approx(28.75)
    assert resultados["N"][2] == pytest.approx(-47.9167, rel=1e-4)
