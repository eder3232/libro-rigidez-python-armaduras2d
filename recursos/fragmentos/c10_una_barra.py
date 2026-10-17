# Barra 2 del ejemplo A
g = geometria[2]
u = U[indices(gdl_de_barra(barras[2]))]
u_local = matriz_transformacion(g["c"], g["s"]) @ u
k_local = rigidez_local(2.0e8, 0.0020, g["longitud"])
f_local = k_local @ u_local
u1, u2 = u_local * 1000  # en mm
print(f"u'1 = {u1:.3f} mm, u'2 = {u2:.3f} mm")
print(f"Alargamiento: {u2 - u1:.3f} mm")
f1, f2 = f_local
print(f"f'1 = {f1:.2f} kN, f'2 = {f2:.2f} kN")
