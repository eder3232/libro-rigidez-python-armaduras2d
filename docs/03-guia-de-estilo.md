# Guía de estilo

## Redacción

- **Texto universitario de gama alta**: riguroso y preciso, pero cercano. La referencia es un buen libro de texto, no un tutorial de internet ni un tratado.
- **Español neutro**, comprensible en toda Hispanoamérica y España. Se evitan regionalismos. "Armadura" es el término del libro; el prefacio menciona su equivalente "cercha".
- **Registro (decisión D19):** primera persona del plural como voz principal ("ahora ensamblamos la matriz", "observemos que..."), que es lo habitual en los textos universitarios en español y acompaña al lector sin tutearlo. En los enunciados de los ejercicios, infinitivo ("Calcular las reacciones..."). Nunca se mezclan registros dentro de un capítulo.
- **Frases cortas.** Una idea por párrafo.
- **Términos técnicos:** en español, con el término en inglés entre paréntesis y en cursiva **solo la primera vez**, para que el lector pueda buscar documentación. Ejemplo: grados de libertad (*degrees of freedom*).
- **Sin relleno.** Si un párrafo no ayuda a construir la calculadora o a entenderla, se elimina.
- **Nunca** "simplemente", "obviamente" o "es fácil ver que": lo que es obvio para el autor no lo es para quien recién programa.

## Notación matemática

| Símbolo | Significado |
|---|---|
| $E$, $A$, $L$ | Módulo de elasticidad, área de la sección, longitud de la barra. |
| $c = \cos\theta$, $s = \sin\theta$ | Cosenos directores de la barra, con $\theta$ medido desde el eje $x$ global, del nodo inicial al nodo final. |
| $\mathbf{k}'$ | Matriz de rigidez de la barra en coordenadas locales (2×2): $\mathbf{k}' = \frac{EA}{L}\begin{bmatrix}1 & -1\\ -1 & 1\end{bmatrix}$. |
| $\mathbf{T}$ | Matriz de transformación (2×4): $\mathbf{T} = \begin{bmatrix}c & s & 0 & 0\\ 0 & 0 & c & s\end{bmatrix}$, tal que $\mathbf{u}' = \mathbf{T}\,\mathbf{u}$. |
| $\mathbf{k}$ | Matriz de rigidez de la barra en coordenadas globales (4×4): $\mathbf{k} = \mathbf{T}^\mathsf{T}\mathbf{k}'\mathbf{T}$. |
| $\mathbf{K}$ | Matriz de rigidez global. |
| $\mathbf{F}$, $\mathbf{U}$ | Vectores globales de fuerzas y desplazamientos. |
| subíndices $l$, $r$ | Grados de libertad libres y restringidos: $\mathbf{K}_{ll}$, $\mathbf{K}_{lr}$, $\mathbf{U}_l$, $\mathbf{F}_r$, etc. |
| $N$ | Fuerza axial de una barra: **positiva en tracción**, negativa en compresión. |

- Matrices y vectores en **negrita**; escalares en cursiva.
- Las macros de LaTeX para esta notación viven en un único archivo compartido con la web (ver [sincronización](04-sincronizacion.md)). No se escribe `\mathbf{K}` a mano: se usa la macro.

## Convenciones del modelo

- Ejes globales: $x$ hacia la derecha, $y$ hacia arriba.
- Cargas positivas en el sentido positivo de los ejes.
- **Unidades:** kN y m en todo el libro; por lo tanto $E$ en kN/m² (kPa) y $A$ en m². Cada ejemplo indica sus unidades en la sección de datos. No se mezclan unidades dentro de un ejemplo. Al presentar resultados se usan las unidades más legibles (desplazamientos en mm, esfuerzos en MPa), indicando siempre la conversión.
- **Materiales y cargas realistas** (decisión D13): acero con $E = 200$ GPa, áreas de perfiles reales, cargas de servicio típicas.

### Numeración desde 1 (decisión D11)

- Nodos, barras y grados de libertad se numeran **desde 1** en el texto, las figuras, el código del modelo y toda salida impresa.
- Grados de libertad del nodo $i$: $2i-1$ (dirección $x$) y $2i$ (dirección $y$).
- Las matrices y vectores impresos muestran encabezados con los grados de libertad desde 1.
- Los arreglos de NumPy, por dentro, empiezan en 0. La conversión (restar 1) se hace en **una sola función** de la calculadora, presentada en el capítulo 6. En ningún otro lugar aparece un `- 1` ni un `+ 1` para traducir numeraciones.

## Código

### Idioma de los nombres

- Todos los nombres propios del libro (variables, funciones, claves de diccionarios) **en español**.
- **Sin tildes ni ñ en los nombres** (`longitud`, `anio`, `matriz_global`). Python los acepta, pero causan problemas con teclados, búsquedas y algunas herramientas. Los comentarios y textos sí llevan tildes.
- En inglés solo lo inevitable: palabras clave de Python y la API de las bibliotecas (`np.linalg.solve`).

### Estilo

- Formato según PEP 8 (se aplicará un formateador automático).
- Nombres en `minusculas_con_guiones_bajos`.
- Los símbolos de las fórmulas pueden usarse como variables locales cuando hacen el código más parecido a la ecuación (`E`, `A`, `L`, `c`, `s`, `k_local`). Fuera de una función, nombres descriptivos.
- Comentarios para explicar el *porqué*, no para repetir lo que dice el código.
- Docstrings breves en español en todas las funciones de la calculadora.

