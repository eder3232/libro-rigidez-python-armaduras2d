suma_x, suma_y, momento = comprobar_equilibrio(
    nodos, F, R, restringidos)
print(f"Suma de fuerzas en x: {suma_x:.2e} kN")
print(f"Suma de fuerzas en y: {suma_y:.2e} kN")
print(f"Suma de momentos:     {momento:.2e} kN·m")
