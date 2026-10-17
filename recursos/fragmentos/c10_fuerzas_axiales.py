def fuerzas_axiales(barras, geometria, U):
    """Fuerza axial de cada barra (+ en tracción)."""
    N = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        u = U[indices(gdl_de_barra(barra))]
        T = matriz_transformacion(g["c"], g["s"])
        u_local = T @ u
        k_local = rigidez_local(barra["elasticidad"],
                                barra["area"],
                                g["longitud"])
        N[numero] = (k_local @ u_local)[1]
    return N


N = fuerzas_axiales(barras, geometria, U)
