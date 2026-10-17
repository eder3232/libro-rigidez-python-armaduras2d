from pathlib import Path

CODIGO = Path(__file__).resolve().parent.parent


def test_cada_solucion_corresponde_a_un_capitulo():
    capitulos = {a.name for a in CODIGO.glob("cap*.py")}
    for solucion in (CODIGO / "soluciones").glob("cap*.py"):
        assert solucion.name in capitulos, f"{solucion.name} no tiene capítulo"
