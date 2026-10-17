import sys
from pathlib import Path

import nbformat
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extraer_fragmentos import extraer
from generar_notebooks import generar

CAP01 = """\
# %% [markdown]
# # Capítulo 1

# %% tags=["acumulable"]
# [inicio: area]
area = 0.002
# [fin: area]

# %% tags=["exploracion"]
print(area)
"""

CAP02 = """\
# %% tags=["acumulable"]
rigidez = 2.0e8 * area / 5.0

# %% tags=["exploracion"]
print(rigidez)
"""

SOL02 = """\
# %%
print(rigidez * 2)
"""


@pytest.fixture
def codigo(tmp_path):
    carpeta = tmp_path / "codigo"
    (carpeta / "soluciones").mkdir(parents=True)
    (carpeta / "cap01_uno.py").write_text(CAP01, encoding="utf-8")
    (carpeta / "cap02_dos.py").write_text(CAP02, encoding="utf-8")
    (carpeta / "soluciones" / "cap02_dos.py").write_text(SOL02, encoding="utf-8")
    return carpeta


def fuentes(ruta):
    return [c.source for c in nbformat.read(ruta, as_version=4).cells]


def test_genera_leccion_control_y_soluciones(codigo, tmp_path):
    destino = tmp_path / "notebooks"
    nombres = sorted(r.name for r in generar(codigo, destino))
    assert nombres == [
        "cap01_uno.ipynb",
        "cap02_dos.ipynb",
        "control_cap01.ipynb",
        "control_cap02.ipynb",
        "soluciones_cap02.ipynb",
    ]


def test_leccion_empieza_con_el_estado_previo(codigo, tmp_path):
    destino = tmp_path / "notebooks"
    generar(codigo, destino)
    celdas = fuentes(destino / "cap02_dos.ipynb")
    assert celdas[0].startswith("# @title")
    assert "area = 0.002" in celdas[0]
    assert "print(area)" not in celdas[0]


def test_control_solo_tiene_celdas_acumulables(codigo, tmp_path):
    destino = tmp_path / "notebooks"
    generar(codigo, destino)
    celdas = fuentes(destino / "control_cap02.ipynb")
    assert celdas[1:] == ["area = 0.002", "rigidez = 2.0e8 * area / 5.0"]


def test_notebooks_no_muestran_marcas_de_fragmentos(codigo, tmp_path):
    destino = tmp_path / "notebooks"
    generar(codigo, destino)
    assert "[inicio:" not in "".join(fuentes(destino / "cap01_uno.ipynb"))


def test_celda_sin_etiqueta_es_un_error(codigo, tmp_path):
    (codigo / "cap03_tres.py").write_text("# %%\nx = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="etiqueta"):
        generar(codigo, tmp_path / "notebooks")


def test_extrae_fragmentos(codigo, tmp_path):
    destino = tmp_path / "fragmentos"
    assert extraer(codigo, destino) == ["area"]
    assert (destino / "area.py").read_text(encoding="utf-8") == "area = 0.002\n"


def test_fragmento_duplicado_es_un_error(codigo, tmp_path):
    (codigo / "cap03_tres.py").write_text(
        "# [inicio: area]\nx = 1\n# [fin: area]\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="duplicado"):
        extraer(codigo, tmp_path / "fragmentos")
