solo_barra_2 = {2: barras[2]}
K_2 = ensamblar_rigidez(nodos, solo_barra_2, rigideces)
mostrar_matriz(K_2 / 1000, list(range(1, 7)))
