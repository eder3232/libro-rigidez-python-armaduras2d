# %% [markdown]
# # Soluciones del capítulo 11

# %% [markdown]
# ## Ejercicio 11.1

# %%
# [inicio: s11_ejercicio_1]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.5, 2.2))
for ax, escala in ((ax1, 100), (ax2, 2000)):
    dibujar_armadura(ax, nodos, barras, estilo="--")
    deformados = nodos_desplazados(nodos, U, escala)
    dibujar_armadura(ax, deformados, barras,
                     color=PRINCIPAL)
    ax.set_title(f"Escala ×{escala}")
    ax.axis("off")
fig.tight_layout()
plt.show()
# [fin: s11_ejercicio_1]

# %% [markdown]
# ## Ejercicio 11.2

# %%
# [inicio: s11_ejercicio_2]
fig, ax = plt.subplots()
dibujar_fuerzas(ax, nodos, barras, N)
for nodo in apoyos:
    punto = nodos[nodo]
    ax.plot(punto["x"], punto["y"] - 0.25, marker="^",
            markersize=14, color="black")
ax.set_ylim(-0.8, 4.5)
ax.set_title("Fuerzas axiales y apoyos (kN)")
plt.show()
# [fin: s11_ejercicio_2]

# %% [markdown]
# ## Ejercicio 11.3

# %%
# [inicio: s11_ejercicio_3]
geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, _, _ = particionar(K_b, libres_b,
                                   restringidos_b)
U_b = np.zeros(2 * len(nodos_b))
U_b[indices(libres_b)] = resolver_desplazamientos(
    K_ll_b, K_lr_b, F_b[indices(libres_b)],
    np.zeros(len(restringidos_b)))
N_b = fuerzas_axiales(barras_b, geometria_b, U_b)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.5, 2.8))
escala = escala_automatica(nodos_b, U_b)
dibujar_armadura(ax1, nodos_b, barras_b, estilo="--")
deformados = nodos_desplazados(nodos_b, U_b, escala)
dibujar_armadura(ax1, deformados, barras_b,
                 color=PRINCIPAL)
ax1.set_title(f"Deformada (×{escala:.0f})")
dibujar_fuerzas(ax2, nodos_b, barras_b, N_b)
ax2.set_title("Fuerzas axiales (kN)")
for ax in (ax1, ax2):
    ax.axis("off")
fig.tight_layout()
plt.show()
# [fin: s11_ejercicio_3]

# %% [markdown]
# ## Ejercicio 11.4

# %%
# [inicio: s11_ejercicio_4]
fig, ax = plt.subplots()
mayor = 0.0
for fuerza in N.values():
    mayor = max(mayor, abs(fuerza))
for numero, barra in barras.items():
    i = nodos[barra["nodo_inicial"]]
    j = nodos[barra["nodo_final"]]
    if N[numero] > 0:
        color = TRACCION
    else:
        color = COMPRESION
    grosor = 1 + 7 * abs(N[numero]) / mayor
    ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
            color=color, linewidth=grosor,
            solid_capstyle="round")
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Grosor proporcional a |N|")
plt.show()
# [fin: s11_ejercicio_4]
