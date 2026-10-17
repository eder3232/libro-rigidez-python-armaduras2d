fig, ax = plt.subplots()
dibujar_fuerzas(ax, nodos, barras, N)
for nodo in apoyos:
    punto = nodos[nodo]
    ax.plot(punto["x"], punto["y"] - 0.25, marker="^",
            markersize=14, color="black")
ax.set_ylim(-0.8, 4.5)
ax.set_title("Fuerzas axiales y apoyos (kN)")
plt.show()
