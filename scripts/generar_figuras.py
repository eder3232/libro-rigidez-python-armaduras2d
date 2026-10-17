"""Convierte las figuras TikZ de libro/figuras/ a SVG para la web.

Cada figura se compila de forma independiente con la misma base de estilo del
libro (libro/estilo/base.sty) y se convierte a SVG con dvisvgm, con el texto
transformado en trazos para que se vea idéntico sin depender de las fuentes.
Solo se regeneran las figuras cuyo .tex es más nuevo que su .svg.

Uso: uv run python scripts/generar_figuras.py [--todas]
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comun import RAIZ

LIBRO = RAIZ / "libro"
FIGURAS = LIBRO / "figuras"
TEMPORAL = LIBRO / "build" / "figuras"
DESTINO = RAIZ / "web" / "public" / "figuras"

PLANTILLA = r"""\documentclass[border=4pt]{standalone}
\usepackage{estilo/base}
\begin{document}
\figura{%s}
\end{document}
"""


def convertir(nombre):
    """Compila una figura a DVI y la convierte a SVG."""
    TEMPORAL.mkdir(parents=True, exist_ok=True)
    # Un nombre distinto al de la figura: si coincidiera, el \input del libro
    # (que también busca en build/) encontraría este documento independiente.
    independiente = f"independiente_{nombre}"
    fuente = TEMPORAL / f"{independiente}.tex"
    fuente.write_text(PLANTILLA % nombre, encoding="utf-8")
    compilacion = subprocess.run(
        [
            "lualatex",
            "--output-format=dvi",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={TEMPORAL}",
            str(fuente),
        ],
        cwd=LIBRO,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if compilacion.returncode != 0:
        raise RuntimeError(
            f"Error al compilar la figura '{nombre}':\n{compilacion.stdout[-2000:]}"
        )
    subprocess.run(
        [
            "dvisvgm",
            "--no-fonts",
            "--exact-bbox",
            "-o",
            str(DESTINO / f"{nombre}.svg"),
            str(TEMPORAL / f"{independiente}.dvi"),
        ],
        check=True,
        capture_output=True,
    )


def generar(todas=False):
    """Convierte las figuras nuevas o modificadas y devuelve sus nombres."""
    DESTINO.mkdir(parents=True, exist_ok=True)
    nombres = sorted(f.stem for f in FIGURAS.glob("*.tex"))
    for viejo in DESTINO.glob("*.svg"):
        if viejo.stem not in nombres:
            viejo.unlink()
    convertidas = []
    for nombre in nombres:
        svg = DESTINO / f"{nombre}.svg"
        tex = FIGURAS / f"{nombre}.tex"
        if todas or not svg.exists() or tex.stat().st_mtime > svg.stat().st_mtime:
            convertir(nombre)
            convertidas.append(nombre)
    return convertidas


if __name__ == "__main__":
    convertidas = generar(todas="--todas" in sys.argv)
    print(f"{len(convertidas)} figuras convertidas: {', '.join(convertidas)}")
