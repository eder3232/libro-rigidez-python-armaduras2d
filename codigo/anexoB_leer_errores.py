# %% [markdown]
# # Anexo B. Leer un error de Python
#
# Cada celda de este archivo produce, a propósito, uno de los errores más
# frecuentes al construir la calculadora. scripts/generar_salidas.py guarda
# el mensaje de cada una para mostrarlo en el libro (etiqueta "error").
# Se ejecuta después de todos los capítulos, con la calculadora completa.

# %% [markdown]
# ## B.1 Cómo se lee un mensaje de error: KeyError

# %% tags=["error"]
# [inicio: b_clave]
barras_mal = {
    1: barra(1, 2, 0.0020),
    2: barra(2, 4, 0.0020),
    3: barra(3, 1, 0.0020),
}
geometria_mal = calcular_geometria(nodos, barras_mal)
# [fin: b_clave]

# %% [markdown]
# ## B.2 Un nombre mal escrito: NameError

# %% tags=["error"]
# [inicio: b_nombre]
geometria = calcular_geometria(nodos, barras)
rigideces = calcular_rigideces(barras, geometira)
# [fin: b_nombre]

# %% [markdown]
# ## B.3 Errores de escritura: SyntaxError e IndentationError

# %% tags=["error"]
# [inicio: b_sintaxis]
for numero in barras
    print(numero)
# [fin: b_sintaxis]

# %% tags=["error"]
# [inicio: b_sangria]
for numero in barras:
print(numero)
# [fin: b_sangria]

# %% [markdown]
# ## B.4 Datos equivocados

# %% tags=["error"]
# [inicio: b_argumentos]
k = rigidez_local(2.0e8, 0.0020)
# [fin: b_argumentos]

# %% tags=["error"]
# [inicio: b_indice]
resultados = analizar_armadura(nodos, barras,
                               apoyos, cargas)
U = resultados["U"]
uy_3 = U[6]
# [fin: b_indice]

# %% tags=["error"]
# [inicio: b_division]
nodos_mal = {
    1: {"x": 0.0, "y": 0.0},
    2: {"x": 6.0, "y": 0.0},
    3: {"x": 6.0, "y": 0.0},
}
geometria_mal = calcular_geometria(nodos_mal, barras)
# [fin: b_division]

# %% [markdown]
# ## B.5 Los errores de la calculadora: ValueError

# %% tags=["error"]
# [inicio: b_inestable]
apoyos_mal = {1: {"x": True, "y": True}}
resultados = analizar_armadura(nodos, barras,
                               apoyos_mal, cargas)
# [fin: b_inestable]
