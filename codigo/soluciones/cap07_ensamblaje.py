# %% [markdown]
# # Soluciones del capítulo 7

# %% [markdown]
# ## Ejercicio 7.1

# %%
# [inicio: s07_ejercicio_1]
# Al gdl 6 (nodo 3, dirección y) llegan las barras 2 y 3
# Su gdl local es u4 (posición 3 de la matriz de 4 x 4)
aporte_2 = rigideces[2][3, 3] / 1000
aporte_3 = rigideces[3][3, 3] / 1000
fila, columna = indices([6, 6])
termino = K_global[fila, columna] / 1000
print(f"Barra 2: {aporte_2:.1f} kN/mm")
print(f"Barra 3: {aporte_3:.1f} kN/mm")
print(f"Suma:    {aporte_2 + aporte_3:.1f} kN/mm")
print(f"K:       {termino:.1f} kN/mm")
# [fin: s07_ejercicio_1]

# %% [markdown]
# ## Ejercicio 7.2

# %%
# [inicio: s07_ejercicio_2]
solo_barra_2 = {2: barras[2]}
K_2 = ensamblar_rigidez(nodos, solo_barra_2, rigideces)
mostrar_matriz(K_2 / 1000, list(range(1, 7)))
# [fin: s07_ejercicio_2]

# %% [markdown]
# ## Ejercicio 7.3

# %%
# [inicio: s07_ejercicio_3]
traslacion_y = np.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0])
K_global @ traslacion_y
# [fin: s07_ejercicio_3]

# %% [markdown]
# ## Ejercicio 7.4

# %%
# [inicio: s07_ejercicio_4]
al_reves = {3: barras[3], 2: barras[2], 1: barras[1]}
K_al_reves = ensamblar_rigidez(nodos, al_reves, rigideces)
np.allclose(K_al_reves, K_global)
# [fin: s07_ejercicio_4]
