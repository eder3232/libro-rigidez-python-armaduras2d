fig, ax = plt.subplots()
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    ax.plot([inicial["x"], final["x"]],
            [inicial["y"], final["y"]], "k-o")
    xm = (inicial["x"] + final["x"]) / 2
    ym = (inicial["y"] + final["y"]) / 2
    ax.text(xm, ym, f" {numero}", color="tab:blue")
ax.set_aspect("equal")
ax.set_title("Ejemplo B")
plt.show()
