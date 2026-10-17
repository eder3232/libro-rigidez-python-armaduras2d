# Visión y decisiones

## Propósito

Que un estudiante de 4.º año de Ingeniería Civil, que ya conoce (o está aprendiendo) el método de rigidez, termine el libro con **su propia calculadora de armaduras 2D funcionando**, escrita por él, y entendiendo cada línea.

El libro **no** enseña el método de rigidez desde cero: lo *recuerda* con precisión y se concentra en lo nuevo para el lector, que es convertir el método en un programa correcto y verificable.

## Público

- Estudiantes de 4.º año de Ingeniería Civil, con conocimientos de análisis estructural.
- Sin experiencia en programación, o con muy poca.
- Sin experiencia en terminal, entornos de Python ni gestores de paquetes. **Esto es una restricción de diseño, no un detalle**: cualquier paso de instalación es un punto de abandono.
- Hispanohablantes.

## Productos

1. **Libro en PDF (LaTeX).** La versión formal, para imprimir, citar y leer de corrido.
2. **Libro web (Next.js).** La misma obra con lo que el papel no puede dar: código ejecutable en la página, animaciones interactivas, botones para descargar o abrir los notebooks.
3. **Notebooks del libro.** Generados automáticamente; el estudiante los usa como referencia o para recuperarse si se saltó algo.

El producto del **estudiante** es su notebook *"Mi calculadora de armaduras"*, en su Google Drive, organizado en tres secciones: **Motor** (funciones), **Datos** (la armadura a analizar) y **Resultados**.

## Cómo trabaja el estudiante

El camino recomendado es siempre el mismo: **crear su propio notebook en Google Drive y abrirlo con Colab**. El libro y la web existen para que ese camino no tenga fricción:

- **Leer y probar** en la web: cada bloque de código se puede ejecutar y modificar ahí mismo (Pyodide).
- **Trabajar** en su notebook de Colab, escribiendo el código él mismo.
- **Recuperarse** si se perdió: cada capítulo ofrece un *punto de control*, un notebook con todo el código acumulado hasta ese capítulo, para copiarlo o descargarlo y seguir desde ahí.
- **Instalar Python en local** queda como anexo opcional, para quien quiera.

## Alcance

**Fase 1 (primera meta):** Partes I a III del [índice](01-indice.md), es decir, de los primeros pasos hasta "Mi calculadora de armaduras", con PDF, web y notebooks.

**Fase 2:** Parte IV (extensiones: asentamientos, temperatura, apoyos inclinados, estabilidad, armaduras grandes).

**Fuera de alcance:**

- Una calculadora web con interfaz gráfica propia. La web es el libro, no una herramienta aparte: todo lo interactivo debe servir para entender o ejecutar lo que el libro enseña.
- Pórticos, armaduras 3D y elementos finitos en general. Solo se mencionan como "hacia dónde seguir".

## Registro de decisiones

