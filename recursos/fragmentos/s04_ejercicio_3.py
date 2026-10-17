longitud_total_b = 0.0
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    longitud_total_b += math.sqrt(dx**2 + dy**2)
print(f"Longitud total: {longitud_total_b:.3f} m")
