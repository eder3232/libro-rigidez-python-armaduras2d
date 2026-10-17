# Al gdl 6 (nodo 3, dirección y) llegan las barras 2 y 3
# Su gdl local es u4 (posición 3 de la matriz de 4 x 4)
aporte_2 = rigideces[2][3, 3] / 1000
aporte_3 = rigideces[3][3, 3] / 1000
fila, columna = indices([6, 6])
termino = K_global[fila, columna] / 1000
print(f"Barra 2: {aporte_2:.1f} kN/mm")
print(f"Barra 3: {aporte_3:.1f} kN/mm")
print(f"Suma:    {aporte_2 + aporte_3:.1f} kN/mm")
print(f"K:       {termino:.1f} kN/mm")
