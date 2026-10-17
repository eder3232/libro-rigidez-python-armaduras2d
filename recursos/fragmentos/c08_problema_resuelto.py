geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, K_rl_b, K_rr_b = particionar(
    K_b, libres_b, restringidos_b)
F_l_b = F_b[indices(libres_b)]

print("K_ll en kN/mm:")
mostrar_matriz(K_ll_b / 1000, libres_b, decimales=0,
               ancho=6)
print(f"Rango de K_ll: {np.linalg.matrix_rank(K_ll_b)}")
print(" gdl  F_l (kN)")
mostrar_vector(F_l_b, libres_b)
