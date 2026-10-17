U_l_doble = resolver_desplazamientos(K_ll, K_lr,
                                     2 * F_l, U_r)
np.allclose(U_l_doble, 2 * U_l)
