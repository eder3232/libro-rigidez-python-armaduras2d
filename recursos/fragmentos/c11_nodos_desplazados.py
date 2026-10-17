def nodos_desplazados(nodos, U, escala):
    """Nodos en su posición deformada, con los
    desplazamientos multiplicados por la escala."""
    nuevos = {}
    for nodo, punto in nodos.items():
        ix, iy = indices(gdl_del_nodo(nodo))
        nuevos[nodo] = {"x": punto["x"] + escala * U[ix],
                        "y": punto["y"] + escala * U[iy]}
    return nuevos
