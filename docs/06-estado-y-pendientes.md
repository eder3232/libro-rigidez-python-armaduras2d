# Estado, publicación y pendientes

Estado al **17/10/2026**. Este documento es la fuente de verdad sobre qué está hecho, dónde está publicado y qué falta. Si cambia algo de lo que dice, se actualiza aquí y en el resumen del [README](../README.md).

## Qué está hecho

- **Texto completo:** prefacio, capítulos 1 a 12 (partes I a III del [índice](01-indice.md)) y anexos A a F, con portada, página legal, bibliografía e índice alfabético. El PDF tiene 180 páginas.
- **Código y verificación:** el código de los 12 capítulos en `codigo/`, con 69 tests (`uv run pytest`) que comprueban los resultados y el equilibrio de cada ejemplo. Todo número que cita el texto sale de ejecutar el código ([sincronización](04-sincronizacion.md)).
- **Notebooks:** 36 generados en `notebooks/`, tres por capítulo: lección, soluciones y punto de control.
- **Libro web:** los capítulos y anexos en MDX (generados desde el LaTeX), con fórmulas en KaTeX que usan las mismas macros del PDF, figuras en SVG, soluciones plegables y enlaces «Abrir en Colab» a cada notebook.
- **Publicado** en GitHub y Vercel (ver abajo).

## Dónde está publicado

| Qué | Dónde |
|---|---|
| Repositorio | https://github.com/eder3232/libro-rigidez-python-armaduras2d, **público**. Tiene que serlo: los enlaces «Abrir en Colab» y la URL del prefacio apuntan a los notebooks de este repo, y Colab solo abre repos públicos. |
| Libro web | https://eder3232-libro-armaduras.vercel.app (también responde `libro-rigidez-python-armaduras2d.vercel.app`) |
| Hosting | Vercel, proyecto `libro-rigidez-python-armaduras2d` (cuenta `eder3232`), conectado al repo. **Cada push a `main` se despliega solo.** |
| PDF para bajar | En la web personal: https://eder3232.com/libros/analisis-matricial-de-armaduras-con-python.pdf. Es una **copia a mano** de `libro/build/libro.pdf` (que no está en git). |
| Caso de estudio | https://eder3232.com/es/proyectos/libro-armaduras: cuenta el libro, cómo se hizo, y enlaza el PDF, la web y este repo. |

**Configuración de Vercel** (ya hecha; anotada por si hay que rehacer el proyecto):
- Root Directory: `web`. Framework: Next.js. Node 24. Sin variables de entorno.
- Debe quedar activada «Include files outside the root directory in the Build Step» (viene activada): la web lee archivos de fuera de `web/`, como las macros de `libro/estilo/notacion.tex` y los fragmentos y salidas de `recursos/`.
- Vercel solo corre `next build`, no `scripts/construir.py`. Por eso **lo generado tiene que estar en git** (`web/contenido/`, `recursos/`, `web/public/`, `notebooks/`): antes de hacer push, construir el libro y subir lo que haya cambiado.
- El dominio `eder3232-libro-armaduras.vercel.app` es un dominio del proyecto, así que se mantiene en cada despliegue. Los dominios van con el prefijo `eder3232-…` en `vercel.app`, sin subdominio propio.

## Pendientes

### Para terminar la versión 1.0

1. **Validación con SAP2000 (anexo D).** Modelar los ejemplos B y C y anotar sus resultados en la columna `sap2000` de [`validacion/resultados_sap2000.csv`](../validacion/resultados_sap2000.csv): 41 valores, todos vacíos. Paso a paso en [05-validacion-sap2000.md](05-validacion-sap2000.md). Mientras falten, el anexo D muestra una raya en cada valor y un aviso de pendiente.
2. **Capturas de pantalla.** Faltan las 8, en `capturas/` y con estos nombres: `colab_vacio`, `colab_nuevo` y `colab_primera_celda` (capítulo 2), y `sap_b_modelo`, `sap_b_deformada`, `sap_b_axiales`, `sap_c_modelo` y `sap_c_axiales` (anexo D). Mientras falten, el PDF y la web muestran un recuadro «Aquí debe ir la captura…». Cómo tomarlas: [05-validacion-sap2000.md § 5](05-validacion-sap2000.md#5-capturas-de-pantalla).
3. **Construir, revisar y publicar.** `uv run python scripts/construir.py`, revisar el PDF y la web, hacer commit y push (Vercel despliega la web). Después, **copiar el PDF nuevo a la web personal**: `libro/build/libro.pdf` → `public/libros/analisis-matricial-de-armaduras-con-python.pdf` en el repo `eder3232-personal-webpage`, y publicarla. En ese repo también hay que actualizar el caso (`src/data/casos.ts`, entrada `libro-armaduras`): el periodo dice «2026, versión preliminar» y la sección «Después» dice que falta SAP2000.
4. **Quitar «Versión preliminar»** de la página legal (`libro/portada.tex`) cuando estén SAP2000 y las capturas, y numerar la versión (ver más abajo).

### Errores conocidos de la web

- **Los números de ecuación no se alinean a la derecha.** Se ven pegados a la fórmula, después de su punto final: «…\]**.(5.1)**». No es el convertidor: el MDX trae bien `\tag{5.1}` y KaTeX genera el `.tag`. El problema está en la maquetación (`web/src/app/globals.css`, regla `.katex-display`, o algún estilo que le quita el ancho completo al bloque de la ecuación). Revisarlo en el navegador con las herramientas de desarrollo, en `/capitulos/cap05_rigidez_barra`.
- **El README decía que la web ejecuta Python (Pyodide) y tiene animaciones interactivas.** Todavía no: eso está planeado (decisión D7 y las ideas de animación del [índice](01-indice.md)), pero no existe. Hoy el estudiante ejecuta el código en Colab. Ya se corrigió en el README; no prometerlo en ningún otro lado hasta que exista.

### Mejoras de la web (sin fecha)

- **Ejecutar el código en la página** con Pyodide (D7): cada bloque de código, editable y ejecutable sin salir del libro.
- **Animaciones interactivas:** las ideas están en el [índice](01-indice.md), una por capítulo. Se priorizan después.
- **Una portada en la web** con la tapa, el botón para bajar el PDF y el enlace al repo. Hoy el inicio es solo el índice de capítulos.

### Fase 2 y credibilidad (opcional)

- **Parte IV, extensiones:** asentamientos, temperatura y errores de fabricación, apoyos inclinados, estabilidad, armaduras grandes ([índice](01-indice.md#parte-iv-extensiones-fase-2)).
- **Versiones numeradas** (1.0, 1.1…) con fecha y una cita sugerida en la página legal y en la web.
- **DOI** gratuito en Zenodo para cada versión, para que se pueda citar en tesis.
- **ISBN** para la edición en PDF (consultar la agencia nacional del ISBN).
- **Fe de erratas pública** y un canal para reportar errores (por ejemplo, los *issues* del repositorio).
- **Revisión técnica** por colegas y **prueba con un grupo de estudiantes** en Colab ([visión](00-vision-y-decisiones.md#publicación-abierta)).
