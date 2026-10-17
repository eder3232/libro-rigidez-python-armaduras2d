geometria_con_angulo = {}
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    theta = math.degrees(math.atan2(dy, dx))
    geometria_con_angulo[numero] = {"theta": theta}

for numero, g in geometria_con_angulo.items():
    print(f"Barra {numero}: θ = {g['theta']:.2f}°")
