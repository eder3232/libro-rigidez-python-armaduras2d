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
