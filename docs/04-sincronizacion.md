# Sincronización entre LaTeX, web y notebooks

El libro se publica en LaTeX (PDF), en la web (Next.js) y en notebooks. Este documento define **qué tiene una sola fuente y cómo se genera todo lo demás**.

## Principio

> **Nada se escribe dos veces.** El código, los números, las figuras, la notación y también la prosa tienen una sola fuente; la web y los notebooks se generan a partir de ella (decisión D20).

## Fuentes únicas

| Elemento | Fuente única | Se consume en |
|---|---|---|
| Código Python | `codigo/capNN_*.py` | LaTeX (fragmentos), web (bloques ejecutables), notebooks (generados) |
| Notebooks | generados desde `codigo/` | Colab, descarga desde la web |
| Salidas del código | `recursos/salidas/` (generadas por `scripts/generar_salidas.py`) | LaTeX (`\salida`) y web (`<Salida>`) |
| Números citados en el texto y en las figuras | `recursos/valores.tex`, registrados por las celdas `libro` con `valor_libro(nombre, numero, decimales)` | LaTeX y figuras TikZ (`\valor{nombre}`) y web (el convertidor reemplaza `\valor`) |
| Tablas de resultados | `recursos/` (generadas) | LaTeX y web |
| Gráficos del código | generados al ejecutar el código: `recursos/graficos/` (PDF) y `web/public/graficos/` (SVG) | LaTeX (`\grafico`) y web (`<Grafico>`) |
| Esquemas (TikZ) | `libro/figuras/*.tex`, convertidos a SVG por `scripts/generar_figuras.py` | LaTeX (`\figura`) y web (`<Figura>`) |
| Macros matemáticas | `libro/estilo/notacion.tex` | LaTeX y KaTeX en la web |
| Prosa | `libro/capitulos/*.tex` | web: `web/contenido/*.mdx`, generado por `scripts/latex_a_mdx.py` |
| Soluciones de los ejercicios | `libro/anexos/anexoF_soluciones.tex` | web: plegadas debajo de cada ejercicio (las coloca el convertidor) |

## Código: archivos por capítulo

Cada capítulo tiene un archivo `codigo/capNN_nombre.py` en formato *percent* de Jupytext (celdas separadas por `# %%`). Ejemplo:

```python
# %% [markdown]
# ## Geometría de todas las barras

# %% tags=["acumulable"]
def geometria_barras(nodos, barras):
    """Calcula longitud, coseno y seno de cada barra."""
    ...

# %% tags=["exploracion"]
for numero, barra in barras.items():
    print(numero, barra["nodo_inicial"])
```

Cada celda de código de un capítulo lleva una de estas etiquetas:

- **`acumulable`:** forma parte de la calculadora. Va a los puntos de control de este capítulo y de todos los siguientes.
- **`calculadora`:** forma las secciones Datos y Resultados de `mi_calculadora.ipynb` (capítulo 12). También se acumula.
- **`exploracion`:** ejemplo para aprender la herramienta de Python. Solo aparece en el notebook de su capítulo.
- **`libro`:** registra con `valor_libro(...)` los números que citan el texto y las figuras del libro. No aparece en ningún notebook.

Los anexos con código (`codigo/anexoX_*.py`) se ejecutan después de todos los capítulos, con la calculadora completa, y no generan notebooks. Sus celdas pueden llevar la etiqueta **`error`**: la celda debe fallar, y su salida es el mensaje real de Python (anexo B). Si no falla, la construcción se detiene.

### Fragmentos citados

Para incluir una parte del código en LaTeX o en la web, se marca con comentarios:

```python
# [inicio: rigidez_barra]
...
# [fin: rigidez_barra]
```

El texto referencia el fragmento por nombre (`rigidez_barra`), nunca por número de línea. Un script verifica que todo fragmento referenciado exista.

## Notebooks generados

Por cada capítulo se generan tres notebooks en `notebooks/` (nunca se editan a mano):

| Notebook | Contenido | Uso |
|---|---|---|
| `capNN_nombre.ipynb` | Una celda inicial que carga el estado acumulado de los capítulos anteriores, más todas las celdas del capítulo. | Seguir la lección. |
| `control_capNN.ipynb` | Solo las celdas `acumulable` de los capítulos 1 a NN, en orden. | Punto de control: recuperarse y seguir. |
| `soluciones_capNN.ipynb` | Las soluciones de los ejercicios, generadas desde `codigo/soluciones/capNN_nombre.py`. | Ver cómo se resuelve un ejercicio. |

Las soluciones también son código con una sola fuente: el anexo F del PDF y los bloques plegables de la web toman sus fragmentos de esos mismos archivos, y los tests verifican que den los resultados correctos.

Los enlaces "Abrir en Colab" apuntan a los notebooks publicados en el repositorio de GitHub.

## Prosa: de LaTeX a la web

La prosa se escribe **solo en LaTeX**. `scripts/latex_a_mdx.py` traduce los comandos semánticos del libro a los componentes de la web (ver la tabla de equivalencias en la [plantilla de capítulo](02-plantilla-capitulo.md)) y escribe `web/contenido/capNN_nombre.mdx`. **Los MDX no se editan a mano**: cualquier cambio se hace en el `.tex` y se vuelve a generar.

