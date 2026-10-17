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
