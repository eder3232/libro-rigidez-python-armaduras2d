geometria_b = calcular_geometria(nodos_b, barras_b)
rigideces_b = calcular_rigideces(barras_b, geometria_b)
K_b = ensamblar_rigidez(nodos_b, barras_b, rigideces_b)

print("K del ejemplo B en kN/mm:")
mostrar_matriz(K_b / 1000, list(range(1, 9)),
               decimales=0, ancho=6)
print(f"Simétrica: {np.allclose(K_b, K_b.T)}")
print(f"Rango: {np.linalg.matrix_rank(K_b)} de 8")
