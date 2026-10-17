escala = escala_automatica(nodos, U)
fig, ax = plt.subplots()
dibujar_armadura(ax, nodos, barras, estilo="--",
                 etiqueta="Original")
deformados = nodos_desplazados(nodos, U, escala)
dibujar_armadura(ax, deformados, barras, color=PRINCIPAL,
                 etiqueta="Deformada")
ax.set_title(f"Ejemplo A, deformada ×{escala:.0f}")
ax.legend()
plt.show()
