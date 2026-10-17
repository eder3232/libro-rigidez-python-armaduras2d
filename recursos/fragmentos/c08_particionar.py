def particionar(K, libres, restringidos):
    """Bloques Kll, Klr, Krl y Krr de la matriz K."""
    l = indices(libres)
    r = indices(restringidos)
    K_ll = K[np.ix_(l, l)]
    K_lr = K[np.ix_(l, r)]
    K_rl = K[np.ix_(r, l)]
    K_rr = K[np.ix_(r, r)]
    return K_ll, K_lr, K_rl, K_rr


K_ll, K_lr, K_rl, K_rr = particionar(K_global, libres,
                                     restringidos)
F_l = F[indices(libres)]
