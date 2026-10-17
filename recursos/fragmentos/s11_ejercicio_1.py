fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.5, 2.2))
for ax, escala in ((ax1, 100), (ax2, 2000)):
    dibujar_armadura(ax, nodos, barras, estilo="--")
    deformados = nodos_desplazados(nodos, U, escala)
    dibujar_armadura(ax, deformados, barras,
                     color=PRINCIPAL)
    ax.set_title(f"Escala ×{escala}")
    ax.axis("off")
fig.tight_layout()
plt.show()
