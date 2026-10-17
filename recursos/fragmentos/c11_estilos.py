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
