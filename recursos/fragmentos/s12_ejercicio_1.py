resultados_c = analizar_armadura(nodos_c, barras_c,
                                 apoyos_c, cargas_c)
iy = indices([8])[0]  # gdl 8: nodo 4, dirección y
flecha = -resultados_c["U"][iy] * 1000
print(f"Flecha en el centro: {flecha:.2f} mm")
print(f"Luz / flecha: {18000 / flecha:.0f}")
