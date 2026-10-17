al_reves = {3: barras[3], 2: barras[2], 1: barras[1]}
K_al_reves = ensamblar_rigidez(nodos, al_reves, rigideces)
np.allclose(K_al_reves, K_global)
