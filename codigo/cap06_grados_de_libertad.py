# %% [markdown]
# # Capítulo 6. Los grados de libertad
#
# Este notebook acompaña al capítulo 6 del libro *Análisis matricial de
# armaduras con Python*. Numeramos los grados de libertad, los
# clasificamos en libres y restringidos, y revisamos la estabilidad.

# %% [markdown]
# ## 6.2 Decisiones con `if`

# %% tags=["exploracion"]
# [inicio: c06_comparaciones]
area = barras[1]["area"]
print(area > 0.001, len(barras) == 3, len(nodos) != 3)
# [fin: c06_comparaciones]

# %% tags=["exploracion"]
# [inicio: c06_condicional]
apoyo = apoyos[2]
if apoyo["x"]:
    print("El nodo 2 no puede moverse en x")
else:
    print("El nodo 2 puede moverse en x")
# [fin: c06_condicional]

# %% [markdown]
# ## 6.3 La numeración de los grados de libertad

# %% tags=["acumulable"]
# [inicio: c06_gdl_del_nodo]
def gdl_del_nodo(nodo):
    """Grados de libertad (x, y) del nodo, desde 1."""
    return 2 * nodo - 1, 2 * nodo
# [fin: c06_gdl_del_nodo]

# %% tags=["exploracion"]
# [inicio: c06_gdl_del_nodo_uso]
gdl_x, gdl_y = gdl_del_nodo(3)
print(f"Nodo 3: x → {gdl_x}, y → {gdl_y}")
# [fin: c06_gdl_del_nodo_uso]

# %% tags=["acumulable"]
# [inicio: c06_gdl_de_barra]
def gdl_de_barra(barra):
    """Grados de libertad de los extremos de una barra."""
    xi, yi = gdl_del_nodo(barra["nodo_inicial"])
    xj, yj = gdl_del_nodo(barra["nodo_final"])
    return [xi, yi, xj, yj]
# [fin: c06_gdl_de_barra]

# %% tags=["exploracion"]
# [inicio: c06_tabla_gdl]
for numero, barra in barras.items():
    print(f"Barra {numero}: {gdl_de_barra(barra)}")
# [fin: c06_tabla_gdl]

# %% [markdown]
# ## 6.4 Grados de libertad libres y restringidos

# %% tags=["acumulable"]
# [inicio: c06_clasificar]
def clasificar_gdl(nodos, apoyos):
    """Grados de libertad libres y restringidos."""
    libres = []
    restringidos = []
    sin_apoyo = {"x": False, "y": False}
    for nodo in nodos:
        gdl_x, gdl_y = gdl_del_nodo(nodo)
        apoyo = apoyos.get(nodo, sin_apoyo)
        if apoyo["x"]:
            restringidos.append(gdl_x)
        else:
            libres.append(gdl_x)
        if apoyo["y"]:
            restringidos.append(gdl_y)
        else:
            libres.append(gdl_y)
    return libres, restringidos
# [fin: c06_clasificar]

# %% tags=["acumulable"]
# [inicio: c06_clasificar_uso]
libres, restringidos = clasificar_gdl(nodos, apoyos)
# [fin: c06_clasificar_uso]

# %% tags=["exploracion"]
# [inicio: c06_clasificar_resultado]
print(f"Libres:       {libres}")
print(f"Restringidos: {restringidos}")
# [fin: c06_clasificar_resultado]

# %% [markdown]
# ## 6.5 De la numeración desde 1 a los índices de Python

# %% tags=["acumulable"]
# [inicio: c06_indices]
def indices(gdl):
    """Traduce grados de libertad (desde 1) a índices
    de NumPy (desde 0). Es el único lugar del libro donde
    se hace esta traducción."""
    resultado = []
    for g in gdl:
        resultado.append(g - 1)
    return resultado
# [fin: c06_indices]

# %% tags=["exploracion"]
# [inicio: c06_indices_uso]
# Un valor por cada grado de libertad del ejemplo A
valores = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
print(indices(libres))
valores[indices(libres)]
# [fin: c06_indices_uso]

# %% [markdown]
# ## 6.6 Una revisión previa de la estabilidad

# %% tags=["acumulable"]
# [inicio: c06_indeterminacion]
def indeterminacion(nodos, barras, restringidos):
    """b + r - 2n: incógnitas menos ecuaciones."""
    b, r, n = len(barras), len(restringidos), len(nodos)
    return b + r - 2 * n
# [fin: c06_indeterminacion]

# %% tags=["exploracion"]
# [inicio: c06_clasificacion]
grado = indeterminacion(nodos, barras, restringidos)
if grado < 0:
    print(f"Inestable: faltan {-grado} barras o apoyos")
elif grado == 0:
    print("Estáticamente determinada (isostática)")
else:
    print(f"Hiperestática de grado {grado}")
# [fin: c06_clasificacion]

# %% [markdown]
# ## Problema resuelto 6.1: los grados de libertad del ejemplo B

# %% tags=["exploracion"]
# [inicio: c06_problema_resuelto]
for numero, barra in barras_b.items():
    print(f"Barra {numero}: {gdl_de_barra(barra)}")

libres_b, restringidos_b = clasificar_gdl(
    nodos_b, apoyos_b)
print(f"Libres:       {libres_b}")
print(f"Restringidos: {restringidos_b}")

grado_b = indeterminacion(nodos_b, barras_b,
                          restringidos_b)
print(f"Grado de indeterminación: {grado_b}")
# [fin: c06_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 6.1: grados de libertad de la barra 6 del ejemplo B
respuesta = None  # reemplace None por una lista, por ejemplo [1, 2, 3, 4]

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif respuesta == [3, 4, 5, 6]:
    print("Correcto.")
else:
    print("Todavía no. La barra 6 va del nodo 2 al nodo 3.")

# %% tags=["exploracion"]
# Ejercicio 6.2: grado de indeterminación con dos apoyos articulados
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif respuesta == 1:
    print("Correcto.")
else:
    print("Todavía no. ¿Cuántas reacciones tiene ahora la armadura?")
