# %% [markdown]
# # Capítulo 10. Fuerzas internas
#
# Este notebook acompaña al capítulo 10 del libro *Análisis matricial de
# armaduras con Python*. Calculamos la fuerza axial de cada barra y la
# verificamos.

# %% [markdown]
# ## 10.2 La fuerza axial de una barra

# %% tags=["exploracion"]
# [inicio: c10_una_barra]
# Barra 2 del ejemplo A
g = geometria[2]
u = U[indices(gdl_de_barra(barras[2]))]
u_local = matriz_transformacion(g["c"], g["s"]) @ u
k_local = rigidez_local(2.0e8, 0.0020, g["longitud"])
f_local = k_local @ u_local
u1, u2 = u_local * 1000  # en mm
print(f"u'1 = {u1:.3f} mm, u'2 = {u2:.3f} mm")
print(f"Alargamiento: {u2 - u1:.3f} mm")
f1, f2 = f_local
print(f"f'1 = {f1:.2f} kN, f'2 = {f2:.2f} kN")
# [fin: c10_una_barra]

# %% tags=["acumulable"]
# [inicio: c10_fuerzas_axiales]
def fuerzas_axiales(barras, geometria, U):
    """Fuerza axial de cada barra (+ en tracción)."""
    N = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        u = U[indices(gdl_de_barra(barra))]
        T = matriz_transformacion(g["c"], g["s"])
        u_local = T @ u
        k_local = rigidez_local(barra["elasticidad"],
                                barra["area"],
                                g["longitud"])
        N[numero] = (k_local @ u_local)[1]
    return N


N = fuerzas_axiales(barras, geometria, U)
# [fin: c10_fuerzas_axiales]

# %% [markdown]
# ## 10.3 Tablas de resultados

# %% tags=["acumulable"]
# [inicio: c10_clasificar]
def clasificar_fuerza(N, tolerancia=1e-6):
    """Tracción, compresión o sin fuerza."""
    if N > tolerancia:
        return "tracción"
    elif N < -tolerancia:
        return "compresión"
    else:
        return "sin fuerza"
# [fin: c10_clasificar]

# %% tags=["acumulable"]
# [inicio: c10_mostrar_tabla]
def mostrar_tabla(encabezados, filas, decimales=2,
                  ancho=11):
    """Imprime una tabla con columnas alineadas. Los
    números se muestran con los decimales indicados."""
    linea = ""
    for encabezado in encabezados:
        linea += f"{encabezado:>{ancho}}"
    print(linea)
    for fila in filas:
        linea = ""
        for valor in fila:
            if isinstance(valor, str):
                linea += f"{valor:>{ancho}}"
            else:
                linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)
# [fin: c10_mostrar_tabla]

# %% tags=["exploracion"]
# [inicio: c10_tabla_n]
filas = []
for numero, fuerza in N.items():
    sigma = fuerza / barras[numero]["area"] / 1000  # MPa
    filas.append([str(numero), fuerza, sigma,
                  clasificar_fuerza(fuerza)])
mostrar_tabla(["Barra", "N (kN)", "σ (MPa)", "Estado"],
              filas)
# [fin: c10_tabla_n]

# %% [markdown]
# ## 10.4 Verificación: equilibrio de cada nodo

# %% tags=["acumulable"]
# [inicio: c10_equilibrio_nodal]
def equilibrio_nodal(nodos, barras, geometria, N, F, R,
                     restringidos):
    """Mayor desequilibrio en los nodos, con las fuerzas
    de las barras, las cargas y las reacciones."""
    residuo = F.copy()
    residuo[indices(restringidos)] += R
    for numero, barra in barras.items():
        g = geometria[numero]
        c, s = g["c"], g["s"]
        ix, iy, jx, jy = indices(gdl_de_barra(barra))
        # En tracción, la barra tira de cada nodo hacia
        # el otro extremo
        residuo[[ix, iy]] += N[numero] * np.array([c, s])
        residuo[[jx, jy]] -= N[numero] * np.array([c, s])
    return np.abs(residuo).max()
# [fin: c10_equilibrio_nodal]

# %% tags=["exploracion"]
# [inicio: c10_verificar_nodos]
desequilibrio = equilibrio_nodal(nodos, barras, geometria,
                                 N, F, R, restringidos)
print(f"Desequilibrio nodal: {desequilibrio:.1e} kN")
# [fin: c10_verificar_nodos]

# %% [markdown]
# ## Problema resuelto 10.1: el método de los nudos

# %% tags=["exploracion"]
# [inicio: c10_problema_resuelto]
# Nodo 3: incógnitas N2 y N3, en ese orden.
# Barra 2: dirección del nodo 3 al nodo 2 (0.6, -0.8)
# Barra 3: dirección del nodo 3 al nodo 1 (-0.6, -0.8)
A_nodo_3 = np.array([[0.6, -0.6],
                     [-0.8, -0.8]])
b_nodo_3 = np.array([-20.0, 50.0])
N2, N3 = np.linalg.solve(A_nodo_3, b_nodo_3)

# Nodo 2, dirección x: -N1 - 0.6 N2 = 0
N1 = -0.6 * N2
print(f"N1 = {N1:.2f} kN, N2 = {N2:.2f} kN, "
      f"N3 = {N3:.2f} kN")
# [fin: c10_problema_resuelto]

# %% [markdown]
# ## 10.5 Las fuerzas del ejemplo B

# %% tags=["exploracion"]
# [inicio: c10_ejemplo_b]
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
U_b = np.zeros(2 * len(nodos_b))
U_b[indices(libres_b)] = U_l_b

N_b = fuerzas_axiales(barras_b, geometria_b, U_b)
filas = []
for numero, fuerza in N_b.items():
    filas.append([str(numero), fuerza,
                  clasificar_fuerza(fuerza)])
mostrar_tabla(["Barra", "N (kN)", "Estado"], filas)

desequilibrio = equilibrio_nodal(
    nodos_b, barras_b, geometria_b, N_b, F_b, R_b,
    restringidos_b)
print(f"Desequilibrio nodal: {desequilibrio:.1e} kN")
# [fin: c10_ejemplo_b]

# %% tags=["libro"]
# Valores que citan el texto y las figuras del capítulo
for numero, fuerza in N.items():
    valor_libro(f"c10_n{numero}", fuerza, 2)
for numero, fuerza in N_b.items():
    valor_libro(f"c10_nb{numero}", fuerza, 2)
for posicion, gdl in enumerate(restringidos):
    valor_libro(f"c10_r{gdl}_magnitud", abs(R[posicion]), 2)
valor_libro("c10_acortamiento_2", u1 - u2, 3)
valor_libro("c10_nb5_magnitud", abs(N_b[5]), 1)
valor_libro("c10_nb6_magnitud", abs(N_b[6]), 1)
sigma_max = abs(N[2]) / barras[2]["area"] / 1000
valor_libro("c10_sigma_max", sigma_max, 0)

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 10.1: mayor esfuerzo, en valor absoluto, del ejemplo A, en MPa
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 23.96) < 0.01:
    print("Correcto.")
else:
    print("Todavía no. σ = N / A; recuerde pasar de kN/m² a MPa.")
