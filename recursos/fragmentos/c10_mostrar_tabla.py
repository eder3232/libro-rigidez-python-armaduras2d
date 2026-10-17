def mostrar_tabla(encabezados, filas, decimales=2,
                  ancho=11):
    """Imprime una tabla con columnas alineadas. Los
    números se muestran con los decimales indicados."""
    linea = ""
    for encabezado in encabezados:
        linea += f"{encabezado:>{ancho}}"
    print(linea)
    for fila in filas:
        linea = ""
        for valor in fila:
            if isinstance(valor, str):
                linea += f"{valor:>{ancho}}"
            else:
                linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)
