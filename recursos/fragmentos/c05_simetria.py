for numero, k in rigideces.items():
    simetrica = np.allclose(k, k.T)
    rango = np.linalg.matrix_rank(k)
    print(f"Barra {numero}: simétrica = {simetrica}, "
          f"rango = {rango}")
