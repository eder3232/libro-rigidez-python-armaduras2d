def graficar_resultados(nodos, barras, resultados,
                        titulo="", decimales=1,
                        tamano=None):
    """Deformada y diagrama de fuerzas, en dos paneles:
    uno sobre otro si la armadura es muy alargada."""
    U, N = resultados["U"], resultados["N"]
    xs = []
    ys = []
    for punto in nodos.values():
        xs.append(punto["x"])
        ys.append(punto["y"])
    ancho = max(xs) - min(xs)
    alto = max(ys) - min(ys)
    if ancho > 2 * alto:
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                       figsize=(4.5, 3.6))
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2,
                                       figsize=(4.5, 2.4))
    escala = escala_automatica(nodos, U)
    dibujar_armadura(ax1, nodos, barras, estilo="--")
    deformados = nodos_desplazados(nodos, U, escala)
    dibujar_armadura(ax1, deformados, barras,
                     color=PRINCIPAL)
    ax1.set_title(f"Deformada (×{escala:.0f})")
    ax1.axis("off")
    dibujar_fuerzas(ax2, nodos, barras, N, decimales,
                    tamano)
    ax2.set_title("Fuerzas axiales (kN)")
    fig.suptitle(titulo)
    fig.tight_layout()
    plt.show()
