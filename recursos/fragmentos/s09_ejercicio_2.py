apoyos_2 = {
    1: {"x": True, "y": True},
    2: {"x": True, "y": True},
}
libres_2, restringidos_2 = clasificar_gdl(nodos, apoyos_2)
K_ll_2, K_lr_2, K_rl_2, K_rr_2 = particionar(
    K_global, libres_2, restringidos_2)
U_r_2 = np.zeros(len(restringidos_2))
U_l_2 = resolver_desplazamientos(
    K_ll_2, K_lr_2, F[indices(libres_2)], U_r_2)
R_2 = calcular_reacciones(K_rl_2, K_rr_2, U_l_2, U_r_2,
                          F[indices(restringidos_2)])
print(" gdl    U (mm)")
mostrar_vector(U_l_2 * 1000, libres_2, decimales=3)
print(" gdl    R (kN)")
mostrar_vector(R_2, restringidos_2)
