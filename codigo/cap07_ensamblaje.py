# %% [markdown]
# # Capítulo 7. Ensamblaje de la matriz global
#
# Este notebook acompaña al capítulo 7 del libro *Análisis matricial de
# armaduras con Python*. Ensamblamos la matriz de rigidez de la armadura
# a partir de las matrices de sus barras.

# %% [markdown]
# ## 7.2 Matrices de ceros e índices

# %% tags=["exploracion"]
# [inicio: c07_zeros]
n_gdl = 2 * len(nodos)
K = np.zeros((n_gdl, n_gdl))
K.shape
# [fin: c07_zeros]

# %% tags=["exploracion"]
# [inicio: c07_indexar]
# Término de la fila del gdl 5 y la columna del gdl 6
fila, columna = indices([5, 6])
K[fila, columna] += 10.0
K[fila, columna] += 2.5
print(fila, columna, K[fila, columna])
# [fin: c07_indexar]

# %% tags=["exploracion"]
# [inicio: c07_range]
for a in range(4):
    print(a, end=" ")
# [fin: c07_range]

# %% [markdown]
# ## 7.3 El ensamblaje, término a término

# %% tags=["exploracion"]
# [inicio: c07_doble_bucle]
K = np.zeros((n_gdl, n_gdl))
for numero, barra in barras.items():
    g = gdl_de_barra(barra)
    k = rigideces[numero]
    for a in range(4):
        for b in range(4):
            fila, columna = indices([g[a], g[b]])
            K[fila, columna] += k[a, b]
# [fin: c07_doble_bucle]

# %% [markdown]
# ## 7.4 Mostrar una matriz con sus grados de libertad

# %% tags=["acumulable"]
# [inicio: c07_mostrar_matriz]
def mostrar_matriz(matriz, filas, columnas=None,
                   decimales=1, ancho=7):
    """Imprime una matriz con los grados de libertad
    (desde 1) como encabezados de filas y columnas."""
    if columnas is None:
        columnas = filas
    encabezado = " gdl"
    for g in columnas:
        encabezado += f"{g:>{ancho}}"
    print(encabezado)
    for i, g in enumerate(filas):
        linea = f"{g:>4}"
        for valor in matriz[i]:
            linea += f"{valor:>{ancho}.{decimales}f}"
        print(linea)
# [fin: c07_mostrar_matriz]

# %% tags=["exploracion"]
# [inicio: c07_mostrar_k_global]
todos = list(range(1, n_gdl + 1))
print("K en kN/mm:")
mostrar_matriz(K / 1000, todos)
# [fin: c07_mostrar_k_global]

# %% [markdown]
# ## 7.5 El ensamblaje con `np.ix_`

# %% tags=["exploracion"]
# [inicio: c07_ix]
g = indices(gdl_de_barra(barras[2]))
print(g)
K[np.ix_(g, g)].shape
# [fin: c07_ix]

# %% tags=["acumulable"]
# [inicio: c07_ensamblar]
def ensamblar_rigidez(nodos, barras, rigideces):
    """Matriz de rigidez global de la armadura."""
    n_gdl = 2 * len(nodos)
    K = np.zeros((n_gdl, n_gdl))
    for numero, barra in barras.items():
        g = indices(gdl_de_barra(barra))
        K[np.ix_(g, g)] += rigideces[numero]
    return K


K_global = ensamblar_rigidez(nodos, barras, rigideces)
# [fin: c07_ensamblar]

# %% tags=["exploracion"]
# [inicio: c07_comparar]
np.allclose(K_global, K)
# [fin: c07_comparar]

# %% [markdown]
# ## 7.6 Verificación

# %% tags=["exploracion"]
# [inicio: c07_verificacion]
simetrica = np.allclose(K_global, K_global.T)
rango = np.linalg.matrix_rank(K_global)
print(f"Simétrica: {simetrica}")
print(f"Rango: {rango} de {n_gdl}")
# [fin: c07_verificacion]

# %% tags=["exploracion"]
# [inicio: c07_cuerpo_rigido]
# Toda la armadura se traslada 1 mm en x
traslacion_x = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 0.0])
K_global @ traslacion_x
# [fin: c07_cuerpo_rigido]

# %% [markdown]
# ## Problema resuelto 7.1: la matriz global del ejemplo B

# %% tags=["exploracion"]
# [inicio: c07_problema_resuelto]
geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)

print("K del ejemplo B en kN/mm:")
mostrar_matriz(K_b / 1000, list(range(1, 9)),
               decimales=0, ancho=6)
print(f"Simétrica: {np.allclose(K_b, K_b.T)}")
print(f"Rango: {np.linalg.matrix_rank(K_b)} de 8")
# [fin: c07_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 7.1: término de la fila y columna del gdl 6, en kN/mm
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 102.4) < 0.05:
    print("Correcto.")
else:
    print("Todavía no. ¿Qué barras llegan al nodo 3? Sume sus términos en s².")
