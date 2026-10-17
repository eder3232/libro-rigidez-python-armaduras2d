simetrica = np.allclose(K_global, K_global.T)
rango = np.linalg.matrix_rank(K_global)
print(f"Simétrica: {simetrica}")
print(f"Rango: {rango} de {n_gdl}")
