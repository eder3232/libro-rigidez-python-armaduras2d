orden = libres + restringidos
K_ordenada = K_global[np.ix_(indices(orden),
                             indices(orden))]
mostrar_matriz(K_ordenada / 1000, orden)
