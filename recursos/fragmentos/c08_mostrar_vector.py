def mostrar_vector(vector, gdl, decimales=2, ancho=10):
    """Imprime un vector con sus grados de libertad."""
    for i, g in enumerate(gdl):
        valor = round(vector[i], decimales) + 0.0
        print(f"{g:>4}{valor:>{ancho}.{decimales}f}")
