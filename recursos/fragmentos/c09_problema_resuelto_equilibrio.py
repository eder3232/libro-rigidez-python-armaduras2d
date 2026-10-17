suma_x, suma_y, momento = comprobar_equilibrio(
    nodos_b, F_b, R_b, restringidos_b)
print(f"ΣFx = {suma_x:.1e}, ΣFy = {suma_y:.1e}, "
      f"ΣM = {momento:.1e}")
