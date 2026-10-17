# Validación con SAP2000 y capturas pendientes

Guía para terminar lo único del libro que necesita trabajo fuera del código: la comparación con SAP2000 (anexo D) y las capturas de pantalla (anexo D y capítulo 2). El libro ya está escrito suponiendo que los resultados coinciden. Basta con:

1. Modelar los ejemplos B y C en SAP2000 ([pasos 1 a 3](#1-modelar-el-ejemplo-b)).
2. Anotar sus resultados en [`validacion/resultados_sap2000.csv`](../validacion/resultados_sap2000.csv) ([paso 4](#4-anotar-los-resultados)).
3. Guardar las capturas en la carpeta [`capturas/`](../capturas) con los nombres indicados ([paso 5](#5-capturas-de-pantalla)).
4. Construir el libro y revisar ([paso 6](#6-construir-y-revisar)).

No hay que editar ningún archivo LaTeX ni de la web: las tablas del anexo D se llenan solas con el CSV, cada recuadro «Aquí debe ir la captura…» se reemplaza por su imagen en cuanto el archivo existe, y el aviso de pendiente del anexo D desaparece cuando el CSV está completo.

---

## Convenciones

| | Libro | SAP2000 |
|---|---|---|
| Plano del modelo | $xy$ | $xz$ (el eje vertical es $z$) |
| Coordenada vertical | $y$ | $z$ |
| Desplazamientos | $u_x$, $u_y$ | `U1`, `U3` |
| Reacciones | $R_x$, $R_y$ | `F1`, `F3` |
| Fuerza axial | $N$, positiva en tracción | `P`, positiva en tracción |

Los signos coinciden: desplazamientos y reacciones positivos en el sentido de los ejes globales, y fuerza axial positiva en tracción. **No hay que cambiar ningún signo.**

**Unidades:** trabajar en `KN, m, C`. Los desplazamientos se anotan en el CSV en **milímetros** (SAP2000 los da en metros: multiplicar por 1000, o cambiar las unidades de la tabla a `KN, mm, C`). Las fuerzas y reacciones, en **kN**.

---

## 1. Modelar el ejemplo B

### Datos

Acero, $E = 2.0\times10^{8}$ kN/m², todas las barras con $A = 0.0020$ m² (20 cm²).

| Nodo | x (m) | z (m) |
|---|---|---|
| 1 | 0.0 | 0.0 |
| 2 | 3.0 | 0.0 |
| 3 | 0.0 | 4.0 |
| 4 | 3.0 | 4.0 |

| Barra | Nodo inicial | Nodo final |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 4 |
| 4 | 1 | 3 |
| 5 | 1 | 4 |
| 6 | 2 | 3 |

- **Apoyos:** nodo 1 articulado (`U1` y `U3` restringidos); nodo 2 rodillo (solo `U3` restringido).
- **Cargas:** nodo 3: 30 kN en `X` y −40 kN en `Z`; nodo 4: −40 kN en `Z`.

### Pasos en SAP2000

Los nombres de los menús corresponden a la interfaz en inglés; pueden variar ligeramente según la versión.

1. **Modelo nuevo:** `File > New Model`, unidades `KN, m, C`, plantilla `Grid Only` con líneas en x = 0, 3 y en z = 0, 4 (en y, una sola línea).
2. **Material:** `Define > Materials > Add New Material`, tipo `Steel`. Cambiar el módulo de elasticidad a `2.0E+08` kN/m² y poner el peso y la masa por unidad de volumen en `0`.
3. **Sección:** `Define > Section Properties > Frame Sections > Add New Property`, tipo `Other > General`. Área (`Cross-section (axial) area`) = `0.002` m², con el material anterior. Las demás propiedades no influyen (se liberan los momentos), pero no pueden ser cero.
4. **Barras:** `Draw > Draw Frame/Cable`, dibujando las barras **en el orden de la tabla** (1 a 6), para que SAP2000 les dé los mismos números que el libro.
5. **Revisar la numeración:** `View > Set Display Options` (Ctrl+W): activar `Labels` en `Joints` y en `Frames`. Si algún número no coincide con el libro, corregirlo con `Edit > Change Labels`.
6. **Liberar los momentos:** seleccionar todas las barras y `Assign > Frame > Releases/Partial Fixity`: liberar `Moment 22` y `Moment 33` al inicio y al final.
7. **Grados de libertad:** `Analyze > Set Analysis Options`: dejar activos solo `UX` y `UZ` (armadura plana). Con los momentos liberados, quitar los giros no cambia los resultados y evita avisos de inestabilidad.
8. **Apoyos:** seleccionar el nodo 1, `Assign > Joint > Restraints`, restringir `U1` y `U3`. Seleccionar el nodo 2 y restringir solo `U3`.
9. **Sin peso propio:** `Define > Load Patterns`: en el patrón `DEAD`, poner `Self Weight Multiplier` = `0` y pulsar `Modify Load Pattern`.
10. **Cargas:** seleccionar el nodo 3, `Assign > Joint Loads > Forces`, patrón `DEAD`, sistema `GLOBAL`: `Force Global X` = `30`, `Force Global Z` = `-40`. Repetir en el nodo 4 con `Force Global Z` = `-40`.
11. **Analizar:** `Analyze > Set Load Cases to Run`: ejecutar solo `DEAD` (marcar `MODAL` como `Do Not Run`) y `Run Now`.

### Comprobación rápida

Antes de anotar los resultados, comprobar que la reacción vertical del nodo 2 es **80.00 kN** y la horizontal del nodo 1, **−30.00 kN**. Si no, revisar los apoyos, las cargas y el peso propio.

---

## 2. Modelar el ejemplo C

### Datos

Acero, $E = 2.0\times10^{8}$ kN/m². Dos secciones:

- `CORDON`: $A = 0.0030$ m² (30 cm²): barras 1 a 12.
- `ALMA`: $A = 0.0015$ m² (15 cm²): barras 13 a 21.

| Nodo | x (m) | z (m) | | Nodo | x (m) | z (m) |
|---|---|---|---|---|---|---|
| 1 | 0.0 | 0.0 | | 7 | 18.0 | 0.0 |
| 2 | 3.0 | 0.0 | | 8 | 3.0 | 3.0 |
| 3 | 6.0 | 0.0 | | 9 | 6.0 | 3.0 |
| 4 | 9.0 | 0.0 | | 10 | 9.0 | 3.0 |
| 5 | 12.0 | 0.0 | | 11 | 12.0 | 3.0 |
| 6 | 15.0 | 0.0 | | 12 | 15.0 | 3.0 |

| Barra | Nodos | Sección | | Barra | Nodos | Sección |
|---|---|---|---|---|---|---|
| 1 | 1 – 2 | CORDON | | 12 | 12 – 7 | CORDON |
| 2 | 2 – 3 | CORDON | | 13 | 2 – 8 | ALMA |
| 3 | 3 – 4 | CORDON | | 14 | 3 – 9 | ALMA |
| 4 | 4 – 5 | CORDON | | 15 | 4 – 10 | ALMA |
| 5 | 5 – 6 | CORDON | | 16 | 5 – 11 | ALMA |
| 6 | 6 – 7 | CORDON | | 17 | 6 – 12 | ALMA |
| 7 | 8 – 9 | CORDON | | 18 | 8 – 3 | ALMA |
| 8 | 9 – 10 | CORDON | | 19 | 9 – 4 | ALMA |
| 9 | 10 – 11 | CORDON | | 20 | 11 – 4 | ALMA |
| 10 | 11 – 12 | CORDON | | 21 | 12 – 5 | ALMA |
| 11 | 1 – 8 | CORDON | | | | |

- **Apoyos:** nodo 1 articulado (`U1` y `U3`); nodo 7 rodillo (solo `U3`).
- **Cargas:** −25 kN en `Z` en cada uno de los nodos 2, 3, 4, 5 y 6.

### Pasos

Los mismos del ejemplo B, en un modelo nuevo: rejilla con x = 0, 3, …, 18 y z = 0, 3; dos secciones `General` (`CORDON` y `ALMA`); barras dibujadas en el orden de la tabla; momentos liberados; solo `UX` y `UZ` activos; peso propio nulo.

### Comprobación rápida

Cada reacción vertical debe valer **62.50 kN**, y la barra 15 (montante central), **0**.

---

## 3. Qué resultados extraer

`Display > Show Tables`, en `Analysis Results`:

| Tabla de SAP2000 | Columnas | Unidades | Para |
|---|---|---|---|
| `Joint Displacements` | `U1`, `U3` | mm (ver [Convenciones](#convenciones)) | Ejemplo B: los 4 nodos. Ejemplo C: solo `U3` del nodo 4. |
| `Joint Reactions` | `F1`, `F3` | kN | Ejemplo B: `F1` y `F3` del nodo 1, `F3` del nodo 2. Ejemplo C: `F3` de los nodos 1 y 7. |
| `Element Forces - Frames` | `P` | kN | Todas las barras. `P` es constante a lo largo de cada barra: tomar cualquier estación. |

Seleccionar solo el caso `DEAD`. Las tablas pueden exportarse a Excel (`File > Export`) para copiar los valores con comodidad.

---

## 4. Anotar los resultados

Abrir [`validacion/resultados_sap2000.csv`](../validacion/resultados_sap2000.csv) (con Excel o un editor de texto) y llenar **solo la última columna, `sap2000`**, en cada una de sus 41 filas:

- La columna `descripcion` dice qué resultado va en cada fila y de qué tabla de SAP2000 sale.
- La columna `unidad` dice en qué unidad anotarlo (mm o kN).
- La columna `calculadora` es el valor de nuestra calculadora, como referencia: el de SAP2000 debe ser prácticamente igual.
- Usar punto o coma decimal; con al menos los mismos decimales que la columna `calculadora`.
- Los desplazamientos de los nodos apoyados (por ejemplo, `U3` del nodo 1) son `0`.

Si se guarda desde Excel, mantener el formato **CSV UTF-8** y no cambiar las otras columnas ni el orden de las filas.

---

## 5. Capturas de pantalla

Guardar cada captura en la carpeta [`capturas/`](../capturas), en formato **PNG** y con el **nombre exacto** de la tabla. Recomendaciones:

- Ancho de al menos 1600 píxeles; recortar los bordes de la ventana para dejar solo el modelo o el diagrama.
- Fondo blanco, si la versión lo permite (`Options > Colors > Display` o equivalente).
- Para capturar, la herramienta Recortes de Windows (Windows + Mayús + S) y guardar como PNG.

### Anexo D (SAP2000)

| Archivo | Qué debe mostrar | Cómo obtenerlo |
|---|---|---|
| `sap_b_modelo.png` | El ejemplo B con los números de nodos y barras, los apoyos y las cargas. | `Set Display Options` con `Labels` de nodos y barras; `Display > Show Object Load Assigns > Joint` para ver las cargas. |
| `sap_b_deformada.png` | La deformada del ejemplo B, con la forma sin deformar de fondo. | `Display > Show Deformed Shape` (F6), caso `DEAD`, con `Wire Shadow`. |
| `sap_b_axiales.png` | El diagrama de fuerzas axiales del ejemplo B, con el valor de cada barra. | `Display > Show Forces/Stresses > Frames/Cables`, componente `Axial Force`, con `Show Values on Diagram`. |
| `sap_c_modelo.png` | El ejemplo C con los números de nodos y barras, los apoyos y las cargas. | Igual que `sap_b_modelo.png`. |
| `sap_c_axiales.png` | El diagrama de fuerzas axiales del ejemplo C, con valores. | Igual que `sap_b_axiales.png`. |

### Capítulo 2 (Google Drive y Colab)

| Archivo | Qué debe mostrar |
|---|---|
| `colab_nuevo.png` | Google Drive con la carpeta *Calculadora de armaduras* abierta y el menú **Nuevo > Más > Google Colaboratory** desplegado. |
| `colab_vacio.png` | El notebook recién creado en Colab, con el nombre cambiado a *Capitulo 02* y una celda de código vacía. |
| `colab_primera_celda.png` | La celda `print("Hola, armaduras")` ya ejecutada, con el botón de ejecución a la izquierda y la salida `Hola, armaduras` debajo. |

Las capturas de Colab no dependen de SAP2000 y pueden hacerse en cualquier momento.

---

## 6. Construir y revisar

```
uv run python scripts/construir.py
```

1. **Si un resultado no coincide,** la construcción se detiene en el paso de tests con un mensaje como `Ejemplo B: fuerza axial P de la barra 5: SAP2000 9.80 kN, calculadora 10.19 kN`. La tolerancia es del 1 % (o dos unidades de la última cifra). Revisar primero el modelo de SAP2000: apoyos, unidades, peso propio, momentos liberados y numeración de barras. Si el modelo está bien, avisar a Claude con el mensaje.
2. **Revisar el anexo D** en `libro/build/libro.pdf`: el aviso naranja «Pendiente: faltan resultados…» debe haber desaparecido, las tablas deben tener la columna SAP2000 llena y las capturas deben verse en lugar de los recuadros.
3. **Confirmar las frases escritas con la suposición positiva.** Si todos los resultados coinciden, no hay que cambiar nada. Si alguno no coincide y la diferencia tiene una explicación, hay que ajustar estas frases:

   | Archivo | Frase |
   |---|---|
   | `libro/anexos/anexoD_validacion.tex` | «Los resultados coinciden en todas las cifras que muestran las tablas.» (ejemplo B) |
   | `libro/anexos/anexoD_validacion.tex` | «La deformada de SAP2000 … y su diagrama de fuerzas axiales … son, además, los mismos que dibuja nuestra calculadora.» |
   | `libro/anexos/anexoD_validacion.tex` | «También aquí los resultados coinciden…» (ejemplo C) |
   | `libro/anexos/anexoD_validacion.tex` | Sección «Conclusión». |
   | `libro/capitulos/cap10_fuerzas_internas.tex` | «En el anexo D las comparamos con las de SAP2000, un programa comercial, y coinciden.» |

4. **Actualizar el estado** en [`docs/04-sincronizacion.md`](04-sincronizacion.md): el capítulo 2 sin «falta: capturas de Colab», el capítulo 10 sin «falta: comparación con software comercial» y el anexo D como estable.