| # | Decisión | Motivo |
|---|---|---|
| D1 | Nombre del repositorio: `libro-rigidez-python-armaduras2d`. | Es un libro independiente, ya no un anexo de tesis. |
| D2 | Español en todo; inglés solo cuando sea inevitable (palabras clave de Python, API de NumPy). | El público es hispanohablante. |
| D3 | LaTeX dedicado para el PDF y Next.js dedicado para la web, en lugar de una herramienta de fuente única (Quarto). | Control total del diseño y de la interactividad: un producto más cuidado. El costo de sincronizar se controla con las reglas de [sincronización](04-sincronizacion.md). |
| D4 | La prosa se escribe primero en LaTeX (fuente canónica) y la web se adapta cuando el capítulo está estable. | Una sola versión "verdadera" del texto evita discusiones sobre cuál es la correcta. |
| D5 | El código, las figuras, las tablas y los números tienen **una sola fuente** y se generan para ambos formatos. | Lo más peligroso de desincronizar es el código y los resultados, así que eso nunca se escribe dos veces. |
| D6 | Canal principal del estudiante: Google Colab desde su Drive. | Elimina la instalación, que es la principal causa de abandono (por ejemplo, Anaconda y pip instalando en intérpretes distintos). |
| D7 | Python en la web mediante Pyodide (Python compilado a WebAssembly, corre en el navegador). | Permite ejecutar los ejemplos sin instalar nada y sin servidor. |
| D8 | Entregable: un notebook con secciones Motor, Datos y Resultados, no un módulo `.py`. | Conserva la lección de separar herramienta y uso, sin agregar el paso de subir e importar archivos en Colab. El módulo `.py` queda como anexo opcional. |
| D9 | Python se enseña integrado con el método, con un capítulo de arranque mínimo y un anexo de referencia. | Motivación y retención: cada concepto de Python se aprende en el momento en que se necesita (ver "Enfoque pedagógico"). |
| D10 | Dependencias del código del libro: solo la biblioteca estándar, NumPy y Matplotlib. | Vienen preinstaladas en Colab y existen en Pyodide; cero instalaciones. |
| D11 | **Todo número que lee el estudiante empieza en 1**: nodos, barras y grados de libertad (nodo *i* → grados 2*i*−1 y 2*i*), también en las tablas y matrices impresas. El paso al índice 0 de Python ocurre en **un solo lugar** del código, explicado una vez en el capítulo 6. | Para una persona que no programa, contar desde 0 es antinatural y molesto; además, los libros de texto y las clases numeran desde 1. Esconder el 0 por completo no es posible, así que se aísla y se explica una vez. |
| D12 | Numeración natural de grados de libertad (por nodo), con partición mediante listas de libres y restringidos (`np.ix_`), en lugar de renumerar primero los libres. | Más simple y elimina la clase de errores de índices del proyecto anterior. La convención de renumerar (Kassimali) se explica en una caja. |
| D13 | Ejemplos con **datos realistas**: acero (E = 200 GPa), áreas de perfiles reales, luces y cargas de estructuras reales. Se verifica que los esfuerzos resultantes sean razonables. | Los datos irreales enseñan mal: el estudiante debe desarrollar intuición sobre órdenes de magnitud (desplazamientos en milímetros, esfuerzos en MPa). Ver [ejemplos](01-indice.md#ejemplos-que-recorren-el-libro). |
| D14 | Sin pandas. Los resultados se muestran con una función propia de tablas (f-strings), `np.set_printoptions` para las matrices y gráficos de Matplotlib. | La función de tablas se enseña en el libro (no es una caja negra), funciona igual en Colab, Pyodide y el PDF, y no suma otra biblioteca que aprender. |
| D15 | **Soluciones de los ejercicios en todos los formatos**: plegables en la web, en un anexo del PDF y en un notebook de soluciones por capítulo. Los ejercicios numéricos incluyen una celda que verifica la respuesta del estudiante. | El libro debe ayudar, no poner obstáculos: quien se traba necesita ver cómo se resuelve. |

| D16 | Título: **Análisis matricial de armaduras con Python**. Subtítulo: *Aprende el método de rigidez construyendo tu propia calculadora*. | Es el más fácil de encontrar y el que mejor corresponde a un texto universitario (opción E del análisis de abajo). |
| D17 | **Publicación abierta y autopublicada**: el libro completo, gratis, en la web propia del autor y difundido por sus redes. Sigue siendo un texto universitario de gama alta. | El propósito del libro es ayudar a los estudiantes; una editorial comercial habría exigido exclusividad y restringido la web gratuita. Se descartó la editorial a favor de la difusión. (Reemplaza la decisión anterior de publicar con editorial comercial.) |
| D18 | Licencias: **código con MIT**; **texto con CC BY-NC-SA 4.0**. | Ver la sección "Licencias". (Reemplaza la decisión anterior de reservar todos los derechos del texto.) |

| D19 | Registro: **primera persona del plural** como voz principal; **infinitivo** en los enunciados de los ejercicios. | Es lo habitual en los textos universitarios en español: acompaña al lector sin tutearlo. Ver la [guía de estilo](03-guia-de-estilo.md#redacción). |

No quedan decisiones pendientes de la revisión inicial.

## Publicación abierta

Sin editorial, el libro gana libertad y alcance, pero pierde dos cosas que una editorial aporta: **la revisión** y **la credibilidad formal**. Ambas se pueden recuperar con poco costo.

**Revisión (lo que haría una editorial):**

- **Revisión técnica:** uno o dos colegas de estructuras revisan cada parte antes de publicarla.
- **Prueba con estudiantes:** un grupo piloto sigue los capítulos en Colab y reporta dónde se traba. Es la prueba más valiosa para este libro.
- **Corrección de estilo y ortotipográfica** antes de cada versión mayor.
- **Fe de erratas pública** y un canal para reportar errores (por ejemplo, un formulario o los *issues* del repositorio).

**Credibilidad formal (opcional, pero útil para que se use en universidades):**

- **ISBN** para la edición en PDF: en muchos países es gratuito o de bajo costo para autores independientes (consultar la agencia nacional del ISBN del país del autor).
- **DOI** gratuito mediante Zenodo para cada versión publicada, para que el libro pueda citarse en tesis y artículos.
- **Versiones numeradas** (1.0, 1.1...) con fecha, y una **cita sugerida** en la página legal y en la web.

**Lo que no cambia:**

- La calidad editorial de gama alta y la maqueta propia (ver la [guía de estilo](03-guia-de-estilo.md#diseño-editorial-maqueta-propia)).
- El LaTeX semántico: ya no es para cambiar de maqueta por una editorial, pero sigue facilitando el mantenimiento y las ediciones futuras.

**Lo que se vuelve posible:**

- La web contiene el libro completo, como estaba planeado originalmente.
- El repositorio puede ser público. Esto da transparencia, permite que otros reporten errores y simplifica los enlaces "Abrir en Colab".
- Ofrecer una **versión impresa bajo demanda** (por ejemplo, Amazon KDP) para quien quiera el libro en papel, y aceptar donaciones. La licencia NC lo permite al autor.

**Para verificar:**

- Si trabajas en una universidad, revisa su reglamento de propiedad intelectual: algunas reclaman derechos sobre el material docente, aunque se publique gratis.
- Si alguien más aportó contenido (por ejemplo, desde la tesis original), acuerda por escrito la autoría.
- No se copian ejemplos ni figuras de otros libros: todo el material es propio.

## Título

Se eligió la **opción E**. Se conserva el análisis como registro.

Criterios: que prometa lo que el lector obtiene (construir algo propio), que contenga las palabras que un estudiante buscaría (*método matricial*, *rigidez*, *armaduras*, *Python*) y que no se lea como un manual árido. Lo usual en libros técnicos es un **título corto y recordable más un subtítulo descriptivo**, que es el que se encuentra en buscadores.

| Opción | Título | Subtítulo | Comentario |
|---|---|---|---|
| A | Del nudo al código | El método matricial de rigidez en Python: construye tu propia calculadora de armaduras | Recordable; evoca el método de los nudos que el lector ya conoce. |
| B | Tu propia calculadora de armaduras | El método de rigidez paso a paso con Python | Promesa directa; menos "académico". |
| C | Programa tus armaduras | Análisis matricial de rigidez con Python, desde cero | Tono activo; "desde cero" se refiere a Python. |
| D | Rigidez en Python | Construye una calculadora de armaduras planas con el método matricial | Corto y técnico; coincide con el nombre del repositorio. |
| E | Análisis matricial de armaduras con Python | Aprende el método de rigidez construyendo tu propia calculadora | El más buscable; el más parecido a un texto universitario clásico. |

**Atención al vocabulario regional:** "armadura" (Perú, México, Chile) se llama "cercha" en Colombia, Venezuela y España. Conviene mencionarlo en el prefacio y, si el libro apunta a todo el mundo hispano, considerar "armaduras (cerchas)" en el subtítulo o en la descripción comercial.

## Licencias

Se adoptó: **código con MIT y texto con CC BY-NC-SA 4.0** (decisión D18), por la vía de autopublicación con web gratuita.

Por qué CC BY-NC-SA 4.0 para el texto:

- **BY (atribución):** quien use el libro debe citar al autor.
- **NC (no comercial):** nadie más puede vender el libro ni obras derivadas. El autor sí puede (por ejemplo, la versión impresa bajo demanda).
- **SA (compartir igual):** si un docente adapta un capítulo para su curso, o alguien lo traduce, la adaptación queda con la misma licencia y sigue siendo libre.

Se consideró CC BY 4.0 (la de OpenStax, máxima difusión). Se prefirió NC-SA para que el trabajo no pueda ser revendido por terceros. Si en el futuro se quiere máxima difusión, se puede pasar a CC BY: abrir siempre es posible, cerrar no.

Se conserva el análisis original como registro.

Hay que licenciar dos cosas distintas.

**Código: MIT (recomendado sin dudas).** El estudiante tiene que poder copiar el código a su notebook, modificarlo y usarlo en su trabajo o en su empresa sin preguntarse si puede. MIT es la licencia permisiva más conocida y corta.

**Texto: depende de cómo quieras publicar.**

| Vía de publicación | Licencia recomendada para el texto | Consecuencias |
|---|---|---|
| **Editorial comercial** (o universitaria con venta) | Todos los derechos reservados | Las editoriales suelen exigir exclusividad y pueden rechazar una obra ya publicada con licencia abierta. La web gratuita habría que negociarla con ellas. |
| **Autopublicación** (Amazon KDP, Leanpub, venta del PDF) + web gratuita | CC BY-NC-SA 4.0 | Cualquiera puede leer, copiar y adaptar el libro **sin fines comerciales**, citándote. **Tú sí puedes venderlo**: la restricción "NC" obliga a los demás, no al autor. Es el modelo de muchos libros técnicos abiertos. |
| **Libro abierto puro** (máxima difusión) | CC BY 4.0 | Cualquiera puede usarlo para todo, incluso venderlo, citándote. Máximo alcance; ningún ingreso garantizado. |

**Recomendación:** mientras no decidas la vía de publicación, **el texto queda con todos los derechos reservados** y el código con MIT. Razón: una licencia Creative Commons es irrevocable para las copias ya distribuidas. Siempre puedes abrir el texto más adelante, pero no puedes cerrarlo después de abrirlo. Si eliges autopublicación con web gratuita, el cambio a CC BY-NC-SA 4.0 es inmediato.

**Para verificar antes de publicar** (esto no reemplaza una consulta legal):

- Si trabajas en una universidad, revisa su reglamento de propiedad intelectual: algunas reclaman derechos sobre material docente.
- Si alguien más aportó contenido (por ejemplo, desde la tesis original), acuerda por escrito la autoría.
- Las figuras y ejemplos propios evitan problemas; no se copian ejemplos ni figuras de otros libros.

## Enfoque pedagógico

Se descartó "primero todo Python, después el método" por tres razones: sin un propósito visible la motivación cae; lo aprendido sin aplicar se olvida antes de usarse; y la literatura sobre instrucción (primeros principios de Merrill, aprendizaje situado, ejemplos resueltos) favorece aprender centrado en un problema real del dominio del estudiante.

También se descartó mezclar sin orden: la teoría de la carga cognitiva (Sweller) advierte que introducir a la vez un concepto estructural nuevo y una sintaxis nueva satura la memoria de trabajo. Como el lector **ya conoce el método**, la carga nueva está en Python. Por eso cada capítulo primero **aísla** la herramienta de Python con ejemplos pequeños (siempre con datos estructurales) y después la **aplica** al paso del método.

El orden natural del método hace que la dificultad de Python crezca sola: variables → listas y diccionarios → bucles → funciones → arreglos de NumPy → indexación → álgebra lineal → gráficos → organización del código.

## Lecciones del proyecto anterior

Lo que se conserva: aprender construyendo, un ejemplo que recorre el libro, describir la armadura con diccionarios.

Lo que no se repite:

- Cuadernos acumulativos escritos a mano (cada uno copiaba todo lo anterior). Ahora los puntos de control se **generan**.
- Mezcla de listas y NumPy con `.tolist()` por todas partes, y vectores que mezclaban números con textos como `"F_n1_x"` o `None`. El código trabaja solo con números; lo simbólico va en la prosa.
- Contenido de Python ajeno al dominio (listas "en desarrollo web", ejemplos de notas de alumnos).
- Errores ocultos por usar un solo ejemplo (el índice que solo funcionaba porque había 4 grados libres y 4 restringidos). Ahora hay varios ejemplos y tests.
- Resolver con `np.linalg.inv`. Se usa `np.linalg.solve` y se explica por qué.
- Ningún resultado comparado con un cálculo a mano o con otro programa. Ahora cada capítulo verifica.
