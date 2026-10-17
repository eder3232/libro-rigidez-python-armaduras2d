fig, ax = plt.subplots()
mayor = 0.0
for fuerza in N.values():
    mayor = max(mayor, abs(fuerza))
for numero, barra in barras.items():
    i = nodos[barra["nodo_inicial"]]
    j = nodos[barra["nodo_final"]]
    if N[numero] > 0:
        color = TRACCION
    else:
        color = COMPRESION
    grosor = 1 + 7 * abs(N[numero]) / mayor
    ax.plot([i["x"], j["x"]], [i["y"], j["y"]],
            color=color, linewidth=grosor,
            solid_capstyle="round")
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Grosor proporcional a |N|")
plt.show()
