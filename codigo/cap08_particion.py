# %% [markdown]
# # Capítulo 8. Cargas y partición del sistema
#
# Este notebook acompaña al capítulo 8 del libro *Análisis matricial de
# armaduras con Python*. Ensamblamos el vector de cargas y dividimos el
# sistema en bloques de grados de libertad libres y restringidos.

# %% [markdown]
# ## 8.2 El vector de cargas

# %% tags=["acumulable"]
# [inicio: c08_ensamblar_cargas]
def ensamblar_cargas(nodos, cargas):
    """Vector de cargas nodales F de la armadura."""
    F = np.zeros(2 * len(nodos))
    for nodo, carga in cargas.items():
        fila_x, fila_y = indices(gdl_del_nodo(nodo))
        F[fila_x] += carga["x"]
        F[fila_y] += carga["y"]
    return F


F = ensamblar_cargas(nodos, cargas)
# [fin: c08_ensamblar_cargas]

# %% tags=["acumulable"]
# [inicio: c08_mostrar_vector]
def mostrar_vector(vector, gdl, decimales=2, ancho=10):
    """Imprime un vector con sus grados de libertad."""
    for i, g in enumerate(gdl):
        print(f"{g:>4}{vector[i]:>{ancho}.{decimales}f}")
# [fin: c08_mostrar_vector]

# %% tags=["exploracion"]
# [inicio: c08_mostrar_vector_f]
print(" gdl  F (kN)")
mostrar_vector(F, list(range(1, len(F) + 1)))
# [fin: c08_mostrar_vector_f]

# %% [markdown]
# ## 8.3 Rebanadas

# %% tags=["exploracion"]
# [inicio: c08_rebanadas]
print(F[0:2])   # gdl 1 y 2: el nodo 1
print(F[0::2])  # gdl 1, 3, 5: las componentes en x
print(F[1::2])  # gdl 2, 4, 6: las componentes en y
# [fin: c08_rebanadas]

# %% tags=["exploracion"]
# [inicio: c08_suma_cargas]
print(f"Suma de cargas en x: {F[0::2].sum():7.2f} kN")
print(f"Suma de cargas en y: {F[1::2].sum():7.2f} kN")
# [fin: c08_suma_cargas]

# %% [markdown]
# ## 8.4 La partición del sistema

# %% tags=["acumulable"]
# [inicio: c08_particionar]
def particionar(K, libres, restringidos):
    """Bloques Kll, Klr, Krl y Krr de la matriz K."""
    l = indices(libres)
    r = indices(restringidos)
    K_ll = K[np.ix_(l, l)]
    K_lr = K[np.ix_(l, r)]
    K_rl = K[np.ix_(r, l)]
    K_rr = K[np.ix_(r, r)]
    return K_ll, K_lr, K_rl, K_rr


K_ll, K_lr, K_rl, K_rr = particionar(K_global, libres,
                                     restringidos)
F_l = F[indices(libres)]
# [fin: c08_particionar]

# %% tags=["exploracion"]
# [inicio: c08_mostrar_bloques]
print("K_ll en kN/mm:")
mostrar_matriz(K_ll / 1000, libres)
print("K_lr en kN/mm:")
mostrar_matriz(K_lr / 1000, libres, restringidos)
print(" gdl  F_l (kN)")
mostrar_vector(F_l, libres)
# [fin: c08_mostrar_bloques]

# %% [markdown]
# ## 8.5 Verificación

# %% tags=["exploracion"]
# [inicio: c08_verificacion]
print(f"K_ll: {K_ll.shape}, rango "
      f"{np.linalg.matrix_rank(K_ll)}")
print(f"K_lr es la transpuesta de K_rl: "
      f"{np.allclose(K_lr, K_rl.T)}")
# [fin: c08_verificacion]

# %% [markdown]
# ## Problema resuelto 8.1: el ejemplo B

# %% tags=["exploracion"]
# [inicio: c08_problema_resuelto]
geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, K_rl_b, K_rr_b = particionar(
    K_b, libres_b, restringidos_b)
F_l_b = F_b[indices(libres_b)]

print("K_ll en kN/mm:")
mostrar_matriz(K_ll_b / 1000, libres_b, decimales=0,
               ancho=6)
print(f"Rango de K_ll: {np.linalg.matrix_rank(K_ll_b)}")
print(" gdl  F_l (kN)")
mostrar_vector(F_l_b, libres_b)
# [fin: c08_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 8.3: rango de K_ll sin la barra 1
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif respuesta == 2:
    print("Correcto.")
else:
    print("Todavía no. Ensamble K sin la barra 1 y particione con los mismos gdl.")
