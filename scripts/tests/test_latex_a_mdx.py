import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from latex_a_mdx import Convertidor, ErrorDeConversion

ETIQUETAS = {"fig:ejemplo": "3.1", "cap:geometria": "4", "eq:proyecciones": "2.1"}


def convertir(texto):
    convertidor = Convertidor(
        "3", ETIQUETAS, {"3.1": "Respuesta."}, {"cap:geometria": "cap04_geometria"}
    )
    return convertidor.bloques(texto).strip()


def test_comandos_en_linea():
    assert convertir(r"\emph{a} y \py{x = {1}}") == "*a* y `x = {1}`"
    assert convertir(r"\termino{bucle}{loop}") == "*bucle* (*loop*)"


def test_unidades_en_texto_y_en_matematica():
    assert convertir(r"\SI{20}{\centi\metre\squared}") == "20\u00a0cm²"
    assert convertir(r"$E = \SI{200}{\giga\pascal}$") == r"$E = 200\,\mathrm{GPa}$"
    assert convertir(r"\SI{400000}{\kilo\newton}") == "400\u202f000\u00a0kN"


def test_referencias_usan_la_numeracion_del_libro():
    assert convertir(r"la \cref{fig:ejemplo}") == "la figura\u00a03.1"
    resultado = convertir(r"el \cref{cap:geometria}")
    assert resultado == "el [capítulo\u00a04](/capitulos/cap04_geometria)"


def test_secciones_numeradas():
    resultado = convertir(r"\section{Listas}\label{sec:listas} texto")
    assert resultado.startswith("## 3.1 Listas")


def test_ejercicio_incluye_su_solucion():
    resultado = convertir(r"\begin{ejercicio}{3.1}Calcular.\end{ejercicio}")
    assert '<Ejercicio numero="3.1">' in resultado
    assert "<SolucionDelEjercicio>\n\nRespuesta." in resultado


def test_solo_web_y_solo_libro():
    assert convertir(r"\sololibro{impreso}\soloweb{<Animacion />}") == "<Animacion />"


def test_comando_desconocido_es_un_error():
    with pytest.raises(ErrorDeConversion, match="desconocido"):
        convertir(r"\inventado{x}")


def test_cita_textual_usa_la_bibliografia():
    assert convertir(r"\textcite[cap.~3]{kassimali2012}") == (
        "Kassimali (2012, cap.\u00a03)"
    )
    assert convertir(r"\textcite{mcguire2000}") == "McGuire et al. (2000)"


def test_align_numera_cada_linea():
    etiquetas = {"eq:a": "8.1", "eq:b": "8.2"}
    convertidor = Convertidor("8", etiquetas, {}, {})
    resultado = convertidor.bloques(
        r"\begin{align} x &= 1 \label{eq:a}\\ y &= 2 \label{eq:b} \end{align}"
    )
    assert r"x = 1 \tag{8.1}" in resultado
    assert r"y = 2 \tag{8.2}" in resultado
