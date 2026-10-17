geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
for numero, k in rigideces_b.items():
    simetrica = np.allclose(k, k.T)
    rango = np.linalg.matrix_rank(k)
    print(f"Barra {numero}: simétrica = {simetrica}, "
          f"rango = {rango}")
