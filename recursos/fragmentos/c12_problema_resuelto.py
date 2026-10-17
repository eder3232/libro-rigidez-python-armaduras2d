# Corte por el tercer panel (x entre 6 y 9 m)
R1 = 5 * 25.0 / 2  # reacción en cada apoyo, por simetría
h = 3.0
# Momentos respecto del nodo 9 (x = 6): cordón inferior
N_inferior = (R1 * 6 - 25.0 * 3) / h
# Momentos respecto del nodo 4 (x = 9): cordón superior
N_superior = -(R1 * 9 - 25.0 * 6 - 25.0 * 3) / h

N_c = resultados_c["N"]
print(f"Barra 3: secciones {N_inferior:8.2f} kN, "
      f"calculadora {N_c[3]:8.2f} kN")
print(f"Barra 8: secciones {N_superior:8.2f} kN, "
      f"calculadora {N_c[8]:8.2f} kN")
