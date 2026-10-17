def resolver_desplazamientos(K_ll, K_lr, F_l, U_r):
    """Desplazamientos de los gdl libres, U_l."""
    if np.linalg.matrix_rank(K_ll) < len(K_ll):
        raise ValueError("La armadura es inestable: "
                         "K_ll es singular.")
    return np.linalg.solve(K_ll, F_l - K_lr @ U_r)
