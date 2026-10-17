# Índice detallado

Cada capítulo indica: qué parte de la calculadora se construye, el **Python nuevo** que se aprende ahí, cómo se **verifica** y qué **animaciones interactivas** podría tener la web. Las animaciones son ideas; se priorizan después.

## Ejemplos que recorren el libro

Se usan tres armaduras distintas a propósito: con un solo ejemplo, los errores de índices pueden quedar ocultos (ver [lecciones del proyecto anterior](00-vision-y-decisiones.md#lecciones-del-proyecto-anterior)).

| Ejemplo | Descripción | Para qué |
|---|---|---|
| **A. Triángulo** | 3 nodos, 3 barras, isostático. Nodo 1 articulado, nodo 2 con rodillo, carga en el nodo 3. 3 grados libres y 3 restringidos. | Verificar cada paso **a mano** (método de los nudos). Es el ejemplo de los primeros capítulos. |
| **B. Cuadro arriostrado** | 4 nodos, 6 barras, hiperestático. Nodo 1 articulado, nodo 2 con rodillo: 5 grados libres y 3 restringidos. | Mostrar que el método resuelve lo que el método de los nudos no puede. Se verifica con software comercial. |
| **C. Armadura Pratt** | Armadura de cubierta o de puente peatonal de 6 paneles. | El caso "real" del capítulo final: el estudiante ve su calculadora resolver algo grande. |

### Datos propuestos (decisión D13)

Todos en acero estructural, $E = 200\ \text{GPa} = 2.0\times10^{8}\ \text{kN/m}^2$, con áreas del orden de perfiles reales (ángulos dobles, tubos) y cargas de servicio típicas. Al escribir cada ejemplo se verifica que los esfuerzos queden por debajo de la fluencia (por ejemplo, $f_y = 250$ MPa) y se comentan los órdenes de magnitud con el lector.

| Ejemplo | Geometría | Área | Cargas |
|---|---|---|---|
| A | Base de 6 m, altura de 4 m (triángulos 3-4-5, cómodos para calcular a mano) | 20 cm² | Nodo superior: 20 kN horizontal, 50 kN hacia abajo |
| B | 3 m de ancho, 4 m de alto (diagonales de 5 m) | 20 cm² | Nodos superiores: 30 kN horizontal y 40 kN hacia abajo en cada uno |
| C | Luz de 18 m en 6 paneles de 3 m, altura de 3 m | Cordones y diagonales con áreas distintas | Cargas de cubierta en los nudos del cordón superior |

Prueba preliminar con los datos de A: desplazamientos de 0.4 a 0.7 mm y esfuerzos de 7 a 24 MPa. Son valores realistas y sirven para comentar que los desplazamientos de una armadura son pequeños, y por eso la deformada se dibuja con un factor de escala.

**Nota sobre B:** con los dos apoyos articulados (como en el proyecto anterior), la barra entre los apoyos queda con fuerza cero, lo que distrae. Por eso se propone un rodillo en el nodo 2. Además, así B tiene una cantidad de grados libres y restringidos distinta de la de A, lo que ayuda a detectar errores de índices.

**Pandeo:** el libro calcula fuerzas axiales, no diseña. En el capítulo 10 una caja advierte que las barras en compresión deben verificarse además por pandeo.

---

## Prefacio: cómo usar este libro

- A quién va dirigido y qué se necesita saber.
- Los tres formatos (PDF, web, notebooks) y cuándo usar cada uno.
- El flujo de trabajo recomendado: tu notebook en Google Drive + Colab.
- Cómo retomar si se omitió una parte: los puntos de control.
- Nota sobre vocabulario: "armadura" y su equivalente "cercha".
- Convenciones tipográficas (cajas, código, notación).

## Parte I. Primeros pasos

### Capítulo 1. Por qué programar el método de rigidez

- **Construimos:** nada todavía. Se muestra el resultado final: la calculadora analizando el ejemplo C, con su deformada y sus fuerzas axiales.
- **Contenido:** los límites del cálculo a mano; qué hacen por dentro los programas comerciales; recorrido del método completo en un diagrama de flujo, que servirá de mapa para todo el libro.
- **Python nuevo:** ninguno.
- **Animación:** el diagrama de flujo del método, donde cada paso enlaza al capítulo correspondiente.

### Capítulo 2. Nuestro primer notebook

- **Construimos:** la geometría de **una** barra: longitud, coseno y seno.
- **Python nuevo:** crear un notebook en Drive y abrirlo con Colab; celdas de código y de texto; ejecutar; variables; operaciones aritméticas; `import math`; `print` y f-strings.
- **Verificación:** comparar con la calculadora de mano.
- **Animación:** una barra con sus extremos arrastrables; la longitud, el ángulo, el coseno y el seno se actualizan en vivo.

## Parte II. Del modelo a la matriz

### Capítulo 3. Describir una armadura

- **Construimos:** el modelo de datos del ejemplo A: nodos, barras, apoyos y cargas.
- **Python nuevo:** listas; diccionarios; diccionarios anidados; acceso por clave; un primer gráfico mínimo con Matplotlib para **ver** la armadura.
- **Verificación:** el dibujo coincide con el croquis del problema.
- **Animación:** el diccionario de datos y el dibujo, uno al lado del otro; al pasar el cursor por una entrada del diccionario se resalta el nodo o la barra.

### Capítulo 4. La geometría de todas las barras

- **Construimos:** longitud, coseno y seno de cada barra.
- **Python nuevo:** bucles `for`; `.items()`; acumular resultados en un diccionario nuevo (sin modificar los datos de entrada, y por qué importa).
- **Verificación:** tabla de geometría contra el cálculo a mano del ejemplo A; aplicar al ejemplo B.

### Capítulo 5. La rigidez de una barra

- **Construimos:** la matriz de rigidez de una barra en coordenadas locales (2×2), la matriz de transformación y la matriz en coordenadas globales (4×4).
- **Python nuevo:** funciones (`def`, parámetros, `return`, docstrings); arreglos de NumPy; producto matricial `@`; transpuesta `.T`.
- **Verificación:** simetría (`np.allclose`); la matriz es singular por sí sola (movimiento de cuerpo rígido); casos de barra horizontal y vertical a mano.
- **Animación:** rotar una barra y ver cómo cambian los 16 términos de su matriz global.

### Capítulo 6. Los grados de libertad

- **Construimos:** la numeración de grados de libertad y las listas de grados libres y restringidos.
- **Python nuevo:** `enumerate`; condicionales `if`/`else`; construir listas con `.append`; **por qué Python cuenta desde 0** y la única función del libro que traduce la numeración desde 1 a los índices de Python (decisión D11).
- **Verificación:** conteo de grados de libertad y de reacciones; chequeo previo de estabilidad (2·nodos frente a barras + reacciones).
- **Caja:** la convención de renumerar primero los grados libres (como en Kassimali) y por qué el libro usa la numeración natural.
- **Animación:** la armadura con sus grados de libertad numerados; los libres y los restringidos en colores distintos.

### Capítulo 7. Ensamblaje de la matriz global

- **Construimos:** la matriz de rigidez global.
- **Python nuevo:** `np.zeros`; indexación de matrices; `np.ix_`; el operador `+=`; `np.set_printoptions` y una función para imprimir matrices con sus grados de libertad numerados desde 1.
- **Verificación:** simetría; la matriz es singular antes de aplicar los apoyos; ensamblaje a mano del ejemplo A.
- **Animación (central del libro):** la matriz 4×4 de cada barra se "reparte" casilla por casilla en la matriz global, barra por barra.

## Parte III. Resolver y entender

### Capítulo 8. Cargas y partición del sistema

- **Construimos:** el vector de cargas y las submatrices (libre-libre, libre-restringido, etc.).
- **Python nuevo:** *slicing*; indexar con listas de índices; repaso de `np.ix_`.
- **Verificación:** dimensiones de cada submatriz; la submatriz libre-libre ya no es singular.
- **Animación:** la matriz global reordenándose en sus cuatro bloques.

### Capítulo 9. Desplazamientos y reacciones

- **Construimos:** la solución del sistema y las reacciones.
- **Python nuevo:** `np.linalg.solve`; por qué no `np.linalg.inv` (costo y precisión); errores numéricos y tolerancias.
- **Verificación:** equilibrio global (cargas + reacciones = 0); ejemplo A contra el cálculo a mano.

### Capítulo 10. Fuerzas internas

- **Construimos:** la fuerza axial de cada barra, con su clasificación en tracción o compresión.
- **Python nuevo:** combinar todo lo anterior; escribir la función `mostrar_tabla` (f-strings con ancho y decimales) para presentar resultados con encabezados y numeración desde 1 (decisión D14).
- **Verificación:** ejemplo A contra el método de los nudos; ejemplo B contra software comercial (SAP2000 o Ftool); esfuerzos frente a la fluencia.
- **Caja:** las barras en compresión deben verificarse además por pandeo (fuera del alcance del libro).

### Capítulo 11. Visualizar los resultados

- **Construimos:** el dibujo de la deformada (con factor de escala) y el diagrama de fuerzas axiales en colores.
- **Python nuevo:** Matplotlib en más detalle: líneas, colores, anotaciones, leyendas, ejes iguales.
- **Animación:** un control deslizante para el factor de escala de la deformada.

### Capítulo 12. Mi calculadora de armaduras

- **Construimos:** el notebook final, organizado en **Motor**, **Datos** y **Resultados**; una función `analizar_armadura(modelo)` que hace todo el proceso.
- **Python nuevo:** organizar el código; funciones que llaman a funciones; devolver varios resultados.
- **Verificación:** el ejemplo C completo; los ejemplos A y B dan los mismos resultados que en los capítulos anteriores.
- **Cierre:** cómo analizar tu propia armadura, una lista de errores típicos (unidades, apoyos insuficientes, nodos sin conectar) y qué hacer en cada caso.

## Parte IV. Extensiones (fase 2)

13. **Asentamientos de apoyo:** desplazamientos prescritos distintos de cero.
14. **Cambios de temperatura y errores de fabricación:** fuerzas equivalentes en los nodos.
15. **Apoyos inclinados:** rotación de los grados de libertad de un nodo.
16. **Estabilidad:** detectar mecanismos con el rango de la matriz y el número de condición.
17. **Armaduras grandes:** generar la geometría con código; matrices dispersas (`scipy.sparse`).
18. **Hacia dónde seguir:** pórticos, armaduras 3D, elementos finitos.

## Anexos

- **A. Referencia rápida de Python y NumPy:** para consultar, no para estudiar de corrido.
- **B. Leer un error de Python:** cómo interpretar un *traceback* y los errores más frecuentes del libro.
- **C. Trabajar en local (opcional):** instalar Python; el problema de los entornos (Anaconda frente a pip) explicado; el código como módulo `.py`.
- **D. Validación con software comercial:** cómo se modelaron los ejemplos en SAP2000 o Ftool.
- **E. Notación y convenciones de signos.**
- **F. Soluciones de los ejercicios.** También están plegadas en cada capítulo de la web y en un notebook de soluciones por capítulo (decisión D15).
