# %% [markdown]
# # Soluciones del capítulo 3

# %% [markdown]
# ## Ejercicio 3.1

# %%
# [inicio: s03_ejercicio_1]
inicial = nodos[barras[3]["nodo_inicial"]]
final = nodos[barras[3]["nodo_final"]]
dx = final["x"] - inicial["x"]
dy = final["y"] - inicial["y"]
L = math.sqrt(dx**2 + dy**2)
print(f"L = {L:.3f} m")
# [fin: s03_ejercicio_1]

# %% [markdown]
# ## Ejercicio 3.2

# %%
# [inicio: s03_ejercicio_2]
# Armadura de cubierta. Unidades: kN y m
nodos_cubierta = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 4.0, "y": 0.0},
    3: {"x": 8.0, "y": 0.0},
    4: {"x": 4.0, "y": 1.5},
}

barras_cubierta = {
    1: {"nodo_inicial": 1, "nodo_final": 2,
        "elasticidad": 2.0e8, "area": 0.0015},
    2: {"nodo_inicial": 2, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0015},
    3: {"nodo_inicial": 1, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0015},
    4: {"nodo_inicial": 4, "nodo_final": 3,
        "elasticidad": 2.0e8, "area": 0.0015},
    5: {"nodo_inicial": 2, "nodo_final": 4,
        "elasticidad": 2.0e8, "area": 0.0010},
}

apoyos_cubierta = {
    1: {"x": True, "y": True},   # articulado
    3: {"x": False, "y": True},  # rodillo
}

cargas_cubierta = {
    4: {"x": 0.0, "y": -30.0},
}

print(f"Nodos: {len(nodos_cubierta)}")
print(f"Barras: {len(barras_cubierta)}")
# [fin: s03_ejercicio_2]

# %% [markdown]
# ## Ejercicio 3.3

# %%
# [inicio: s03_ejercicio_3]
print(apoyos.get(3))
print(3 in cargas, 1 in cargas)
# [fin: s03_ejercicio_3]

# %% [markdown]
# ## Ejercicio 3.4

# %%
# [inicio: s03_ejercicio_4]
n1, n2 = nodos_b[1], nodos_b[2]
n3, n4 = nodos_b[3], nodos_b[4]

fig, ax = plt.subplots()
ax.plot([n1["x"], n2["x"]], [n1["y"], n2["y"]], "k-o")
ax.plot([n2["x"], n4["x"]], [n2["y"], n4["y"]], "k-o")
ax.plot([n3["x"], n4["x"]], [n3["y"], n4["y"]], "k-o")
ax.plot([n1["x"], n3["x"]], [n1["y"], n3["y"]], "k-o")
ax.plot([n1["x"], n4["x"]], [n1["y"], n4["y"]], "k-o")
ax.plot([n2["x"], n3["x"]], [n2["y"], n3["y"]], "k-o")
ax.set_aspect("equal")
ax.set_title("Ejemplo B")
plt.show()
# [fin: s03_ejercicio_4]
