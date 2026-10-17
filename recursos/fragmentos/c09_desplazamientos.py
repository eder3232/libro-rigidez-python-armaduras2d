U_r = np.zeros(len(restringidos))
U_l = resolver_desplazamientos(K_ll, K_lr, F_l, U_r)

# Vector completo de desplazamientos
U = np.zeros(2 * len(nodos))
U[indices(libres)] = U_l
U[indices(restringidos)] = U_r
