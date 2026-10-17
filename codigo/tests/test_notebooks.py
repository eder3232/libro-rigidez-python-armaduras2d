"""Todo notebook generado debe ejecutarse de principio a fin sin errores."""

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
    NotebookClient(notebook, timeout=120, kernel_name="python3").execute()
