"""Los resultados del programa comercial deben coincidir con los de la
calculadora (anexo D y docs/05-validacion-sap2000.md).

Solo compara las filas de validacion/resultados_sap2000.csv que ya tienen el
valor de SAP2000 anotado; mientras no haya ninguna, no compara nada.
"""

import csv
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
RESULTADOS = RAIZ / "validacion" / "resultados_sap2000.csv"
VALORES = RAIZ / "recursos" / "valores.tex"


def valores_de_la_calculadora():
    patron = r"\\csname valor@([a-z0-9_]+)\\endcsname\{([^}]*)\}"
    return dict(re.findall(patron, VALORES.read_text(encoding="utf-8")))


def test_resultados_comerciales_coinciden_con_la_calculadora():
    calculadora = valores_de_la_calculadora()
    with open(RESULTADOS, encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo))
    diferencias = []
    for fila in filas:
        texto = fila["sap2000"].strip().replace(",", ".")
        if not texto:
            continue
        esperado = calculadora[fila["clave"]]
        decimales = len(esperado.split(".")[1])
        # 1 % del valor, o dos unidades de la última cifra que muestra el libro
        tolerancia = max(0.01 * abs(float(esperado)), 2 * 10**-decimales)
        if abs(float(texto) - float(esperado)) > tolerancia:
            diferencias.append(
                f"{fila['descripcion']}: SAP2000 {texto} {fila['unidad']},"
                f" calculadora {esperado} {fila['unidad']}"
            )
    assert not diferencias, "Resultados que no coinciden:\n" + "\n".join(diferencias)
