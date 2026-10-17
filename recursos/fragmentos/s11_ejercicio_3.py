geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)
F_b = ensamblar_cargas(nodos_b, cargas_b)
libres_b, restringidos_b = clasificar_gdl(nodos_b,
                                          apoyos_b)
K_ll_b, K_lr_b, _, _ = particionar(K_b, libres_b,
                                   restringidos_b)
U_b = np.zeros(2 * len(nodos_b))
U_b[indices(libres_b)] = resolver_desplazamientos(
    K_ll_b, K_lr_b, F_b[indices(libres_b)],
    np.zeros(len(restringidos_b)))
N_b = fuerzas_axiales(barras_b, geometria_b, U_b)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.5, 2.8))
escala = escala_automatica(nodos_b, U_b)
dibujar_armadura(ax1, nodos_b, barras_b, estilo="--")
deformados = nodos_desplazados(nodos_b, U_b, escala)
dibujar_armadura(ax1, deformados, barras_b,
                 color=PRINCIPAL)
ax1.set_title(f"Deformada (×{escala:.0f})")
dibujar_fuerzas(ax2, nodos_b, barras_b, N_b)
ax2.set_title("Fuerzas axiales (kN)")
for ax in (ax1, ax2):
    ax.axis("off")
fig.tight_layout()
plt.show()
