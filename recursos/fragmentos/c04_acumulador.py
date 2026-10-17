longitud_total = 0.0
for numero, barra in barras.items():
    inicial = nodos[barra["nodo_inicial"]]
    final = nodos[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    longitud_total += math.sqrt(dx**2 + dy**2)
print(f"Longitud total: {longitud_total:.3f} m")
