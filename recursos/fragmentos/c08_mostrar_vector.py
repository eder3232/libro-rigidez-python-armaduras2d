def mostrar_vector(vector, gdl, decimales=2, ancho=10):
    """Imprime un vector con sus grados de libertad."""
    for i, g in enumerate(gdl):
        print(f"{g:>4}{vector[i]:>{ancho}.{decimales}f}")
