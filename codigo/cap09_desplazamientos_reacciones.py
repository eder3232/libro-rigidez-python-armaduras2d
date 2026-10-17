# %% [markdown]
# # Capítulo 9. Desplazamientos y reacciones
#
# Este notebook acompaña al capítulo 9 del libro *Análisis matricial de
# armaduras con Python*. Resolvemos el sistema, calculamos las reacciones y
# verificamos el equilibrio.

# %% [markdown]
# ## 9.2 Resolver un sistema de ecuaciones con NumPy

# %% tags=["exploracion"]
# [inicio: c09_solve]
# Apoyos sin asentamientos: U_r es nulo
U_r = np.zeros(len(restringidos))
lado_derecho = F_l - K_lr @ U_r
U_l = np.linalg.solve(K_ll, lado_derecho)
U_l * 1000  # en mm
# [fin: c09_solve]

# %% tags=["exploracion"]
# [inicio: c09_residuo]
residuo = K_ll @ U_l - lado_derecho
print(f"Mayor residuo: {np.abs(residuo).max():.1e} kN")
print(np.allclose(K_ll @ U_l, lado_derecho))
# [fin: c09_residuo]

# %% tags=["exploracion"]
# [inicio: c09_inv]
U_l_con_inv = np.linalg.inv(K_ll) @ lado_derecho
np.allclose(U_l_con_inv, U_l)
# [fin: c09_inv]

# %% [markdown]
# ## 9.3 Armaduras inestables: `raise`, `try` y `except`

# %% tags=["acumulable"]
# [inicio: c09_resolver]
def resolver_desplazamientos(K_ll, K_lr, F_l, U_r):
    """Desplazamientos de los gdl libres, U_l."""
    if np.linalg.matrix_rank(K_ll) < len(K_ll):
        raise ValueError("La armadura es inestable: "
                         "K_ll es singular.")
    return np.linalg.solve(K_ll, F_l - K_lr @ U_r)
# [fin: c09_resolver]

# %% tags=["exploracion"]
# [inicio: c09_inestable]
barras_sin_1 = {2: barras[2], 3: barras[3]}
K_sin_1 = ensamblar_rigidez(nodos, barras_sin_1,
                            rigideces)
K_ll_sin_1, K_lr_sin_1, _, _ = particionar(
    K_sin_1, libres, restringidos)
try:
    resolver_desplazamientos(K_ll_sin_1, K_lr_sin_1,
                             F_l, U_r)
except ValueError as error:
    print(f"No se puede resolver. {error}")
# [fin: c09_inestable]

# %% [markdown]
# ## 9.4 Desplazamientos y reacciones del ejemplo A

# %% tags=["acumulable"]
# [inicio: c09_desplazamientos]
U_r = np.zeros(len(restringidos))
U_l = resolver_desplazamientos(K_ll, K_lr, F_l, U_r)

# Vector completo de desplazamientos
U = np.zeros(2 * len(nodos))
U[indices(libres)] = U_l
U[indices(restringidos)] = U_r
# [fin: c09_desplazamientos]

# %% tags=["exploracion"]
# [inicio: c09_mostrar_u]
print(" gdl    U (mm)")
mostrar_vector(U * 1000, list(range(1, len(U) + 1)),
               decimales=3)
# [fin: c09_mostrar_u]

# %% tags=["libro"]
# Desplazamientos que cita el texto, en mm (gdl 5 y 6: nodo 3; gdl 3: nodo 2)
ux_3, uy_3, ux_2 = U[indices([5, 6, 3])] * 1000
valor_libro("c09_ux_3", ux_3, 3)
valor_libro("c09_uy_3", uy_3, 3)
valor_libro("c09_uy_3_abajo", -uy_3, 3)
valor_libro("c09_ux_2", ux_2, 3)

# %% tags=["acumulable"]
# [inicio: c09_reacciones]
def calcular_reacciones(K_rl, K_rr, U_l, U_r, F_r):
    """Reacciones en los grados de libertad restringidos.

    F_r son las cargas aplicadas directamente sobre los
    apoyos (normalmente ceros)."""
    return K_rl @ U_l + K_rr @ U_r - F_r


F_r = F[indices(restringidos)]
R = calcular_reacciones(K_rl, K_rr, U_l, U_r, F_r)
# [fin: c09_reacciones]

# %% tags=["exploracion"]
# [inicio: c09_mostrar_r]
print(" gdl    R (kN)")
mostrar_vector(R, restringidos)
# [fin: c09_mostrar_r]

# %% [markdown]
# ## 9.5 Verificación del equilibrio

# %% tags=["acumulable"]
# [inicio: c09_equilibrio]
def comprobar_equilibrio(nodos, F, R, restringidos):
    """Resultantes de cargas más reacciones: Fx, Fy y el
    momento respecto del origen. Deben ser nulas."""
    total = F.copy()
    total[indices(restringidos)] += R
    momento = 0.0
    for nodo in nodos:
        ix, iy = indices(gdl_del_nodo(nodo))
        x, y = nodos[nodo]["x"], nodos[nodo]["y"]
        momento += x * total[iy] - y * total[ix]
    return total[0::2].sum(), total[1::2].sum(), momento
# [fin: c09_equilibrio]

# %% tags=["exploracion"]
# [inicio: c09_comprobar]
suma_x, suma_y, momento = comprobar_equilibrio(
    nodos, F, R, restringidos)
print(f"Suma de fuerzas en x: {suma_x:.2e} kN")
print(f"Suma de fuerzas en y: {suma_y:.2e} kN")
print(f"Suma de momentos:     {momento:.2e} kN·m")
# [fin: c09_comprobar]

# %% [markdown]
# ## Problema resuelto 9.1: el ejemplo B

# %% tags=["exploracion"]
# [inicio: c09_problema_resuelto]
geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, K_rl_b, K_rr_b = particionar(
    K_b, libres_b, restringidos_b)

U_r_b = np.zeros(len(restringidos_b))
U_l_b = resolver_desplazamientos(
    K_ll_b, K_lr_b, F_b[indices(libres_b)], U_r_b)
R_b = calcular_reacciones(
    K_rl_b, K_rr_b, U_l_b, U_r_b,
    F_b[indices(restringidos_b)])

print(" gdl    U (mm)")
mostrar_vector(U_l_b * 1000, libres_b, decimales=3)
print(" gdl    R (kN)")
mostrar_vector(R_b, restringidos_b)
# [fin: c09_problema_resuelto]

# %% tags=["exploracion"]
# [inicio: c09_problema_resuelto_equilibrio]
suma_x, suma_y, momento = comprobar_equilibrio(
    nodos_b, F_b, R_b, restringidos_b)
print(f"ΣFx = {suma_x:.1e}, ΣFy = {suma_y:.1e}, "
      f"ΣM = {momento:.1e}")
# [fin: c09_problema_resuelto_equilibrio]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 9.1: reacción vertical del nodo 2 del ejemplo A, en kN
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 38.333) < 1e-2:
    print("Correcto.")
else:
    print("Todavía no. Tome momentos respecto del nodo 1.")

# %% tags=["exploracion"]
# Ejercicio 9.4: mayor desplazamiento del ejemplo B, en mm
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 0.900) < 1e-3:
    print("Correcto.")
else:
    print("Todavía no. Use np.abs y max sobre los desplazamientos en mm.")