### Reglas técnicas

- Solo biblioteca estándar, NumPy y Matplotlib (decisión D10). Nada que requiera `pip install` en Colab.
- El código debe ejecutarse igual en Colab y en Pyodide.
- Los arreglos numéricos son siempre de NumPy; nada de convertir a listas (`.tolist()`) para operar.
- Los vectores y matrices contienen **solo números**. Lo simbólico (nombres de incógnitas) se muestra en la prosa o en las figuras, no dentro de los arreglos.
- Los datos de entrada no se modifican: los resultados se guardan en estructuras nuevas.
- Nada de `print` de depuración en el código del libro: cada salida que aparece está ahí porque el texto la comenta.
- **Ancho máximo de 58 caracteres por línea** en el código que aparece en el libro, para que quepa en la página impresa sin cortes. `scripts/extraer_fragmentos.py` lo verifica y falla si una línea es más larga. Los diccionarios de datos largos se escriben en varias líneas.
- Las salidas que muestra el libro se generan ejecutando el código (`scripts/generar_salidas.py`); nunca se copian a mano.

### Modelo de datos (propuesta, a confirmar en la revisión)

Ejemplo A (unidades: kN, m):

```python
nodos = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 6.0, "y": 0.0},
    3: {"x": 3.0, "y": 4.0},
}

barras = {
    1: {"nodo_inicial": 1, "nodo_final": 2, "elasticidad": 2.0e8, "area": 0.0020},
    2: {"nodo_inicial": 2, "nodo_final": 3, "elasticidad": 2.0e8, "area": 0.0020},
    3: {"nodo_inicial": 1, "nodo_final": 3, "elasticidad": 2.0e8, "area": 0.0020},
}

apoyos = {
    1: {"x": True, "y": True},   # articulado
    2: {"x": False, "y": True},  # rodillo
}

cargas = {
    3: {"x": 20.0, "y": -50.0},
}
```

Separar apoyos y cargas de los nodos hace que cada diccionario tenga una sola responsabilidad y que los nodos sin apoyo ni carga no necesiten entradas vacías.

### Presentación de resultados (decisión D14)

- Matrices: `np.set_printoptions` con precisión y sin notación científica innecesaria, más una función propia que imprime la matriz con encabezados de grados de libertad desde 1.
- Tablas: una función propia `mostrar_tabla`, construida en el capítulo 10 con f-strings, con columnas alineadas, unidades en los encabezados y numeración desde 1.
- Gráficos: Matplotlib, con la paleta del libro.

## Figuras

- Todas las figuras con datos se generan por código (ver [sincronización](04-sincronizacion.md)); nada de capturas de pantalla de resultados.
- **Esquemas estructurales** (barras, apoyos, cargas, ejes, grados de libertad): con TikZ, con una biblioteca propia de símbolos (apoyo articulado, rodillo, flecha de carga, numeración de nodos) para que todos los esquemas del libro sean idénticos en estilo.
- **Gráficos de resultados**: Matplotlib con el *backend* PGF, para que usen exactamente la tipografía y los tamaños del libro.
- Paleta única para todo el libro: tracción y compresión con colores distinguibles también para personas con daltonismo, más un color neutro para la geometría sin deformar.

## Diseño editorial (maqueta propia)

**Referencia de diseño:** el libro favorito del autor, *Mecánica vectorial para ingenieros: Dinámica* de Beer y Johnston (McGraw-Hill, 10.ª edición, a todo color). De esa tradición tomamos:

- **Problemas resueltos** destacados, con banda de título a color, enunciado, solución y verificación.
- **Estrategias de resolución**: cómo abordar un tipo de problema, paso a paso.
- **Ecuaciones clave** resaltadas con fondo de color.
- **Repaso y resumen** al final de cada capítulo.
- **Ejercicios numerados** por capítulo, con sus soluciones al final del libro.
- Uso generoso pero ordenado del color y de las figuras.

Lo que distingue a un libro de gama alta está en los detalles. La maqueta propia debe cuidar:

- **Tipografía:** una familia con versiones de texto, matemática y código que combinen bien (por definir al armar la plantilla), con kerning, ligaduras y microtipografía (`microtype`).
- **Retícula y márgenes amplios**, con notas al margen para comentarios breves, referencias cruzadas y pequeñas figuras.
- **Color con moderación:** un color principal y uno de acento, usados de forma consistente (cajas, títulos, resaltado de código).
- **Aperturas de capítulo cuidadas:** número, título, objetivos de aprendizaje y una figura.
- **Código bien compuesto:** resaltado de sintaxis sobrio, numeración de líneas solo cuando el texto se refiere a ellas, sin cortes de bloque entre páginas cuando se pueda evitar.
- **Aparato académico completo:** ecuaciones numeradas por capítulo, referencias cruzadas, bibliografía (BibLaTeX), índice alfabético, glosario de términos y lista de símbolos.
- **Revisión tipográfica final:** viudas y huérfanas, figuras cerca de su primera mención, partición de palabras en español.

La maqueta se implementa por completo con **comandos semánticos**: el texto usa comandos propios (`\recuerda{...}`, `\fragmento{rigidez_barra}`, `\matriz{K}`) y nunca formato directo (negritas sueltas, colores, tamaños). Así, cambiar el diseño es cambiar las definiciones de esos comandos, sin tocar el texto.
