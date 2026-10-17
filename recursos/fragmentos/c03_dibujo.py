n1, n2, n3 = nodos[1], nodos[2], nodos[3]

fig, ax = plt.subplots()
# Barra 1: del nodo 1 al nodo 2
ax.plot([n1["x"], n2["x"]], [n1["y"], n2["y"]], "k-o")
# Barra 2: del nodo 2 al nodo 3
ax.plot([n2["x"], n3["x"]], [n2["y"], n3["y"]], "k-o")
# Barra 3: del nodo 1 al nodo 3
ax.plot([n1["x"], n3["x"]], [n1["y"], n3["y"]], "k-o")
ax.set_aspect("equal")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title("Ejemplo A")
plt.show()
