# Análisis matricial de armaduras con Python

*Aprende el método de rigidez construyendo tu propia calculadora*

Texto universitario para estudiantes de 4.º año de Ingeniería Civil: aprenden a **construir su propia calculadora de armaduras 2D** con el método matricial de rigidez, escribiendo el código en Python paso a paso.

> **Estado:** planificación. Todavía no hay contenido escrito; los documentos de `docs/` están en revisión.

> **Licencias:** el texto del libro se publica con [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es) y el código con licencia MIT. El libro es gratuito y autopublicado.

## Qué se publica

| Producto | Formato | Rol |
|---|---|---|
| Libro impreso / PDF | LaTeX | Fuente canónica de la prosa. |
| Libro web | Next.js | El libro completo, gratis, con código ejecutable en el navegador (Pyodide), animaciones interactivas, soluciones y enlaces a los notebooks. |
| Notebooks | `.ipynb` (generados) | Lo que el estudiante copia a su Google Drive y abre en Colab. Uno por capítulo, más un "punto de control" por capítulo. |

El **entregable del estudiante** es su propio notebook *"Mi calculadora de armaduras"*, en su Google Drive.

## Estructura del repositorio

```
codigo/      Fuente única del código Python (por capítulo) y sus tests
notebooks/   Notebooks generados desde codigo/ (no se editan a mano)
recursos/    Figuras, tablas y resultados generados; macros matemáticas compartidas
libro/       Fuente LaTeX del libro
web/         Aplicación Next.js del libro web
scripts/     Generadores y verificadores de sincronía
docs/        Visión, índice, plantilla, estilo y reglas de sincronización
```

## Documentos de trabajo

1. [Visión y decisiones](docs/00-vision-y-decisiones.md): qué es el libro, para quién y por qué se decidió cada cosa.
2. [Índice detallado](docs/01-indice.md): capítulos, Python que se enseña en cada uno y animaciones previstas.
3. [Plantilla de capítulo](docs/02-plantilla-capitulo.md): estructura que siguen todos los capítulos.
4. [Guía de estilo](docs/03-guia-de-estilo.md): redacción, notación, unidades y convenciones del código.
5. [Sincronización](docs/04-sincronizacion.md): cómo se mantienen alineados LaTeX, web y notebooks.

**Leer estos documentos antes de escribir cualquier capítulo.**
