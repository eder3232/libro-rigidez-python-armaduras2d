# %% [markdown]
# # Capítulo 11. Visualizar los resultados
#
# Este notebook acompaña al capítulo 11 del libro *Análisis matricial de
# armaduras con Python*. Dibujamos la deformada de la armadura y el
# diagrama de fuerzas axiales.

# %% [markdown]
# ## 11.2 Matplotlib con más detalle

# %% tags=["acumulable"]
# [inicio: c11_colores]
# Colores del libro, distinguibles con daltonismo
TRACCION = "#0072B2"
COMPRESION = "#D55E00"
PRINCIPAL = "#1F4E79"
NEUTRO = "#8C8C8C"
# [fin: c11_colores]

# %% tags=["exploracion"]
# [inicio: c11_estilos]
fig, ax = plt.subplots()
ax.plot([0, 6], [0, 0], color=TRACCION, linewidth=3,
        label="Tracción")
ax.plot([0, 3], [0, 4], color=COMPRESION, linewidth=3,
        label="Compresión")
ax.plot([0, 3, 6], [0, 4, 0], color=NEUTRO,
        linestyle="--", marker="o", label="Geometría")
ax.text(3, 0.2, "texto en (3, 0.2)", ha="center")
ax.set_aspect("equal")
ax.legend()
plt.show()
# [fin: c11_estilos]

# %% [markdown]
# ## 11.3 Una función para dibujar la armadura

# %% tags=["acumulable"]
# [inicio: c11_dibujar_armadura]
def dibujar_armadura(ax, nodos, barras, color=NEUTRO,
                     estilo="-", etiqueta=None):
    """Dibuja las barras de una armadura en ax."""
    for barra in barras.values():
        i = nodos[barra["nodo_inicial"]]
        j = nodos[barra["nodo_final"]]
        ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
                color=color, linestyle=estilo, marker="o",
                markersize=4, label=etiqueta)
        etiqueta = None  # la leyenda, una sola vez
    ax.set_aspect("equal")
# [fin: c11_dibujar_armadura]

# %% [markdown]
# ## 11.4 La deformada

# %% tags=["acumulable"]
# [inicio: c11_nodos_desplazados]
def nodos_desplazados(nodos, U, escala):
    """Nodos en su posición deformada, con los
    desplazamientos multiplicados por la escala."""
    nuevos = {}
    for nodo, punto in nodos.items():
        ix, iy = indices(gdl_del_nodo(nodo))
        nuevos[nodo] = {"x": punto["x"] + escala * U[ix],
                        "y": punto["y"] + escala * U[iy]}
    return nuevos
# [fin: c11_nodos_desplazados]

# %% tags=["acumulable"]
# [inicio: c11_escala_automatica]
def escala_automatica(nodos, U, fraccion=0.1):
    """Escala para que el mayor desplazamiento dibujado
    sea una fracción del tamaño de la armadura."""
    xs = []
    ys = []
    for punto in nodos.values():
        xs.append(punto["x"])
        ys.append(punto["y"])
    tamano = max(max(xs) - min(xs), max(ys) - min(ys))
    return fraccion * tamano / np.abs(U).max()
# [fin: c11_escala_automatica]

# %% tags=["exploracion"]
# [inicio: c11_deformada]
escala = escala_automatica(nodos, U)
fig, ax = plt.subplots()
dibujar_armadura(ax, nodos, barras, estilo="--",
                 etiqueta="Original")
deformados = nodos_desplazados(nodos, U, escala)
dibujar_armadura(ax, deformados, barras, color=PRINCIPAL,
                 etiqueta="Deformada")
ax.set_title(f"Ejemplo A, deformada ×{escala:.0f}")
ax.legend()
plt.show()
# [fin: c11_deformada]

# %% [markdown]
# ## 11.5 El diagrama de fuerzas axiales

# %% tags=["acumulable"]
# [inicio: c11_dibujar_fuerzas]
def dibujar_fuerzas(ax, nodos, barras, N, decimales=1):
    """Barras en colores según su fuerza axial, con su
    valor en kN al 40 % de cada barra."""
    for numero, barra in barras.items():
        estado = clasificar_fuerza(N[numero])
        if estado == "tracción":
            color = TRACCION
        elif estado == "compresión":
            color = COMPRESION
        else:
            color = NEUTRO
        i = nodos[barra["nodo_inicial"]]
        j = nodos[barra["nodo_final"]]
        ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
                color=color, linewidth=3)
        # Al 40 % y no en el punto medio: así no se tapan
        # los valores de dos diagonales que se cruzan
        xm = i["x"] + 0.4 * (j["x"] - i["x"])
        ym = i["y"] + 0.4 * (j["y"] - i["y"])
        fondo = {"facecolor": "white", "linewidth": 0}
        ax.text(xm, ym, f"{N[numero]:.{decimales}f}",
                color=color, ha="center", va="center",
                bbox=fondo)
    # Leyenda con líneas vacías: solo muestran los colores
    ax.plot([], [], color=TRACCION, linewidth=3,
            label="Tracción")
    ax.plot([], [], color=COMPRESION, linewidth=3,
            label="Compresión")
    # Leyenda debajo del dibujo, para no tapar las barras
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0),
              ncol=2, frameon=False)
    ax.set_aspect("equal")
    ax.axis("off")
# [fin: c11_dibujar_fuerzas]

# %% tags=["exploracion"]
# [inicio: c11_fuerzas]
fig, ax = plt.subplots()
dibujar_fuerzas(ax, nodos, barras, N)
ax.set_title("Fuerzas axiales del ejemplo A (kN)")
plt.show()
# [fin: c11_fuerzas]

# %% [markdown]
# ## Problema resuelto 11.1: un informe gráfico

# %% tags=["exploracion"]
# [inicio: c11_problema_resuelto]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.5, 2.2))

escala = escala_automatica(nodos, U)
dibujar_armadura(ax1, nodos, barras, estilo="--")
dibujar_armadura(ax1, nodos_desplazados(nodos, U, escala),
                 barras, color=PRINCIPAL)
ax1.set_title(f"Deformada (×{escala:.0f})")

dibujar_fuerzas(ax2, nodos, barras, N)
ax2.set_title("Fuerzas axiales (kN)")

for ax in (ax1, ax2):
    ax.axis("off")  # sin ejes: es un esquema
fig.tight_layout()
plt.show()
# [fin: c11_problema_resuelto]

# %% [markdown]
# ## Ejercicios
#
# Los ejercicios de este capítulo son gráficos: compare su dibujo con
# el de la solución.
