def mostrar_matriz(matriz, gdl, decimales=1, ancho=7):
    """Imprime una matriz con los grados de libertad
    (desde 1) como encabezados de filas y columnas."""
    encabezado = " gdl"
    for g in gdl:
        encabezado += f"{g:>{ancho}}"
    print(encabezado)
    for i, g in enumerate(gdl):
        linea = f"{g:>4}"
        for valor in matriz[i]:
            linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)
