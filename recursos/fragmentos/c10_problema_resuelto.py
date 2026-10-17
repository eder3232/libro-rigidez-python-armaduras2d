# Nodo 3: incógnitas N2 y N3, en ese orden.
# Barra 2: dirección del nodo 3 al nodo 2 (0.6, -0.8)
# Barra 3: dirección del nodo 3 al nodo 1 (-0.6, -0.8)
A_nodo_3 = np.array([[0.6, -0.6],
                     [-0.8, -0.8]])
b_nodo_3 = np.array([-20.0, 50.0])
N2, N3 = np.linalg.solve(A_nodo_3, b_nodo_3)

# Nodo 2, dirección x: -N1 - 0.6 N2 = 0
N1 = -0.6 * N2
print(f"N1 = {N1:.2f} kN, N2 = {N2:.2f} kN, "
      f"N3 = {N3:.2f} kN")
