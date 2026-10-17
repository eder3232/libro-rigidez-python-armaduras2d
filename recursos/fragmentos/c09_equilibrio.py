def comprobar_equilibrio(nodos, F, R, restringidos):
    """Resultantes de cargas más reacciones: Fx, Fy y el
    momento respecto del origen. Deben ser nulas."""
    total = F.copy()
    total[indices(restringidos)] += R
    momento = 0.0
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        x, y = nodos[nodo]["x"], nodos[nodo]["y"]
        momento += x * total[iy] - y * total[ix]
    return total[0::2].sum(), total[1::2].sum(), momento
