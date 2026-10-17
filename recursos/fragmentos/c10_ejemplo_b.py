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
U_b = np.zeros(2 * len(nodos_b))
U_b[indices(libres_b)] = U_l_b

N_b = fuerzas_axiales(barras_b, geometria_b, U_b)
filas = []
for numero, fuerza in N_b.items():
    filas.append([str(numero), fuerza,
                  clasificar_fuerza(fuerza)])
mostrar_tabla(["Barra", "N (kN)", "Estado"], filas)

desequilibrio = equilibrio_nodal(
    nodos_b, barras_b, geometria_b, N_b, F_b, R_b,
    restringidos_b)
print(f"Desequilibrio nodal: {desequilibrio:.1e} kN")
