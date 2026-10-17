# Sincronización entre LaTeX, web y notebooks

El libro se publica en dos formatos escritos a mano (LaTeX y Next.js) más notebooks generados. Este documento define **qué tiene una sola fuente, qué se duplica y cómo se controla**.

## Principio

> Lo que es peligroso desincronizar (código, números, figuras, notación) **nunca se escribe dos veces**. Solo la prosa se duplica, y siempre en una dirección: de LaTeX a la web.

## Fuentes únicas

| Elemento | Fuente única | Se consume en |
|---|---|---|
| Código Python | `codigo/capNN_*.py` | LaTeX (fragmentos), web (bloques ejecutables), notebooks (generados) |
| Notebooks | generados desde `codigo/` | Colab, descarga desde la web |
| Números citados en el texto | `recursos/` (generados por scripts que ejecutan el código) | LaTeX (`.tex`) y web (`.json`) |
| Tablas de resultados | `recursos/` (generadas) | LaTeX y web |
| Figuras con datos | `recursos/` (generadas: PDF para LaTeX, SVG para la web) | LaTeX y web |
| Macros matemáticas | `libro/estilo/notacion.tex` | LaTeX y KaTeX en la web |
| Prosa | `libro/` (LaTeX, canónica) | adaptada a mano en `web/` |

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

Cada celda de código lleva una de dos etiquetas:

- **`acumulable`:** forma parte de la calculadora. Va a los puntos de control de este capítulo y de todos los siguientes.
- **`exploracion`:** ejemplo para aprender la herramienta de Python. Solo aparece en el notebook de su capítulo.

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

1. El capítulo se escribe y revisa en LaTeX.
2. Cuando se marca como **estable**, se adapta a MDX en `web/`.
3. La adaptación puede **agregar** lo que el papel no puede dar (animaciones, código ejecutable, soluciones plegables) y **reformular** para pantalla, pero **no puede cambiar el contenido técnico**. Si al adaptar se descubre un error, se corrige primero en LaTeX.
4. Cada archivo MDX registra en su cabecera el commit de LaTeX con el que se sincronizó:

   ```yaml
   ---
   capitulo: 7
   sincronizado_con: a1b2c3d
   ---
   ```

   Un script compara ese commit con el último cambio del `.tex` correspondiente y avisa si la web quedó atrás.

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
| (sin capítulos todavía) | | | | |

Estados posibles: `pendiente` → `borrador` → `revisado` → `estable`.

## Tecnologías (propuestas, a confirmar al armar el andamiaje)

| Pieza | Herramienta |
|---|---|
| Python del repositorio | `uv`, Python ≥ 3.12, NumPy, Matplotlib, pytest, Jupytext |
| LaTeX | LuaLaTeX + `minted` para el código |
| Web | Next.js (exportación estática) + MDX + KaTeX + Pyodide en un *web worker* |
| Publicación | GitHub Pages o Vercel para la web; el PDF en las *releases* de GitHub |
