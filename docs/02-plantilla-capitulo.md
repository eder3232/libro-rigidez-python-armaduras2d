# Plantilla de capítulo

Todos los capítulos de las Partes II a IV siguen esta estructura, en este orden. Los capítulos 1 y 2 y los anexos pueden apartarse de ella cuando haga falta.

## Secciones

### 1. Objetivo

Uno o dos párrafos: qué parte de la calculadora se construye y en qué punto del diagrama de flujo del método estamos. Termina con los **objetivos de aprendizaje**: una lista breve de lo que el estudiante sabrá hacer al final, redactada con verbos observables ("calcular", "implementar", "verificar").

### 2. Recordatorio teórico

La teoría del método **que el lector ya conoce**, recordada de forma breve y precisa con la notación del libro (ver [guía de estilo](03-guia-de-estilo.md)). Remite a la bibliografía para el desarrollo completo. No se demuestra lo que se puede citar.

### 3. Herramienta de Python

El concepto de Python nuevo, **aislado**: explicado con ejemplos pequeños, pero siempre con datos estructurales (una barra, un nodo, una carga), nunca con ejemplos ajenos al dominio. Aquí no se avanza en la calculadora.

### 4. Implementación

Se aplica la herramienta al paso del método, sobre el ejemplo del capítulo. El código que forma parte de la calculadora se marca como **acumulable** (ver [sincronización](04-sincronizacion.md)): es lo que irá al punto de control.

Incluye al menos un **problema resuelto** (enunciado, solución con código y su salida, y verificación) y, cuando el procedimiento lo amerite, una caja **Estrategia de resolución** con los pasos a seguir.

### 5. Verificación

Todo resultado nuevo se comprueba con al menos uno de estos medios:

- cálculo a mano (ejemplo A);
- una propiedad que debe cumplirse (simetría, equilibrio, singularidad);
- software comercial (ejemplo B).

La verificación se enseña como un hábito de ingeniero, no como un trámite.

### 6. Repaso y resumen del capítulo

Los puntos clave del capítulo en una lista breve: las ecuaciones, las funciones de la calculadora que se construyeron y los conceptos de Python que se aprendieron. Cuando corresponda, termina con las **referencias** del capítulo para profundizar.

### 7. Ejercicios

Entre 3 y 6 ejercicios, de menor a mayor dificultad. Todos tienen solución completa y explicada, disponible en todos los formatos (decisión D15):

- **Web:** plegada debajo de cada ejercicio.
- **PDF:** en el anexo F, y cada ejercicio indica la página de su solución.
- **Notebook:** `soluciones_capNN.ipynb`, con su enlace "Abrir en Colab".

Los ejercicios con respuesta numérica traen una **celda de verificación**: el estudiante escribe su resultado y la celda le dice si es correcto (con tolerancia) y, si no, le da una pista.

### 8. Punto de control

Cierre fijo del capítulo:

> **Punto de control.** Si algo no funcionó o se omitió una parte, el notebook con todo el código hasta este capítulo permite continuar desde aquí.
>
> [Abrir en Colab] · [Descargar .ipynb]

En el PDF, el texto equivalente con la dirección web del notebook.

## Cajas (elementos destacados)

Se usan con moderación; nunca dos cajas seguidas.

| Caja | Uso |
|---|---|
| **Recuerda** | Un dato teórico clave que el lector debería tener presente. |
| **Python** | Un detalle del lenguaje que conviene saber pero no es esencial. |
| **Cuidado** | Un error frecuente y cómo evitarlo. |
| **Para saber más** | Un tema que excede el libro, con una referencia. |
| **Estrategia de resolución** | Los pasos para abordar un tipo de problema, o una recomendación de método de trabajo. |
| **Problema resuelto** | Enunciado, solución (código y salida) y verificación. Numerado por capítulo. |
| **Ecuación clave** | Las ecuaciones centrales del capítulo, resaltadas. Una o dos por capítulo. |

| Elemento | LaTeX | Web (MDX) |
|---|---|---|
| Recuerda, Python, Cuidado, Para saber más | `\begin{recuerda}` … | `<Recuerda>` … |
| Estrategia de resolución | `\begin{estrategia}` | `<Estrategia>` |
| Problema resuelto | `\begin{problemaresuelto}[título]` + `\solucion` | `<ProblemaResuelto numero="2.1" titulo="…">` + `<Solucion />` |
| Ecuación clave | `\begin{ecuacionclave}` (entorno `align*`) | `<EcuacionClave>` |
| Objetivos | `\begin{objetivos}` | `<Objetivos>` |
| Código | `\fragmento{nombre}` | `<Fragmento nombre="…" />` |
| Salida del código | `\salida{nombre}` | `<Salida nombre="…" />` |
| Ejercicio | `\begin{ejercicio}{2.1}`; su solución con `\soluciondel{2.1}` | por definir al adaptar el primer capítulo |
| Repaso y resumen | `\repasoyresumen` | `## Repaso y resumen del capítulo` |
| Punto de control | `\puntodecontrol{02}` | `<PuntoDeControl capitulo="02" />` |
| Término técnico | `\termino{español}{inglés}`, o `\concepto{palabra}` si es igual en ambos idiomas | cursiva, con el inglés entre paréntesis |

## Criterios de "capítulo terminado"

Un capítulo está terminado cuando:

- [ ] sigue esta plantilla;
- [ ] todo su código vive en `codigo/` y los tests pasan;
- [ ] los notebooks del capítulo y del punto de control se generan sin errores y se ejecutan de principio a fin en Colab;
- [ ] los números citados en el texto provienen de `recursos/` (no se escribieron a mano);
- [ ] cumple la [guía de estilo](03-guia-de-estilo.md);
- [ ] tiene ejercicios con soluciones en la web, el PDF y su notebook de soluciones;
- [ ] está registrado en la tabla de estado de [sincronización](04-sincronizacion.md).
