# Capturas pendientes

Lo único del libro que necesita trabajo fuera del código: las tres capturas de pantalla de Colab del capítulo 2.

La validación del anexo D ya no requiere trabajo manual. `codigo/anexoD_validacion.py` analiza los ejemplos B y C con OpenSees en cada construcción, registra sus resultados para las tablas (`\valoropensees`) y dibuja las figuras. `codigo/tests/test_validacion.py` comprueba que coincidan con la calculadora (decisión D21 en [visión y decisiones](00-vision-y-decisiones.md)).

No hay que editar ningún archivo LaTeX ni de la web: cada recuadro «Aquí debe ir la captura…» se reemplaza por su imagen en cuanto el archivo existe.

---

## Capturas del capítulo 2 (Google Drive y Colab)

Guardar cada captura en la carpeta [`capturas/`](../capturas), en formato **PNG** y con el **nombre exacto** de la tabla.

| Archivo | Qué debe mostrar |
|---|---|
| `colab_nuevo.png` | Google Drive con la carpeta *Calculadora de armaduras* abierta y el menú **Nuevo > Más > Google Colaboratory** desplegado. |
| `colab_vacio.png` | El notebook recién creado en Colab, con el nombre cambiado a *Capitulo 02* y una celda de código vacía. |
| `colab_primera_celda.png` | La celda `print("Hola, armaduras")` ya ejecutada, con el botón de ejecución a la izquierda y la salida `Hola, armaduras` debajo. |

Recomendaciones:

- Ancho de al menos 1600 píxeles; recortar los bordes de la ventana para dejar solo lo que importa.
- Tema claro de Colab y del navegador.
- Para capturar, la herramienta Recortes de Windows (Windows + Mayús + S) y guardar como PNG.

---

## Construir y revisar

```
uv run python scripts/construir.py
```

1. Revisar el capítulo 2 en `libro/build/libro.pdf` y en la web: las capturas deben verse en lugar de los recuadros.
2. Actualizar el estado en [`docs/04-sincronizacion.md`](04-sincronizacion.md): el capítulo 2 sin «falta: capturas de Colab».
