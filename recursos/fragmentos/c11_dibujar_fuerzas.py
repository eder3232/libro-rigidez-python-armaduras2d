def dibujar_fuerzas(ax, nodos, barras, N, decimales=1,
                    tamano=None):
    """Barras en colores según su fuerza axial, con su
    valor en kN al 40 % de cada barra. tamano: tamaño
    de letra de los valores."""
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
        valor = round(N[numero], decimales) + 0.0
        fondo = {"facecolor": "white", "linewidth": 0}
        ax.text(xm, ym, f"{valor:.{decimales}f}",
                color=color, ha="center", va="center",
                bbox=fondo, fontsize=tamano)
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
