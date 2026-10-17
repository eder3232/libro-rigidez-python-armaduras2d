# Sin las diagonales 18 y 19, el tramo izquierdo
# queda formado por rectángulos sin arriostrar
barras_sin_diagonales = {}
for numero, datos in barras_c.items():
    if numero not in (18, 19):
        barras_sin_diagonales[numero] = datos

try:
    analizar_armadura(nodos_c, barras_sin_diagonales,
                      apoyos_c, cargas_c)
except ValueError as error:
    print(f"No se puede analizar. {error}")
