def analizar_armadura(nodos, barras, apoyos, cargas):
    """Análisis completo de una armadura plana.

    Devuelve un diccionario con los resultados."""
    geometria = calcular_geometria(nodos, barras)
    rigideces = calcular_rigideces(barras, geometria)
    K = ensamblar_rigidez(nodos, barras, rigideces)
    F = ensamblar_cargas(nodos, cargas)
    libres, restringidos = clasificar_gdl(nodos, apoyos)
    K_ll, K_lr, K_rl, K_rr = particionar(K, libres,
                                         restringidos)
    U_r = np.zeros(len(restringidos))
    U_l = resolver_desplazamientos(
        K_ll, K_lr, F[indices(libres)], U_r)
    U = np.zeros(2 * len(nodos))
    U[indices(libres)] = U_l
    U[indices(restringidos)] = U_r
    R = calcular_reacciones(K_rl, K_rr, U_l, U_r,
                            F[indices(restringidos)])
    N = fuerzas_axiales(barras, geometria, U)
    return {"geometria": geometria, "K": K, "F": F,
            "U": U, "R": R, "N": N, "libres": libres,
            "restringidos": restringidos}
