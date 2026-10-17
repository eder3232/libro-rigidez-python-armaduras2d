# %% [markdown]
# # Capítulo 4. La geometría de todas las barras
#
# Este notebook acompaña al capítulo 4 del libro *Análisis matricial de
# armaduras con Python*. Recorremos las barras con bucles `for` y
# calculamos la geometría de todas ellas.

# %% [markdown]
# ## 4.2 El bucle `for`

# %% tags=["exploracion"]
# [inicio: c04_for_lista]
for numero in [1, 2, 3]:
    print(f"Barra {numero}")
# [fin: c04_for_lista]

# %% tags=["exploracion"]
# [inicio: c04_for_dict]
for numero in barras:
    print(numero, barras[numero]["area"])
# [fin: c04_for_dict]

# %% tags=["exploracion"]
# [inicio: c04_items]
for numero, barra in barras.items():
    i = barra["nodo_inicial"]
    j = barra["nodo_final"]
    print(f"Barra {numero}: del nodo {i} al nodo {j}")
# [fin: c04_items]

# %% tags=["exploracion"]
# [inicio: c04_acumulador]
longitud_total = 0.0
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    longitud_total += math.sqrt(dx**2 + dy**2)
print(f"Longitud total: {longitud_total:.3f} m")
# [fin: c04_acumulador]

# %% [markdown]
# ## 4.3 La geometría de todas las barras

# %% tags=["acumulable"]
# [inicio: c04_geometria]
geometria = {}
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    L = math.sqrt(dx**2 + dy**2)
    geometria[numero] = {"longitud": L,
                         "c": dx / L, "s": dy / L}
# [fin: c04_geometria]

# %% tags=["exploracion"]
# [inicio: c04_tabla]
print("Barra   L (m)       c       s")
for numero, g in geometria.items():
    L, c, s = g["longitud"], g["c"], g["s"]
    print(f"{numero:>5} {L:7.3f} {c:7.4f} {s:7.4f}")
# [fin: c04_tabla]

# %% [markdown]
# ## 4.4 Verificación

# %% tags=["exploracion"]
# [inicio: c04_verificacion]
for numero, g in geometria.items():
    suma = g["c"] ** 2 + g["s"] ** 2
    print(f"Barra {numero}: c² + s² = {suma:.12f}")
# [fin: c04_verificacion]

# %% tags=["exploracion"]
# [inicio: c04_datos_intactos]
barras[1]
# [fin: c04_datos_intactos]

# %% [markdown]
# ## 4.5 Dibujar cualquier armadura

# %% tags=["exploracion"]
# [inicio: c04_dibujo]
fig, ax = plt.subplots()
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    ax.plot([inicial["x"], final["x"]],
            [inicial["y"], final["y"]], "k-o")
    # Número de la barra en su punto medio
    xm = (inicial["x"] + final["x"]) / 2
    ym = (inicial["y"] + final["y"]) / 2
    ax.text(xm, ym, f" {numero}", color="tab:blue")
ax.set_aspect("equal")
ax.set_title("Ejemplo A")
plt.show()
# [fin: c04_dibujo]

# %% [markdown]
# ## Problema resuelto 4.1: la geometría del ejemplo B

# %% tags=["exploracion"]
# [inicio: c04_problema_resuelto]
geometria_b = {}
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    L = math.sqrt(dx**2 + dy**2)
    geometria_b[numero] = {"longitud": L,
                           "c": dx / L, "s": dy / L}

print("Barra   L (m)       c       s")
for numero, g in geometria_b.items():
    L, c, s = g["longitud"], g["c"], g["s"]
    print(f"{numero:>5} {L:7.3f} {c:7.4f} {s:7.4f}")
# [fin: c04_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Resuelva cada ejercicio en su notebook y después ejecute la celda de
# verificación correspondiente.

# %% tags=["exploracion"]
# Ejercicio 4.2: peso propio total del ejemplo A, en kN
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 2.512) < 1e-3:
    print("Correcto.")
else:
    print("Todavía no. El peso de una barra es γ · A · L, con γ = 78.5 kN/m³.")

# %% tags=["exploracion"]
# Ejercicio 4.3: longitud total de las barras del ejemplo B, en m
respuesta = None  # reemplace None por su resultado

if respuesta is None:
    print("Escriba su resultado en lugar de None y vuelva a ejecutar la celda.")
elif abs(respuesta - 24.0) < 1e-3:
    print("Correcto.")
else:
    print("Todavía no. ¿Recorrió barras_b con las coordenadas de nodos_b?")
