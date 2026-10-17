def calcular_reacciones(K_rl, K_rr, U_l, U_r, F_r):
    """Reacciones en los grados de libertad restringidos.

    F_r son las cargas aplicadas directamente sobre los
    apoyos (normalmente ceros)."""
    return K_rl @ U_l + K_rr @ U_r - F_r


F_r = F[indices(restringidos)]
R = calcular_reacciones(K_rl, K_rr, U_l, U_r, F_r)
