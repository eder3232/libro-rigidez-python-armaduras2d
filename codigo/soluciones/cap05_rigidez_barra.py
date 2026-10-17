# %% [markdown]
# # Soluciones del capítulo 5

# %% [markdown]
# ## Ejercicio 5.1

# %%
# [inicio: s05_ejercicio_1]
def peso_barra(A, L, gamma=78.5):
    """Peso propio de una barra, en kN."""
    return gamma * A * L


peso_total = 0.0
for numero, barra in barras.items():
    L = geometria[numero]["longitud"]
    peso_total += peso_barra(barra["area"], L)
print(f"Peso propio: {peso_total:.3f} kN")
# [fin: s05_ejercicio_1]

# %% [markdown]
# ## Ejercicio 5.2

# %%
# [inicio: s05_ejercicio_2]
g = geometria[3]
c, s = g["c"], g["s"]
# El nodo final se mueve 1 mm perpendicular a la barra
perpendicular = 0.001 * np.array([0.0, 0.0, -s, c])
rigideces[3] @ perpendicular
# [fin: s05_ejercicio_2]

# %% [markdown]
# ## Ejercicio 5.3

# %%
# [inicio: s05_ejercicio_3]
# Barra vertical de 3 m: de (0, 0) a (0, 3)
k_vertical = rigidez_barra(2.0e8, 0.0010, 3.0, 0.0, 1.0)
k_vertical
# [fin: s05_ejercicio_3]

# %% [markdown]
# ## Ejercicio 5.4

# %%
# [inicio: s05_ejercicio_4]
geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
for numero, k in rigideces_b.items():
    simetrica = np.allclose(k, k.T)
    rango = np.linalg.matrix_rank(k)
    print(f"Barra {numero}: simétrica = {simetrica}, "
          f"rango = {rango}")
# [fin: s05_ejercicio_4]
