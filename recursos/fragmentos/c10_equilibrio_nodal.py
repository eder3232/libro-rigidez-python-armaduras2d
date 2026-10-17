def equilibrio_nodal(nodos, barras, geometria, N, F, R,
                     restringidos):
    """Mayor desequilibrio en los nodos, con las fuerzas
    de las barras, las cargas y las reacciones."""
    residuo = F.copy()
    residuo[indices(restringidos)] += R
    for numero, barra in barras.items():
        g = geometria[numero]
        c, s = g["c"], g["s"]
        ix, iy, jx, jy = indices(gdl_de_barra(barra))
        # En tracción, la barra tira de cada nodo hacia
        # el otro extremo
        residuo[[ix, iy]] += N[numero] * np.array([c, s])
        residuo[[jx, jy]] -= N[numero] * np.array([c, s])
    return np.abs(residuo).max()
