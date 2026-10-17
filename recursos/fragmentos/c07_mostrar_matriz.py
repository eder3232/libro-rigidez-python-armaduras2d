def mostrar_matriz(matriz, filas, columnas=None,
                   decimales=1, ancho=7):
    """Imprime una matriz con los grados de libertad
    (desde 1) como encabezados de filas y columnas."""
    if columnas is None:
        columnas = filas
    encabezado = " gdl"
    for g in columnas:
        encabezado += f"{g:>{ancho}}"
    print(encabezado)
    for i, g in enumerate(filas):
        linea = f"{g:>4}"
        for valor in matriz[i]:
            linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)
