# %% [markdown]
# # Soluciones del capítulo 9

# %% [markdown]
# ## Ejercicio 9.1

# %%
# [inicio: s09_ejercicio_1]
# Momentos respecto del nodo 1, positivos antihorarios:
# R2y · 6 - 20 · 4 - 50 · 3 = 0
R2y = (20 * 4 + 50 * 3) / 6
R1y = 50 - R2y
R1x = -20
print(f"R1x = {R1x:.2f} kN, R1y = {R1y:.2f} kN, "
      f"R2y = {R2y:.2f} kN")
# [fin: s09_ejercicio_1]

# %% [markdown]
# ## Ejercicio 9.2

# %%
# [inicio: s09_ejercicio_2]
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
# [fin: s09_ejercicio_2]

# %% [markdown]
# ## Ejercicio 9.3

# %%
# [inicio: s09_ejercicio_3]
U_l_doble = resolver_desplazamientos(K_ll, K_lr,
                                     2 * F_l, U_r)
np.allclose(U_l_doble, 2 * U_l)
# [fin: s09_ejercicio_3]

# %% [markdown]
# ## Ejercicio 9.4

# %%
# [inicio: s09_ejercicio_4]
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
# [fin: s09_ejercicio_4]
