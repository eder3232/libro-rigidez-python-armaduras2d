# %% [markdown]
# # Soluciones del capítulo 4

# %% [markdown]
# ## Ejercicio 4.1

# %%
# [inicio: s04_ejercicio_1]
geometria_con_angulo = {}
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    theta = math.degrees(math.atan2(dy, dx))
    geometria_con_angulo[numero] = {"theta": theta}

for numero, g in geometria_con_angulo.items():
    print(f"Barra {numero}: θ = {g['theta']:.2f}°")
# [fin: s04_ejercicio_1]

# %% [markdown]
# ## Ejercicio 4.2

# %%
# [inicio: s04_ejercicio_2]
gamma = 78.5  # peso específico del acero, en kN/m³
peso_total = 0.0
for numero, barra in barras.items():
    L = geometria[numero]["longitud"]
    peso_total += gamma * barra["area"] * L
print(f"Peso propio: {peso_total:.3f} kN")
# [fin: s04_ejercicio_2]

# %% [markdown]
# ## Ejercicio 4.3

# %%
# [inicio: s04_ejercicio_3]
longitud_total_b = 0.0
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    longitud_total_b += math.sqrt(dx**2 + dy**2)
print(f"Longitud total: {longitud_total_b:.3f} m")
# [fin: s04_ejercicio_3]

# %% [markdown]
# ## Ejercicio 4.4

# %%
# [inicio: s04_ejercicio_4]
fig, ax = plt.subplots()
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    ax.plot([inicial["x"], final["x"]],
            [inicial["y"], final["y"]], "k-o")
    xm = (inicial["x"] + final["x"]) / 2
    ym = (inicial["y"] + final["y"]) / 2
    ax.text(xm, ym, f" {numero}", color="tab:blue")
ax.set_aspect("equal")
ax.set_title("Ejemplo B")
plt.show()
# [fin: s04_ejercicio_4]
