barras_sin_1 = {2: barras[2], 3: barras[3]}
K_sin_1 = ensamblar_rigidez(nodos, barras_sin_1,
                            rigideces)
K_ll_sin_1 = particionar(K_sin_1, libres,
                         restringidos)[0]
print(f"Rango de K_ll: "
      f"{np.linalg.matrix_rank(K_ll_sin_1)} de 3")
