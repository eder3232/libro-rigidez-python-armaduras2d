inicial = nodos[barras[3]["nodo_inicial"]]
final = nodos[barras[3]["nodo_final"]]
dx = final["x"] - inicial["x"]
dy = final["y"] - inicial["y"]
L = math.sqrt(dx**2 + dy**2)
print(f"L = {L:.3f} m")
