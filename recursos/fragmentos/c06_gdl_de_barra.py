def gdl_de_barra(barra):
    """Grados de libertad de los extremos de una barra."""
    xi, yi = gdl_del_nodo(barra["nodo_inicial"])
    xj, yj = gdl_del_nodo(barra["nodo_final"])
    return [xi, yi, xj, yj]
