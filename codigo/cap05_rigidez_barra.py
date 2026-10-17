# %% [markdown]
# # Capítulo 5. La rigidez de una barra
#
# Este notebook acompaña al capítulo 5 del libro *Análisis matricial de
# armaduras con Python*. Escribimos las primeras funciones de la
# calculadora y construimos la matriz de rigidez de cada barra con NumPy.

# %% [markdown]
# ## 5.2 Funciones

# %% tags=["exploracion"]
# [inicio: c05_primera_funcion]
def rigidez_axial(E, A, L):
    """Rigidez axial EA/L de una barra, en kN/m."""
    return E * A / L


rigidez_axial(2.0e8, 0.0020, 5.0)
# [fin: c05_primera_funcion]

# %% tags=["acumulable"]
# [inicio: c05_calcular_geometria]
def calcular_geometria(nodos, barras):
    """Longitud y cosenos directores de cada barra.

    Devuelve un diccionario {número de barra:
    {"longitud": L, "c": c, "s": s}}.
    """
    geometria = {}
    for numero, barra in barras.items():
        inicial = nodos[barra["nodo_inicial"]]
        final = nodos[barra["nodo_final"]]
        dx = final["x"] - inicial["x"]
        dy = final["y"] - inicial["y"]
        L = math.sqrt(dx**2 + dy**2)
        geometria[numero] = {"longitud": L,
                             "c": dx / L, "s": dy / L}
    return geometria
# [fin: c05_calcular_geometria]

# %% tags=["exploracion"]
# [inicio: c05_usar_geometria]
geometria = calcular_geometria(nodos, barras)
geometria_b = calcular_geometria(nodos_b, barras_b)
geometria_b[6]
# [fin: c05_usar_geometria]

# %% [markdown]
# ## 5.3 NumPy

# %% tags=["acumulable"]
# [inicio: c05_import_numpy]
import numpy as np

np.set_printoptions(precision=1, suppress=True)
# [fin: c05_import_numpy]

# %% tags=["exploracion"]
# [inicio: c05_arreglo]
k_local = np.array([[1, -1],
                    [-1, 1]])
k_local.shape
# [fin: c05_arreglo]

# %% tags=["exploracion"]
# [inicio: c05_operaciones]
80000 * k_local
# [fin: c05_operaciones]

# %% tags=["exploracion"]
# [inicio: c05_producto]
# Barra 3 del ejemplo A: c = 0.6, s = 0.8
T = np.array([[0.6, 0.8, 0.0, 0.0],
              [0.0, 0.0, 0.6, 0.8]])
# El nodo final se mueve 3 mm en x y 4 mm en y
u = np.array([0.0, 0.0, 3.0, 4.0])
print(T.shape, u.shape, T.T.shape)
T @ u
# [fin: c05_producto]

# %% [markdown]
# ## 5.4 La matriz de rigidez de una barra

# %% tags=["acumulable"]
# [inicio: c05_funciones_rigidez]
def rigidez_local(E, A, L):
    """Matriz de rigidez de la barra en sus ejes (2x2)."""
    return E * A / L * np.array([[1.0, -1.0],
                                 [-1.0, 1.0]])


def matriz_transformacion(c, s):
    """Matriz T (2 x 4) tal que u' = T u."""
    return np.array([[c, s, 0.0, 0.0],
                     [0.0, 0.0, c, s]])


def rigidez_barra(E, A, L, c, s):
    """Matriz de rigidez de la barra en ejes globales."""
    T = matriz_transformacion(c, s)
    return T.T @ rigidez_local(E, A, L) @ T
# [fin: c05_funciones_rigidez]

# %% tags=["exploracion"]
# [inicio: c05_barra_1]
g = geometria[1]
k1 = rigidez_barra(2.0e8, 0.0020, g["longitud"],
                   g["c"], g["s"])
k1
# [fin: c05_barra_1]

# %% tags=["acumulable"]
# [inicio: c05_todas_las_barras]
def calcular_rigideces(barras, geometria):
    """Matriz de rigidez global (4 x 4) de cada barra."""
    rigideces = {}
    for numero, barra in barras.items():
        g = geometria[numero]
        rigideces[numero] = rigidez_barra(
            barra["elasticidad"], barra["area"],
            g["longitud"], g["c"], g["s"])
    return rigideces


geometria = calcular_geometria(nodos, barras)
rigideces = calcular_rigideces(barras, geometria)
# [fin: c05_todas_las_barras]

# %% [markdown]
# ## 5.5 Verificación

# %% tags=["exploracion"]
# [inicio: c05_simetria]
for numero, k in rigideces.items():
    simetrica = np.allclose(k, k.T)
    rango = np.linalg.matrix_rank(k)
    print(f"Barra {numero}: simétrica = {simetrica}, "
          f"rango = {rango}")
# [fin: c05_simetria]

# %% tags=["exploracion"]
# [inicio: c05_cuerpo_rigido]
# Traslación de la barra 2 como cuerpo rígido: 1 mm en x
traslacion = np.array([0.001, 0.0, 0.001, 0.0])
rigideces[2] @ traslacion
# [fin: c05_cuerpo_rigido]

# %% [markdown]
# ## Problema resuelto 5.1: la barra 2 del ejemplo A

# %% tags=["exploracion"]
# [inicio: c05_problema_resuelto]
g = geometria[2]
EA_L = 2.0e8 * 0.0020 / g["longitud"]
c, s = g["c"], g["s"]
print(f"EA/L = {EA_L:.0f} kN/m, c = {c:.1f}, s = {s:.1f}")
print(f"EA/L·c²  = {EA_L * c**2:9.1f}")
print(f"EA/L·cs  = {EA_L * c * s:9.1f}")
print(f"EA/L·s²  = {EA_L * s**2:9.1f}")
rigideces[2]
# [fin: c05_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 5.1: peso propio total del ejemplo A, en kN
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 2.512) < 1e-3:
    print("Correcto.")
else:
    print("Todavía no. ¿Sumó el peso de las tres barras con su función?")

# %% tags=["exploracion"]
# Ejercicio 5.3: término k[1, 1] de la barra vertical, en kN/m
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 66666.67) < 0.1:
    print("Correcto.")
else:
    print("Todavía no. En una barra vertical, c = 0 y s = 1.")
