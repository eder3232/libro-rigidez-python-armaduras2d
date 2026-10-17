def ensamblar_rigidez(nodos, barras, rigideces):
    """Matriz de rigidez global de la armadura."""
    n_gdl = 2 * len(nodos)
    K = np.zeros((n_gdl, n_gdl))
    for numero, barra in barras.items():
        g = indices(gdl_de_barra(barra))
        K[np.ix_(g, g)] += rigideces[numero]
    return K


K_global = ensamblar_rigidez(nodos, barras, rigideces)
