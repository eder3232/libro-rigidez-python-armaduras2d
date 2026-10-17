# %% [markdown]
# # Soluciones del capítulo 10

# %% [markdown]
# ## Ejercicio 10.1

# %%
# [inicio: s10_ejercicio_1]
sigma_maxima = 0.0
for numero, fuerza in N.items():
    sigma = abs(fuerza) / barras[numero]["area"] / 1000
    sigma_maxima = max(sigma_maxima, sigma)
print(f"Mayor esfuerzo: {sigma_maxima:.2f} MPa")
fraccion = sigma_maxima / 250  # fy = 250 MPa
print(f"Fracción de la fluencia: {fraccion:.1%}")
# [fin: s10_ejercicio_1]

# %% [markdown]
# ## Ejercicio 10.2

# %%
# [inicio: s10_ejercicio_2]
apoyos_2 = {
    1: {"x": True, "y": True},
    2: {"x": True, "y": True},
}
libres_2, restringidos_2 = clasificar_gdl(nodos, apoyos_2)
K_ll_2, K_lr_2, _, _ = particionar(K_global, libres_2,
                                   restringidos_2)
U_2 = np.zeros(6)
U_2[indices(libres_2)] = resolver_desplazamientos(
    K_ll_2, K_lr_2, F[indices(libres_2)],
    np.zeros(len(restringidos_2)))
N_2 = fuerzas_axiales(barras, geometria, U_2)
filas = []
for numero in barras:
    filas.append([str(numero), N[numero], N_2[numero]])
mostrar_tabla(["Barra", "Rodillo", "Articulado"], filas)
# [fin: s10_ejercicio_2]

# %% [markdown]
# ## Ejercicio 10.3

# %%
# [inicio: s10_ejercicio_3]
barras_dobles = {}
for numero, barra in barras.items():
    copia = dict(barra)
    copia["area"] = 2 * barra["area"]
    barras_dobles[numero] = copia

geometria_d = calcular_geometria(nodos, barras_dobles)
rigideces_d = calcular_rigideces(barras_dobles,
                                 geometria_d)
K_d = ensamblar_rigidez(nodos, barras_dobles,
                        rigideces_d)
K_ll_d, K_lr_d, _, _ = particionar(K_d, libres,
                                   restringidos)
U_d = np.zeros(6)
U_d[indices(libres)] = resolver_desplazamientos(
    K_ll_d, K_lr_d, F_l, U_r)
N_d = fuerzas_axiales(barras_dobles, geometria_d, U_d)
print(f"Desplazamientos a la mitad: "
      f"{np.allclose(U_d, U / 2)}")
filas = []
for numero in barras:
    filas.append([str(numero), N[numero], N_d[numero]])
mostrar_tabla(["Barra", "N (kN)", "N, 2A (kN)"], filas)
# [fin: s10_ejercicio_3]
