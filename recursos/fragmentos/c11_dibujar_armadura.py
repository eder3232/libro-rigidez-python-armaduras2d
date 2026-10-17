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
