# %% [markdown]
# # Soluciones del capítulo 6

# %% [markdown]
# ## Ejercicio 6.1

# %%
# [inicio: s06_ejercicio_1]
# La barra 6 va del nodo 2 al nodo 3
gdl_de_barra(barras_b[6])
# [fin: s06_ejercicio_1]

# %% [markdown]
# ## Ejercicio 6.2

# %%
# [inicio: s06_ejercicio_2]
apoyos_articulados = {
    1: {"x": True, "y": True},
    2: {"x": True, "y": True},
}
libres_2, restringidos_2 = clasificar_gdl(
    nodos, apoyos_articulados)
print(f"Libres:       {libres_2}")
print(f"Restringidos: {restringidos_2}")
grado = indeterminacion(nodos, barras, restringidos_2)
print(f"Grado de indeterminación: {grado}")
# [fin: s06_ejercicio_2]

# %% [markdown]
# ## Ejercicio 6.3

# %%
# [inicio: s06_ejercicio_3]
barras_sin_1 = {2: barras[2], 3: barras[3]}
grado = indeterminacion(nodos, barras_sin_1, restringidos)
print(f"Grado de indeterminación: {grado}")
# [fin: s06_ejercicio_3]

# %% [markdown]
# ## Ejercicio 6.4

# %%
# [inicio: s06_ejercicio_4]
nueva_numeracion = libres + restringidos
for nuevo, original in enumerate(nueva_numeracion, 1):
    print(f"GDL {original} → {nuevo}")
# [fin: s06_ejercicio_4]
