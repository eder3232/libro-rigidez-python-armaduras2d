def ensamblar_cargas(nodos, cargas):
    """Vector de cargas nodales F de la armadura."""
    F = np.zeros(2 * len(nodos))
    for nodo, carga in cargas.items():
        fila_x, fila_y = indices(gdl_del_nodo(nodo))
        F[fila_x] += carga["x"]
        F[fila_y] += carga["y"]
    return F


F = ensamblar_cargas(nodos, cargas)
