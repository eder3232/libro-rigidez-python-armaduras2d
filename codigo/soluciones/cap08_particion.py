# %% [markdown]
# # Soluciones del capítulo 8

# %% [markdown]
# ## Ejercicio 8.1

# %%
# [inicio: s08_ejercicio_1]
F_b = ensamblar_cargas(nodos_b, cargas_b)
print(f"Ejemplo B, en x: {F_b[0::2].sum():7.2f} kN")
print(f"Ejemplo B, en y: {F_b[1::2].sum():7.2f} kN")
# [fin: s08_ejercicio_1]

# %% [markdown]
# ## Ejercicio 8.2

# %%
# [inicio: s08_ejercicio_2]
cargas_2 = {
    2: {"x": 15.0, "y": 0.0},
    3: {"x": 20.0, "y": -50.0},
}
F_2 = ensamblar_cargas(nodos, cargas_2)
print(" gdl  F (kN)")
mostrar_vector(F_2, list(range(1, 7)))
print(" gdl  F_l (kN)")
mostrar_vector(F_2[indices(libres)], libres)
# [fin: s08_ejercicio_2]

# %% [markdown]
# ## Ejercicio 8.3

# %%
# [inicio: s08_ejercicio_3]
barras_sin_1 = {2: barras[2], 3: barras[3]}
K_sin_1 = ensamblar_rigidez(nodos, barras_sin_1,
                            rigideces)
K_ll_sin_1 = particionar(K_sin_1, libres,
                         restringidos)[0]
print(f"Rango de K_ll: "
      f"{np.linalg.matrix_rank(K_ll_sin_1)} de 3")
# [fin: s08_ejercicio_3]

# %% [markdown]
# ## Ejercicio 8.4

# %%
# [inicio: s08_ejercicio_4]
orden = libres + restringidos
K_ordenada = K_global[np.ix_(indices(orden),
                             indices(orden))]
mostrar_matriz(K_ordenada / 1000, orden)
# [fin: s08_ejercicio_4]
