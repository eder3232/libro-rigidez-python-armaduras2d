geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, K_rl_b, K_rr_b = particionar(
    K_b, libres_b, restringidos_b)

U_r_b = np.zeros(len(restringidos_b))
U_l_b = resolver_desplazamientos(
    K_ll_b, K_lr_b, F_b[indices(libres_b)], U_r_b)
R_b = calcular_reacciones(
    K_rl_b, K_rr_b, U_l_b, U_r_b,
    F_b[indices(restringidos_b)])

print(" gdl    U (mm)")
mostrar_vector(U_l_b * 1000, libres_b, decimales=3)
print(" gdl    R (kN)")
mostrar_vector(R_b, restringidos_b)
