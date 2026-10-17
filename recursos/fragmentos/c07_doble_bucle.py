K = np.zeros((n_gdl, n_gdl))
for numero, barra in barras.items():
    g = gdl_de_barra(barra)
    k = rigideces[numero]
    for a in range(4):
        for b in range(4):
            fila, columna = indices([g[a], g[b]])
            K[fila, columna] += k[a, b]
