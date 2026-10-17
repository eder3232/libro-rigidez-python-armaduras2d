geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, _, _ = particionar(K_b, libres_b,
                                   restringidos_b)
U_l_b = resolver_desplazamientos(
    K_ll_b, K_lr_b, F_b[indices(libres_b)],
    np.zeros(len(restringidos_b)))
maximo = np.abs(U_l_b * 1000).max()
print(f"Mayor desplazamiento: {maximo:.3f} mm")
