# Análisis matricial de armaduras con Python

*Aprende el método de rigidez construyendo tu propia calculadora*

Texto universitario para estudiantes de 4.º año de Ingeniería Civil: aprenden a **construir su propia calculadora de armaduras 2D** con el método matricial de rigidez, escribiendo el código en Python paso a paso.

## Estado (17/10/2026)

**Versión preliminar, publicada.** El texto está completo (prefacio, capítulos 1 a 12 y anexos A a F; 180 páginas), con 69 tests y 36 notebooks.

| | |
|---|---|
| Libro web | https://eder3232-libro-armaduras.vercel.app (Vercel; cada push a `main` se despliega solo) |
| PDF para bajar | https://eder3232.com/libros/analisis-matricial-de-armaduras-con-python.pdf (copia a mano en la web personal) |
| Caso de estudio | https://eder3232.com/es/proyectos/libro-armaduras |

**Lo que falta para la 1.0:**
1. La validación con SAP2000 (anexo D): los 41 valores de `validacion/resultados_sap2000.csv`.
2. Las 8 capturas de pantalla (Colab y SAP2000).
3. Construir, publicar y **volver a copiar el PDF a la web personal**.

**Error conocido:** en la web, los números de ecuación no se alinean a la derecha y quedan pegados a la fórmula («.(5.1)»).

Todo el detalle está en [**Estado, publicación y pendientes**](docs/06-estado-y-pendientes.md): qué está hecho, la configuración de Vercel, los pendientes y las mejoras planeadas. El paso a paso de SAP2000 y las capturas está en [Validación con SAP2000 y capturas pendientes](docs/05-validacion-sap2000.md).

## Construir el libro

```
uv run python scripts/construir.py
```

Genera el PDF (`libro/build/libro.pdf`), los notebooks (`notebooks/`) y la web (`web/out/`), y ejecuta todos los tests.

Vercel solo corre `next build` dentro de `web/`, así que lo generado (`web/contenido/`, `recursos/`, `web/public/`, `notebooks/`) tiene que estar en git: construir el libro **antes** de hacer push.

> **Licencias:** el texto del libro se publica con [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es) y el código con licencia MIT. El libro es gratuito y autopublicado.

## Qué se publica

| Producto | Formato | Rol |
|---|---|---|
| Libro impreso / PDF | LaTeX | Fuente canónica de la prosa. |
| Libro web | Next.js | El libro completo, gratis, con fórmulas (KaTeX), figuras, soluciones plegables y enlaces «Abrir en Colab» a los notebooks. Ejecutar el código en la página (Pyodide) y las animaciones interactivas están planeados, todavía no existen. |
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
capturas/    Capturas de pantalla del libro (las aporta el autor)
validacion/  Resultados de SAP2000 para el anexo D (los anota el autor)
```

## Documentos de trabajo

1. [Visión y decisiones](docs/00-vision-y-decisiones.md): qué es el libro, para quién y por qué se decidió cada cosa.
2. [Índice detallado](docs/01-indice.md): capítulos, Python que se enseña en cada uno y animaciones previstas.
3. [Plantilla de capítulo](docs/02-plantilla-capitulo.md): estructura que siguen todos los capítulos.
4. [Guía de estilo](docs/03-guia-de-estilo.md): redacción, notación, unidades y convenciones del código.
5. [Sincronización](docs/04-sincronizacion.md): cómo se mantienen alineados LaTeX, web y notebooks.
6. [Validación con SAP2000 y capturas pendientes](docs/05-validacion-sap2000.md): lo que falta hacer fuera del código para terminar el libro, paso a paso.
7. [Estado, publicación y pendientes](docs/06-estado-y-pendientes.md): qué está hecho, dónde está publicado (GitHub, Vercel, web personal) y todo lo que falta.

**Leer estos documentos antes de escribir cualquier capítulo.**