1. El capítulo se escribe y revisa en LaTeX.
2. Se compila el libro (`latexmk`): el convertidor toma la numeración de figuras, ecuaciones y capítulos de los `.aux`, para que las referencias de la web coincidan con las del PDF.
3. Se genera el MDX. Cada uno registra una huella del contenido del `.tex` del que proviene, para detectar si la web quedó atrás:

   ```js
   export const metadatos = {
     numero: 7,
     titulo: "Ensamblaje de la matriz global",
     sincronizado_con: "3f2a9c1d7e",
   };
   ```

**Contenido exclusivo de un formato:**

- `\soloweb{...}`: aparece solo en la web y se copia tal cual al MDX. Es el lugar de las animaciones interactivas y de cualquier componente propio de la web.
- `\sololibro{...}`: aparece solo en el PDF (por ejemplo, una referencia a un número de página).

El convertidor falla ante cualquier comando o entorno que no conozca, para que nada se pierda en silencio. Si un capítulo necesita un comando nuevo, se define en `armaduras.sty`, en el convertidor y, si corresponde, como componente de la web.

## Nombres de archivo

El identificador `capNN_nombre` (por ejemplo, `cap07_ensamblaje`) es el mismo en las tres carpetas:

```
codigo/cap07_ensamblaje.py
libro/capitulos/cap07_ensamblaje.tex
web/contenido/cap07_ensamblaje.mdx
notebooks/cap07_ensamblaje.ipynb
notebooks/control_cap07.ipynb
codigo/soluciones/cap07_ensamblaje.py
notebooks/soluciones_cap07.ipynb
```

## Verificaciones automáticas

Un único comando (por definir en `scripts/`) ejecuta todas las verificaciones y debe pasar antes de cada commit a `main`:

1. Los tests de `codigo/` pasan.
2. Los notebooks se generan y se ejecutan de principio a fin sin errores.
3. Los recursos (números, tablas, figuras) están actualizados respecto al código.
4. Todo fragmento citado en LaTeX o en la web existe en `codigo/`.
5. Todo capítulo estable en LaTeX existe en la web, y su `sincronizado_con` está al día.
6. Las macros se usan desde el archivo compartido (no hay notación escrita a mano).

## Estado de los capítulos

| Capítulo | LaTeX | Código y tests | Web | Animaciones |
|---|---|---|---|---|
| Prefacio | estable | — (sin código) | generado | — |
| 1. Por qué programar el método de rigidez | estable | — (sin código) | generado | — |
| 2. Nuestro primer notebook | estable (falta: capturas de Colab) | listo | generado | — |
| 3. Describir una armadura | estable | listo | generado | — |
| 4. La geometría de todas las barras | estable | listo | generado | — |
| 5. La rigidez de una barra | estable | listo | generado | — |
| 6. Los grados de libertad | estable | listo | generado | — |
| 7. Ensamblaje de la matriz global | estable | listo | generado | — |
| 8. Cargas y partición del sistema | estable | listo | generado | — |
| 9. Desplazamientos y reacciones | estable | listo | generado | — |
| 10. Fuerzas internas | estable (falta: comparación con software comercial) | listo | generado | — |
| 11. Visualizar los resultados | estable | listo | generado | — |
| 12. Mi calculadora de armaduras | estable | listo | generado | — |
| Anexo A. Referencia rápida de Python y NumPy | estable | — | generado | — |
| Anexo B. Leer un error de Python | borrador | listo (celdas "error") | generado | — |

Estados posibles: `pendiente` → `borrador` → `revisado` → `estable`.

## Tecnologías

| Pieza | Herramienta | Estado |
|---|---|---|
| Python del repositorio | `uv`, Python 3.12 (la versión de Colab), NumPy, Matplotlib, pytest, Jupytext, Ruff | Listo |
| LaTeX | LuaLaTeX + KOMA-Script (`scrbook`) + `minted` + `tcolorbox` + TikZ; tipografías Libertinus y Source Code Pro | Listo (maqueta inicial) |
| Web | Next.js 16 (exportación estática) + MDX + KaTeX, con las mismas tipografías del PDF | Listo (maqueta inicial) |
| Python en la web | Pyodide en un *web worker* | Pendiente |
| Publicación | GitHub Pages o Vercel para la web; el PDF en las *releases* de GitHub | Pendiente |

## Comandos

| Tarea | Comando (desde la raíz) |
|---|---|
| **Reconstruir todo** (código, notebooks, figuras, PDF, web y tests) | `uv run python scripts/construir.py` |
| Tests y verificación del código | `uv run pytest` |
| Extraer los fragmentos | `uv run python scripts/extraer_fragmentos.py` |
| Generar las salidas | `uv run python scripts/generar_salidas.py` |
| Generar los notebooks | `uv run python scripts/generar_notebooks.py` |
| Convertir las figuras TikZ a SVG | `uv run python scripts/generar_figuras.py` |
| Generar la web de un capítulo | `uv run python scripts/latex_a_mdx.py cap04_geometria` (después de compilar el libro) |
| Compilar el libro | `cd libro && latexmk libro.tex` (PDF en `libro/build/`) |
| Compilar la muestra tipográfica | `cd libro && latexmk muestra.tex` |
| Web en desarrollo | `cd web && pnpm dev` |
| Web estática | `cd web && pnpm build` (sitio en `web/out/`) |
