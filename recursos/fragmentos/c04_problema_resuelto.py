geometria_b = {}
for numero, barra in barras_b.items():
    inicial = nodos_b[barra["nodo_inicial"]]
    final = nodos_b[barra["nodo_final"]]
    dx = final["x"] - inicial["x"]
    dy = final["y"] - inicial["y"]
    L = math.sqrt(dx**2 + dy**2)
    geometria_b[numero] = {"longitud": L,
                           "c": dx / L, "s": dy / L}

print("Barra   L (m)       c       s")
for numero, g in geometria_b.items():
    L, c, s = g["longitud"], g["c"], g["s"]
    print(f"{numero:>5} {L:7.3f} {c:7.4f} {s:7.4f}")
