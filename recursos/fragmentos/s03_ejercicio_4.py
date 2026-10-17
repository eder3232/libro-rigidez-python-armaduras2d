n1, n2 = nodos_b[1], nodos_b[2]
n3, n4 = nodos_b[3], nodos_b[4]

fig, ax = plt.subplots()
ax.plot([n1["x"], n2["x"]], [n1["y"], n2["y"]], "k-o")
ax.plot([n2["x"], n4["x"]], [n2["y"], n4["y"]], "k-o")
ax.plot([n3["x"], n4["x"]], [n3["y"], n4["y"]], "k-o")
ax.plot([n1["x"], n3["x"]], [n1["y"], n3["y"]], "k-o")
ax.plot([n1["x"], n4["x"]], [n1["y"], n4["y"]], "k-o")
ax.plot([n2["x"], n3["x"]], [n2["y"], n3["y"]], "k-o")
ax.set_aspect("equal")
ax.set_title("Ejemplo B")
plt.show()
