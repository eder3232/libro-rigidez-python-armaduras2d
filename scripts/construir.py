"""Reconstruye todo el libro, en orden, a partir de sus fuentes.

1. Fragmentos de código, salidas y gráficos, y notebooks (desde codigo/).
2. Figuras TikZ convertidas a SVG para la web.
3. El libro en PDF (latexmk), que además produce la numeración (.aux).
4. Los capítulos de la web (MDX), generados desde el LaTeX.
5. Los tests (incluida la ejecución de todos los notebooks).
6. El sitio web estático.

Se detiene en el primer paso que falle.

Uso: uv run python scripts/construir.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
PYTHON = [sys.executable]


def programa(nombre):
    """Ruta completa de un programa (en Windows, pnpm es pnpm.cmd)."""
    ruta = shutil.which(nombre)
    if ruta is None:
        sys.exit(f"No se encontró el programa '{nombre}'.")
    return ruta


PASOS = [
    ("Fragmentos de código", PYTHON + ["scripts/extraer_fragmentos.py"], RAIZ),
    ("Salidas y gráficos", PYTHON + ["scripts/generar_salidas.py"], RAIZ),
    ("Notebooks", PYTHON + ["scripts/generar_notebooks.py"], RAIZ),
    ("Figuras TikZ a SVG", PYTHON + ["scripts/generar_figuras.py"], RAIZ),
    ("Libro en PDF", [programa("latexmk"), "-silent", "libro.tex"], RAIZ / "libro"),
    ("Capítulos de la web", PYTHON + ["scripts/latex_a_mdx.py"], RAIZ),
    ("Tests", PYTHON + ["-m", "pytest", "-q"], RAIZ),
    ("Sitio web", [programa("pnpm"), "build"], RAIZ / "web"),
]


def main():
    for numero, (nombre, comando, carpeta) in enumerate(PASOS, 1):
        print(f"[{numero}/{len(PASOS)}] {nombre}...", flush=True)
        resultado = subprocess.run(
            comando,
            cwd=carpeta,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if resultado.returncode != 0:
            print(resultado.stdout[-3000:])
            print(resultado.stderr[-3000:])
            sys.exit(f"Falló el paso: {nombre}")
    print("Todo construido: libro/build/libro.pdf y web/out/")


if __name__ == "__main__":
    main()
