"""La calculadora y OpenSees deben dar los mismos resultados (anexo D).

Ejecuta las celdas del notebook validacion_opensees.ipynb, que analizan los
ejemplos B y C con ambos programas, y compara todos los desplazamientos,
reacciones y fuerzas. Comprueba además que las tablas del anexo D muestran
los mismos valores en las dos columnas.
"""

import contextlib
import io
import re
from pathlib import Path

import nbformat
import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent.parent
NOTEBOOK = RAIZ / "notebooks" / "validacion_opensees.ipynb"
VALORES = RAIZ / "recursos" / "valores.tex"
ANEXO = RAIZ / "libro" / "anexos" / "anexoD_validacion.tex"


@pytest.fixture(scope="module")
def analisis():
    """Las variables del notebook de validación, después de ejecutarlo."""
    espacio = {}
    for celda in nbformat.read(NOTEBOOK, as_version=4).cells:
        # La instalación de OpenSees es para Colab: aquí ya está instalado
        if celda.cell_type == "code" and "instalar" not in celda.metadata.get("tags", []):
            with contextlib.redirect_stdout(io.StringIO()):
                exec(celda.source, espacio)  # noqa: S102
    return espacio


@pytest.mark.parametrize("ejemplo", ["b", "c"])
def test_opensees_coincide_con_la_calculadora(analisis, ejemplo):
    calculadora = analisis[f"resultados_{ejemplo}"]
    opensees = analisis[f"opensees_{ejemplo}"]
    np.testing.assert_allclose(opensees["U"], calculadora["U"], rtol=1e-9, atol=1e-12)
    assert opensees["restringidos"] == calculadora["restringidos"]
    np.testing.assert_allclose(opensees["R"], calculadora["R"], rtol=1e-9, atol=1e-9)
    assert opensees["N"].keys() == calculadora["N"].keys()
    for barra, fuerza in calculadora["N"].items():
        assert opensees["N"][barra] == pytest.approx(fuerza, rel=1e-9, abs=1e-9), barra


def test_las_tablas_del_anexo_muestran_los_mismos_valores():
    """Cada \\valoropensees{n} del anexo D se imprime igual que \\valor{n}."""
    patron = r"\\csname valor@([a-z0-9_]+)\\endcsname\{([^}]*)\}"
    valores = dict(re.findall(patron, VALORES.read_text(encoding="utf-8")))
    citados = re.findall(r"\\valoropensees\{([a-z0-9_]+)\}", ANEXO.read_text(encoding="utf-8"))
    assert citados
    distintos = [n for n in citados if valores.get(f"ops_{n}") != valores[n]]
    assert not distintos, f"valores de OpenSees que faltan o difieren: {distintos}"
